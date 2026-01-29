import pygame

class BattleSystem:
    def __init__(self, player, enemy):
        self.player = player  # 角色對象，包含 hp, atk, def, spd 等
        self.enemy = enemy    # 怪物對象
        
        # 初始狀態
        self.state = "IDLE"
        self.current_turn = "PLAYER" if player.spd >= enemy.spd else "ENEMY"
        self.battle_log = "戰鬥開始！"
        self.action_result = {} # 存放當前動作的結果（如傷害值、是否暴擊）

    def update(self):
        """每幀被 Scene 呼叫，處理不需要玩家操作的狀態"""
        if self.state == "ENEMY_THINKING":
            self.execute_enemy_ai()
        elif self.state == "CHECK_DEATH":
            self.check_battle_status()

    def handle_player_input(self, action_type, skill=None):
        """當玩家在 UI 點擊按鈕時觸發"""
        if self.state != "IDLE" or self.current_turn != "PLAYER":
            return

        if action_type == "ATTACK":
            self.execute_attack(self.player, self.enemy)
        elif action_type == "SKILL":
            self.execute_skill(self.player, self.enemy, skill)

    def execute_attack(self, attacker, target):
        """核心傷害公式"""
        # 簡單公式：傷害 = 攻擊力 - (防禦力 / 2)
        damage = max(1, attacker.atk - (target.def_val // 2))
        target.hp -= damage
        
        # 記錄結果，供 UI 層讀取來顯示動畫（如飄字）
        self.action_result = {
            "attacker": attacker,
            "target": target,
            "damage": damage,
            "type": "NORMAL_HIT"
        }
        
        self.battle_log = f"{attacker.name} 發起攻擊，造成 {damage} 點傷害！"
        self.state = "CHECK_DEATH"

    def execute_enemy_ai(self):
        """敵人的簡易 AI"""
        # 這裡可以加入延時邏輯，或者直接執行攻擊
        self.execute_attack(self.enemy, self.player)
        self.state = "CHECK_DEATH"

    def check_battle_status(self):
        """檢查勝負並切換回合"""
        if self.enemy.hp <= 0:
            self.enemy.hp = 0
            self.state = "WIN"
        elif self.player.hp <= 0:
            self.player.hp = 0
            self.state = "LOSS"
        else:
            # 切換回合
            if self.current_turn == "PLAYER":
                self.current_turn = "ENEMY"
                self.state = "ENEMY_THINKING"
            else:
                self.current_turn = "PLAYER"
                self.state = "IDLE"