import pygame
from Scenes.Battle.BattleSystem import BattleSystem
from Scenes.Battle.BattleUI import BattleUI
from Scenes.text import UIConfig
from .models.entity import Entity

class BattleScene:
    def __init__(self, screen, player_entity, enemy_entity):
        self.screen = screen
        self.player = player_entity
        self.enemy = enemy_entity
        self.system = BattleSystem(self.player, self.enemy)
        self.ui = BattleUI(screen)
        
        self.main_options = ["普通攻击", "使用技能", "防御模式", "撤退逃跑"]
        self.current_menu = "MAIN" 
        self.selected_index = 0
        
        # 反击计时器
        self.enemy_action_timer = 0
        self.is_waiting_for_enemy = False

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN: return None

        # 胜负结算后按逻辑返回
        if self.system.state in ["WIN", "LOSS"]:
            if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE]:
                return "WORLD"
        
        # 如果正在等待怪物反击，屏蔽玩家输入
        if self.is_waiting_for_enemy or self.system.state != "IDLE":
            return None

        options_count = len(self.main_options) if self.current_menu == "MAIN" else len(self.player.active_skills)
        cols = 2

        # 网格导航逻辑
        if event.key == pygame.K_UP:
            if self.selected_index >= cols: self.selected_index -= cols
        elif event.key == pygame.K_DOWN:
            if self.selected_index + cols < options_count: self.selected_index += cols
        elif event.key == pygame.K_LEFT:
            if self.selected_index % cols > 0: self.selected_index -= 1
        elif event.key == pygame.K_RIGHT:
            if self.selected_index % cols < cols - 1 and self.selected_index + 1 < options_count:
                self.selected_index += 1
        
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.current_menu == "MAIN":
                choice = self.main_options[self.selected_index]
                if choice == "普通攻击":
                    res = self.system.process_action(-1)
                    if res and res["status"] == "SUCCESS":
                        self.trigger_enemy_counter()
                elif choice == "使用技能":
                    self.current_menu = "SKILL"
                    self.selected_index = 0
                elif choice == "撤退逃跑":
                    return "WORLD"
            elif self.current_menu == "SKILL":
                res = self.system.process_action(self.selected_index)
                if res and res["status"] == "SUCCESS":
                    self.current_menu = "MAIN"
                    self.selected_index = 1
                    self.trigger_enemy_counter()
        
        elif event.key == pygame.K_ESCAPE:
            if self.current_menu == "SKILL":
                self.current_menu = "MAIN"
                self.selected_index = 1

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
            # 伤害数字漂浮位置：目标是敌人则在左半边，目标是玩家则在右半边
            pos = (200, 250) if res['target'] == self.enemy else (self.screen.get_width() - 300, self.screen.get_height() - 350)
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

        # 状态条与背景
        self.ui.draw_character_portraits(self.player, self.enemy)
        self.ui.draw_enemy_status(self.enemy)
        self.ui.draw_player_status(self.player)

        # 菜单绘制 (如果正在等待怪物行动，可以给菜单加个半透明遮罩表示不可用)
        if self.system.state == "IDLE":
            if self.current_menu == "MAIN":
                self.ui.draw_menu_grid(self.main_options, self.selected_index, self.player.theme_color)
            elif self.current_menu == "SKILL":
                self.ui.draw_skill_menu_grid(self.player, self.selected_index)
            
            # 如果是等待怪物状态，可以在菜单上画一个淡淡的锁定层 (可选)
            if self.is_waiting_for_enemy:
                pass

        if self.system.state == "WIN":
            UIConfig.draw_center_text(self.screen, UIConfig.render_text("胜利！(按回车键返回)", "title", (255, 215, 0)), sh // 2)
        elif self.system.state == "LOSS":
            UIConfig.draw_center_text(self.screen, UIConfig.render_text("战败...", "title", (255, 50, 50)), sh // 2)

        self.ui.update_and_draw_effects()