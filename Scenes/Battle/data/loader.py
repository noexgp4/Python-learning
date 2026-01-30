import os
from .skills_library import SKILLS_LIB

class Actor:
    def __init__(self, key, config_dict):
        data = config_dict[key]
        self.name = data["name"]
        
        # 装载数值
        s = data["stats"]
        self.hp = self.max_hp = s["hp"]
        self.mp = self.max_mp = s["mp"]
        self.atk = s["atk"]
        self.armor = s["def"]
        
        # 【核心】装载技能数据
        self.skills = []
        for s_id in data["skills"]:
            if s_id in SKILLS_LIB:
                # 复制一份，防止动态修改影响全局库
                skill_info = SKILLS_LIB[s_id].copy()
                self.skills.append(skill_info)