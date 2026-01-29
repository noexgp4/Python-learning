from Scenes.data.jobs_config import JOBS_DATA
from Scenes.data.monsters_config import MONSTERS_DATA

class Entity:
    def __init__(self, data_dict):
        # 通用属性
        self.name = data_dict.get("name", "Unknown")
        self.job_name = data_dict.get("name", "Unknown") # 为了兼容 UI
        self.hp = self.max_hp = data_dict.get("hp", 100)
        self.mp = self.max_mp = data_dict.get("mp", 0)
        self.atk = data_dict.get("atk", 10)
        self.m_atk = data_dict.get("m_atk", 0)
        self.def_val = data_dict.get("def", 5)
        self.spd = data_dict.get("spd", 10)
        self.skills = data_dict.get("skills", [])
        self.theme_color = data_dict.get("theme_color", (200, 200, 200))
        
        # 怪物特有属性
        self.exp_reward = data_dict.get("exp", 0)
        self.gold_reward = data_dict.get("gold", 0)
        self.ai_type = data_dict.get("ai_type", "IDLE")
        self.image_key = data_dict.get("image_key", None)

    @classmethod
    def from_job(cls, job_key):
        if job_key in JOBS_DATA:
            return cls(JOBS_DATA[job_key])
        return None

    @classmethod
    def from_monster(cls, monster_key):
        if monster_key in MONSTERS_DATA:
            return cls(MONSTERS_DATA[monster_key])
        return None