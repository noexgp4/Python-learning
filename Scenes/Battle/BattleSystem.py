import pygame
import random

class BattleSystem:
   
    def __init__(self, player, enemy):
        self.player = player 
        self.enemy = enemy
        self.state = "IDLE"
        self.battle_log = "战斗开始！"
        self.action_result = {} 

    # 在 BattleSystem 类中修改或新增
    def execute_skill(self, attacker, target, skill):
        """
        取代原本简单的 hp -= damage 逻辑
        支持多段命中、吸取和状态添加
        """
        skill_id = skill.get("id")
        results = []
    
        # 1. 处理“贪婪”被动：决定施放次数
        repeat_times = 3 if (any(s['id'] == "greedy" for s in attacker.skills) and random.random() < 0.1) else 1
    
        for _ in range(repeat_times):
            # 2. 处理分摊逻辑 (针对 fire_ball, ice_shards)
            hits = 1
            if skill_id in ["fire_ball", "ice_shards"]:
                hits = 8  # 这里假设只有1个敌人，所以吃满8发；如果是群体战斗，则在此处除以目标数

            for h in range(hits):
                # 计算单次伤害
                damage = self.calculate_damage(attacker, target, skill)
                target.hp = max(0, target.hp - damage)
            
                # 记录结果（用于动画或日志）
                results.append(damage)

            # 3. 处理效果判定 (流血、眩晕等)
            for effect in skill.get("effects", []):
                if random.random() < effect["chance"]:
                    target.add_status(effect["id"])
            
            # 4. 处理特殊效果：吸取魔法 (drain_magic)
            if skill_id == "drain_magic":
                last_dmg = results[-1] if results else 0
                drain_val = int(last_dmg * 0.5) # 比如吸取伤害的50%
                attacker.mp = min(attacker.max_mp, attacker.mp + drain_val)

        return sum(results), len(results) # 返回总伤害和总命中次数

    def process_action(self, action_index):
        if self.state != "IDLE": return None

        attacker = self.player
        target = self.enemy

        # 技能/普攻 判定
        if action_index == -1:
            skill = {"name": "普通攻击", "type": "PHYSIC", "power": 0, "id": "basic_atk"}
        else:
            skill = attacker.active_skills[action_index]
            cost = skill.get('cost', 0)
            if attacker.mp < cost:
                self.battle_log = "魔法值不足！"
                return {"status": "FAILED"}
            attacker.mp -= cost
        
        # --- 调用新逻辑 ---
        total_dmg, total_hits = self.execute_skill(attacker, target, skill)
        # ------------------

        if skill["id"] == "basic_atk":
            self.battle_log = f"{attacker.job_name} 发起普通攻击，造成 {total_dmg} 伤害！"
        else:
            self.battle_log = f"{attacker.job_name} 使用 {skill['name']}，命中 {total_hits} 次，共造成 {total_dmg} 伤害！"
        
        self.action_result = {"status": "SUCCESS", "attacker": attacker, "target": target, "damage": total_dmg}
        self.state = "CHECK_DEATH"
        return self.action_result

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