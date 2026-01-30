from .constants import *

# --- 技能模板 (Templates) ---
BASE_PHYSIC = {"type": TYPE_PHYSIC, "color": C_RED, "cost": 10}
BASE_MAGIC  = {"type": TYPE_MAGIC, "color": C_BLUE, "cost": 25}

# --- 核心技能库 (字典) ---
SKILLS_LIB = {
    "basic_slash": {
        **BASE_PHYSIC,
        "id": "basic_slash",
        "name": "基础斩击",
        "power": 20,
        "effects": [{"id": "BLEED", "chance": 0.3}],
        "desc": "简单的一击，概率造成流血。"
    },
    "heavy_strike": {
        **BASE_PHYSIC,
        "id": "heavy_strike",
        "name": "重劈",
        "cost": 20,
        "power": 45,
        "effects": [{"id": "STUN", "chance": 0.1}],
    },
    "fire_ball": {
        **BASE_MAGIC,
        "id": "fire_ball",
        "name": "火球术",
        "power": 40,
        "effects": [{"id": "BURN", "chance": 0.5}],
    },
    "ice_shards": {
        **BASE_MAGIC,
        "id": "ice_shards",
        "name": "寒冰箭",
        "power": 30,
        "effects": [{"id": "FREEZE", "chance": 0.4}],
    }
}


class SkillsLibrary:
    """兼容层：提供 `get_skills_by_ids` 等方法，供 `Entity` 使用。"""

    @staticmethod
    def get_skills_by_ids(ids):
        out = []
        for i in ids:
            if i in SKILLS_LIB:
                out.append(SKILLS_LIB[i])
        return out

    @staticmethod
    def get_skill(id_):
        return SKILLS_LIB.get(id_)

__all__ = ["SKILLS_LIB", "SkillsLibrary"]