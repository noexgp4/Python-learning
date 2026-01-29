import pygame

class BattleSystem:
    def __init__(self, player, enemy):
        self.player = player 
        self.enemy = enemy
        self.state = "IDLE"
        self.battle_log = "战斗开始！"
        self.action_result = {} 

    def process_action(self, action_index):
        if self.state != "IDLE": return None

        if action_index == -1:
            # -1 约定为普通物理攻击
            damage = self.calculate_damage(self.player, self.enemy, {"type": "PHYSIC", "power": 0})
            self.enemy.hp = max(0, self.enemy.hp - damage)
            self.battle_log = f"{self.player.job_name} 发起普通攻击，造成 {damage} 伤害！"
            result = {"status": "SUCCESS", "attacker": self.player, "target": self.enemy, "damage": damage}
        else:
            # 技能攻击
            skill = self.player.skills[action_index]
            cost = skill.get('cost', 0)
            if self.player.mp < cost:
                self.battle_log = "魔法值不足！"
                return {"status": "FAILED"}
            
            self.player.mp -= cost
            damage = self.calculate_damage(self.player, self.enemy, skill)
            self.enemy.hp = max(0, self.enemy.hp - damage)
            self.battle_log = f"{self.player.job_name} 使用 {skill['name']}，造成 {damage} 伤害！"
            result = {"status": "SUCCESS", "attacker": self.player, "target": self.enemy, "damage": damage}

        self.action_result = result
        self.state = "CHECK_DEATH"
        return result

    def calculate_damage(self, attacker, target, skill):
        power = skill.get('power', 0)
        s_type = skill.get('type', 'PHYSIC')
        
        # 核心逻辑：物理攻击使用 atk，魔法使用 m_atk
        if s_type == "PHYSIC":
            damage = max(1, attacker.atk + power - target.def_val)
        else: # MAGIC, FIRE, etc.
            damage = max(1, attacker.m_atk + power - (target.def_val // 2))
        return int(damage)

    def execute_enemy_turn(self):
        if self.enemy.hp <= 0: return
        
        # 敌人随机选一个技能
        import random
        skill = random.choice(self.enemy.skills) if self.enemy.skills else {"name": "撞击", "type": "PHYSIC", "power": 5}
        
        damage = self.calculate_damage(self.enemy, self.player, skill)
        self.player.hp = max(0, self.player.hp - damage)
        self.battle_log = f"{self.enemy.name} 发动 {skill['name']}，造成 {damage} 伤害！"
        
        self.action_result = {"status": "SUCCESS", "attacker": self.enemy, "target": self.player, "damage": damage}
        self.state = "CHECK_DEATH"

    def update(self):
        if self.state == "CHECK_DEATH":
            if self.enemy.hp <= 0:
                self.state = "WIN"
            elif self.player.hp <= 0:
                self.state = "LOSS"
            else:
                self.state = "IDLE"