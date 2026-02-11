from ..data.jobs_config import JOBS as JOBS_DATA
from ..data.monsters_config import MONSTERS_DATA
from ..data.skills_library import SkillsLibrary

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
        
        # 技能处理:支持技能ID列表或完整技能对象列表
        skills_raw = data_dict.get("skills", [])
        self.skills = self._load_skills(skills_raw)
        
        self.theme_color = data_dict.get("theme_color", (200, 200, 200))
        
        # 怪物特有属性
        import random
        self.exp_reward = data_dict.get("exp", 0)
        self.exp_min = data_dict.get("exp_min", self.exp_reward)
        self.exp_max = data_dict.get("exp_max", self.exp_reward)
        
        self.gold_reward = data_dict.get("gold", 0)
        self.gold_min = data_dict.get("gold_min", self.gold_reward)
        self.gold_max = data_dict.get("gold_max", self.gold_reward)
        
        self.ai_type = data_dict.get("ai_type", "IDLE")
        self.image_key = data_dict.get("image_key", None)
        
        # 实时结算的 XP (在被击败时决定)
        self.final_exp = random.randint(self.exp_min, self.exp_max) if self.exp_max >= self.exp_min else 0
        self.final_gold = random.randint(self.gold_min, self.gold_max) if self.gold_max >= self.gold_min else 0
        
        # 状态效果
        self.status_effects = []
    
    def add_status(self, status_id):
        """为实体添加状态效果"""
        if status_id not in [s['id'] for s in self.status_effects]:
            # 这里可以扩展从状态库加载具体效果，目前简单记录ID
            self.status_effects.append({"id": status_id, "duration": 3})
            print(f"{self.name} 获得了状态: {status_id}")

    def _load_skills(self, skills_raw):
        """加载技能数据
        
        Args:
            skills_raw: 可以是技能ID列表 ['fireball', 'arcane_blast'] 
                       或完整技能对象列表 [{"name": "火球术", ...}]
        
        Returns:
            完整的技能对象列表
        """
        if not skills_raw:
            return []
        
        # 判断是技能ID还是完整对象
        first_skill = skills_raw[0]
        
        if isinstance(first_skill, str):
            # 技能ID列表,从技能库加载
            return SkillsLibrary.get_skills_by_ids(skills_raw)
        else:
            # 已经是完整对象,直接返回(向后兼容)
            return skills_raw

    @property
    def active_skills(self):
        """返回主动技能（即包含 cost 或 type 的技能）"""
        return [s for s in self.skills if "cost" in s or "type" in s]

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
