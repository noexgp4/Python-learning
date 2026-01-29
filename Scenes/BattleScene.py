import pygame 

class BattleScene:
    def __init__(self, player, enemy):
        self.system = BattleSystem(player, enemy) # 导入之前的逻辑类
        self.ui = BattleUI(screen, UIConfig)      # 导入 UI 类
        
        # 初始化显示血量
        self.ui.player_display_hp = player.hp
        self.ui.enemy_display_hp = enemy.hp

    def update(self, events):
        # 1. 监控逻辑层产生的“结果”
        old_hp = self.system.enemy.hp
        self.system.update() # 逻辑运行
        
        # 2. 如果敌人掉血了，告诉 UI 弹数字
        if self.system.action_result.get("damage") and self.system.state == "CHECK_DEATH":
            res = self.system.action_result
            self.ui.trigger_damage_num(res['damage'], (1300, 300)) # 怪物坐标
            self.system.action_result = {} # 清空结果，防止重复触发

    def draw(self, screen):
        # 1. 画背景和人物立绘
        # ... 
        
        # 2. 画 UI
        self.ui.player_display_hp = self.ui.draw_stat_bar(
            150, 850, 300, 25, self.system.player.hp, self.system.player.max_hp, 
            self.ui.player_display_hp, (50, 200, 50)
        )
        
        self.ui.enemy_display_hp = self.ui.draw_stat_bar(
            1300, 250, 250, 20, self.system.enemy.hp, self.system.enemy.max_hp, 
            self.ui.enemy_display_hp, (200, 50, 50)
        )
        
        # 3. 画菜单和特效
        if self.system.state == "IDLE":
            self.ui.draw_menu(["攻击", "技能", "防御", "逃跑"], self.selected_index)
            
        self.ui.update_and_draw_effects()