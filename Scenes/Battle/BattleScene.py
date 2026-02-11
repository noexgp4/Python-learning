import pygame
from Scenes.Battle.BattleSystem import BattleSystem
from Scenes.Battle.BattleUI import BattleUI
from Scenes.text import UIConfig
from .models.entity import Entity

class BattleScene:
    def __init__(self, screen, player_entity, enemies):
        self.screen = screen
        self.player = player_entity
        # 支持传入单个敌人或敌人列表
        self.enemies = enemies if isinstance(enemies, list) else [enemies]
        self.system = BattleSystem(self.player, self.enemies)
        self.ui = BattleUI(screen)
        
        self.main_options = ["普通攻击", "使用技能", "防御模式", "撤退逃跑"]
        self.current_menu = "MAIN" 
        self.selected_index = 0
        self.pending_action = None # 记录选中的动作索引

        # 反击计时器
        self.enemy_action_timer = 0
        self.is_waiting_for_enemy = False

        # 狙击决策菜单
        self.aim_confirm_options = ["立即释放", "继续蓄力"]

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN: return None

        # 胜负结算后按逻辑返回
        if self.system.state in ["WIN", "LOSS"]:
            if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE]:
                return "WORLD"
        
        # 如果正在等待怪物反击，屏蔽玩家输入
        if self.is_waiting_for_enemy or self.system.state != "IDLE":
            return None

        # --- 狙击蓄力决策逻辑 ---
        # 如果玩家正在蓄力，在下一回合行动前必须决定是否释放
        if self.current_menu != "CONFIRM_AIM" and getattr(self.player, "aim_charge", 0) > 0:
            self.current_menu = "CONFIRM_AIM"
            self.selected_index = 0
            return None

        # --- 获取当前菜单选项总数 ---
        if self.current_menu == "MAIN":
            options_count = len(self.main_options)
            cols = 2
        elif self.current_menu == "SKILL":
            options_count = len(self.player.active_skills)
            cols = 2
        elif self.current_menu == "CONFIRM_AIM":
            options_count = len(self.aim_confirm_options)
            cols = 2
        else: # TARGET
            options_count = len(self.enemies)
            cols = 1

        # --- 通用网格/列表导航 ---
        if self.current_menu == "TARGET":
            living_indices = [i for i, e in enumerate(self.enemies) if e.hp > 0]
            if not living_indices: return None
            
            try:
                current_living_pos = living_indices.index(self.selected_index)
            except ValueError:
                current_living_pos = 0
                self.selected_index = living_indices[0]

            if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_LEFT or event.key == pygame.K_a:
                current_living_pos = (current_living_pos - 1) % len(living_indices)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                current_living_pos = (current_living_pos + 1) % len(living_indices)
            
            self.selected_index = living_indices[current_living_pos]
        else:
            # --- 通用网格/列表导航 (MAIN, SKILL, CONFIRM_AIM) ---
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if self.selected_index >= cols: self.selected_index -= cols
                else: self.selected_index = (self.selected_index + options_count - (options_count % cols or cols)) % options_count
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if self.selected_index + cols < options_count: self.selected_index += cols
                else: self.selected_index %= cols
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if self.selected_index % cols > 0: self.selected_index -= 1
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if self.selected_index % cols < cols - 1 and self.selected_index + 1 < options_count:
                    self.selected_index += 1

        # --- 确认逻辑 ---
        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.current_menu == "MAIN":
                choice = self.main_options[self.selected_index]
                if choice == "普通攻击":
                    self.pending_action = -1
                    self.current_menu = "TARGET"
                    self.selected_index = 0 # 默认指向第一个目标
                elif choice == "使用技能":
                    self.current_menu = "SKILL"
                    self.selected_index = 0
                elif choice == "撤退逃跑":
                    return "WORLD"
            elif self.current_menu == "SKILL":
                self.pending_action = self.selected_index
                self.current_menu = "TARGET"
                self.selected_index = 0
            elif self.current_menu == "CONFIRM_AIM":
                choice = self.aim_confirm_options[self.selected_index]
                if choice == "立即释放":
                    # 寻找之前的瞄准目标
                    target = self.player.aim_target
                    # 找到目标在列表中的索引
                    t_idx = 0
                    if target in self.enemies: t_idx = self.enemies.index(target)
                    
                    # 执行狙击（BattleSystem 会识别出 aim_charge > 0）
                    res = self.system.process_action(self.pending_action, t_idx)
                    if res and res["status"] == "SUCCESS":
                        self.current_menu = "MAIN"
                        self.selected_index = 0
                        self.trigger_enemy_counter()
                else:
                    # 继续蓄力：跳过本回合行为，增加层数
                    if self.player.aim_charge < 4:
                        self.player.aim_charge += 1
                        self.system.battle_log = f"{self.player.job_name} 稳住呼吸，威力进一步提升... (蓄力 {self.player.aim_charge}/4)"
                    else:
                        self.system.battle_log = f"已达到蓄力上限！威力已达 500%！"
                    
                    self.current_menu = "MAIN"
                    self.selected_index = 0
                    self.trigger_enemy_counter() # 进入敌人回合

            elif self.current_menu == "TARGET":
                res = self.system.process_action(self.pending_action, self.selected_index)
                if res and res["status"] == "SUCCESS":
                    self.current_menu = "MAIN"
                    self.selected_index = 0
                    self.trigger_enemy_counter()
        
        elif event.key == pygame.K_ESCAPE:

            if self.current_menu == "CONFIRM_AIM": return None # 必须选，不能取消
            if self.current_menu == "SKILL":
                self.current_menu = "MAIN"
                self.selected_index = 1
            elif self.current_menu == "TARGET":
                self.current_menu = "SKILL" if self.pending_action != -1 else "MAIN"
                self.selected_index = self.pending_action if self.pending_action != -1 else 0

        return None

    def trigger_enemy_counter(self):
        """触发怪物反击的准备工作"""
        self.is_waiting_for_enemy = True
        self.enemy_action_timer = 45 # 约 0.75 秒后反击 (假设 60fps)

    def update(self):
        # 1. 逻辑状态更新（处理胜负检测）
        self.system.update()
        
        # 2. 处理飘字特效
        if self.system.action_result:
            res = self.system.action_result
            target = res['target']
            # 根据目标的逻辑坐标（如果有）或默认位置飘字
            if target == self.player:
                pos = (self.screen.get_width() - 300, self.screen.get_height() - 350)
            else:
                # 假设 target 是敌人，尝试获取其在 Tiled 中定义的 pos，否则使用默认
                t_pos = getattr(target, 'pos', (200, 250))
                pos = (t_pos[0] + 50, t_pos[1] + 50)
                
            self.ui.trigger_damage_num(res['damage'], pos)
            self.system.action_result = {}

        # 3. 处理反击计时器
        if self.is_waiting_for_enemy and self.system.state == "IDLE":
            if self.enemy_action_timer > 0:
                self.enemy_action_timer -= 1
            else:
                self.is_waiting_for_enemy = False
                self.system.execute_enemy_turn()

    def draw(self):
        sw, sh = self.screen.get_width(), self.screen.get_height()
        self.screen.fill((10, 10, 18))
        
        # 日志
        UIConfig.draw_center_text(self.screen, UIConfig.render_text(self.system.battle_log, "normal"), 50)

        # 状态条与背景 - 这里的 UI 需要支持多怪列表
        target_sel = self.selected_index if self.current_menu == "TARGET" else -1
        self.ui.draw_character_portraits(self.player, self.enemies, target_sel)
        self.ui.draw_enemy_status(self.enemies)
        self.ui.draw_player_status(self.player)

        # 菜单绘制 (如果正在等待怪物行动，可以给菜单加个半透明遮罩表示不可用)
        if self.system.state == "IDLE":
            if self.current_menu == "MAIN":
                self.ui.draw_menu_grid(self.main_options, self.selected_index, self.player.theme_color)
            elif self.current_menu == "SKILL":
                self.ui.draw_skill_menu_grid(self.player, self.selected_index)
            elif self.current_menu == "CONFIRM_AIM":
                # 绘制特殊的决策弹窗
                self.ui.draw_menu_grid(self.aim_confirm_options, self.selected_index, (255, 50, 50))
                UIConfig.draw_center_text(self.screen, UIConfig.render_text("--- 狙击蓄力中：是否释放？ ---", "normal", (255, 215, 0)), sh - 220)
            
            # 如果是等待怪物状态，可以在菜单上画一个淡淡的锁定层 (可选)
            if self.is_waiting_for_enemy:
                pass

        if self.system.state == "WIN":
            UIConfig.draw_center_text(self.screen, UIConfig.render_text("胜利！(按回车键返回)", "title", (255, 215, 0)), sh // 2)
        elif self.system.state == "LOSS":
            UIConfig.draw_center_text(self.screen, UIConfig.render_text("战败...", "title", (255, 50, 50)), sh // 2)

        self.ui.update_and_draw_effects()