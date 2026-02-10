import pygame
import random

class BattleSystem:
   
    def __init__(self, player, enemies):
        self.player = player 
        self.enemies = enemies if isinstance(enemies, list) else [enemies]
        self.state = "IDLE"
        self.battle_log = "战斗开始！"
        self.action_result = {} 

    def execute_skill(self, attacker, target, skill):
        skill_id = skill.get("id")
        results = []
        
        # --- 狙击 (Aim) 逻辑 ---
        if skill_id == "aim":
            if not hasattr(attacker, "aim_charge"): attacker.aim_charge = 0
            if not hasattr(attacker, "aim_target"): attacker.aim_target = None

            # 首次发动：开始蓄力
            if attacker.aim_target != target or attacker.aim_charge == 0:
                attacker.aim_target = target
                attacker.aim_charge = 1
                self.battle_log = f"{attacker.job_name} 开始瞄准 {target.name}... (蓄力中)"
                return 0, 1 # 无伤害
            
            # 手动确认释放
            multiplier = 1.0 + (attacker.aim_charge * 1.0) # 2.0, 3.0, 4.0, 5.0
            damage = self.calculate_damage(attacker, target, skill) * multiplier
            target.hp = max(0, target.hp - int(damage))
            self.battle_log = f"{attacker.job_name} 蓄力结束！造成 {int(damage)} 毁灭伤害！"
            attacker.aim_charge = 0
            attacker.aim_target = None
            return int(damage), 1

        # --- 其他技能逻辑 ---
        repeat_times = 3 if (any(s['id'] == "greedy" for s in attacker.skills) and random.random() < 0.1) else 1
    
        for _ in range(repeat_times):
            hits = 1
            if skill_id in ["fire_ball", "ice_shards"]:
                hits = 8

            for h in range(hits):
                # 检查普通攻击是否享受狙击倍率
                final_multiplier = 1.0
                if skill_id == "basic_atk" and getattr(attacker, "aim_target", None) == target:
                    final_multiplier = 1.0 + getattr(attacker, "aim_charge", 0)
                    attacker.aim_charge = 0
                    attacker.aim_target = None
                
                damage = self.calculate_damage(attacker, target, skill) * final_multiplier
                target.hp = max(0, target.hp - int(damage))
                results.append(int(damage))

            # --- 霰弹枪 (Shotgun) 弹射逻辑 ---
            if skill_id == "shotgun":
                others = [e for e in self.enemies if e != target and e.hp > 0]
                if others:
                    bounce_dmg = int(results[-1] * 0.5)
                    for o in others:
                        o.hp = max(0, o.hp - bounce_dmg)
                    self.battle_log += f" 弹丸跳弹造成额外群体伤害！"

            for effect in skill.get("effects", []):
                if random.random() < effect["chance"]:
                    target.add_status(effect["id"])
            
            if skill_id == "drain_magic":
                last_dmg = results[-1] if results else 0
                drain_val = int(last_dmg * 0.5)
                attacker.mp = min(attacker.max_mp, attacker.mp + drain_val)

        return sum(results), len(results)

    def process_action(self, action_index, target_idx=0):
        if self.state != "IDLE": return None

        # 如果 target_idx 有效则使用，否则寻找活着的
        if target_idx < len(self.enemies):
            target = self.enemies[target_idx]
        else:
            target = next((e for e in self.enemies if e.hp > 0), None)
            
        if not target: return None

        attacker = self.player
        if action_index == -1:
            skill = {"name": "普通攻击", "type": "PHYSIC", "power": 0, "id": "basic_atk"}
        else:
            skill = attacker.active_skills[action_index]
            cost = skill.get('cost', 0)
            if attacker.mp < cost:
                self.battle_log = "魔法值不足！"
                return {"status": "FAILED"}
            attacker.mp -= cost
        
        # 在执行前，如果玩家正在蓄力但还没释放（且动作不是 aim/attack），
        # 我们可以在这里处理蓄力的自然增长（如果玩家选择“跳过”或执行其他非攻击动作）
        # 这里简单化：只有手动选狙击目标才增加倍率
        if skill["id"] == "aim" and getattr(attacker, "aim_target", None) == target:
            # 逻辑已在 execute_skill 处理
            pass
        elif hasattr(attacker, "aim_charge") and attacker.aim_charge > 0:
            # 如果蓄力中干了别的事，蓄力暂时保留还是中断？
            # 按照“瞄准”的逻辑，干别的事通常会中断
            # attacker.aim_charge = 0 
            pass

        total_dmg, total_hits = self.execute_skill(attacker, target, skill)

        # 仅当不是蓄力状态时更新 log
        if not (skill["id"] == "aim" and getattr(attacker, "aim_target", None) == target and total_dmg == 0):
            if skill["id"] == "basic_atk":
                self.battle_log = f"{attacker.job_name} 对 {target.name} 发起攻击，造成 {total_dmg} 伤害！"
            else:
                self.battle_log = f"{attacker.job_name} 使用 {skill['name']}，命中 {total_hits} 次，共造成 {total_dmg} 伤害！"
        
        # 如果是潜行瞄准后的释放，额外加一句
        if skill["id"] == "aim" and total_dmg > 0:
            self.battle_log = f"狙击穿透！对 {target.name} 造成 {total_dmg} 毁灭伤害！"

        self.action_result = {"status": "SUCCESS", "attacker": attacker, "target": target, "damage": total_dmg}
        self.state = "CHECK_DEATH"
        return self.action_result

    def calculate_damage(self, attacker, target, skill):
        power = skill.get('power', 0)
        s_type = skill.get('type', 'PHYSIC')
        if s_type == "PHYSIC":
            damage = max(1, attacker.atk + power - target.def_val)
        else:
            damage = max(1, attacker.m_atk + power - (target.def_val // 2))
        return int(damage)

    def execute_enemy_turn(self):
        alive_enemies = [e for e in self.enemies if e.hp > 0]
        if not alive_enemies: return

        logs = []
        total_dmg = 0
        for enemy in alive_enemies:
            skill = random.choice(enemy.skills) if enemy.skills else {"name": "撞击", "power": 5}
            damage = self.calculate_damage(enemy, self.player, skill)
            self.player.hp = max(0, self.player.hp - damage)
            logs.append(f"{enemy.name}攻击造成{damage}")
            total_dmg += damage
            if self.player.hp <= 0: break

        self.battle_log = " | ".join(logs)
        self.action_result = {"status": "SUCCESS", "attacker": alive_enemies[0], "target": self.player, "damage": total_dmg}
        self.state = "CHECK_DEATH"

    def update(self):
        if self.state == "CHECK_DEATH":
            if all(e.hp <= 0 for e in self.enemies):
                self.state = "WIN"
            elif self.player.hp <= 0:
                self.state = "LOSS"
            else:
                self.state = "IDLE"
