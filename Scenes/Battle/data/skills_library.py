from .constants import *

# --- 技能模板 (Templates) ---
# 这样你改一个模板，所有关联技能都会变
BASE_PHYSIC = {"type": TYPE_PHYSIC, "color": C_RED, "cost": 10}
BASE_MAGIC  = {"type": TYPE_MAGIC, "color": C_BLUE, "cost": 25}

# --- 核心技能库 ---
SKILLS_LIB = {
    # 战士系
    "basic_slash": {
        **BASE_PHYSIC,
        "name": "基础斩击",
        "power": 20,
        "effects": [{"id": "BLEED", "chance": 0.3}],
        "desc": "简单的一击，概率造成流血。"
    },
    "heavy_strike": {
        **BASE_PHYSIC,
        "name": "重劈",
        "cost": 20, # 覆盖模板中的 10
        "power": 45,
        "effects": [{"id": "STUN", "chance": 0.1}],
    },
    
    # 法师系
    "fire_ball": {
        **BASE_MAGIC,
        "name": "火球术",
        "power": 40,
        "effects": [{"id": "BURN", "chance": 0.5}],
    },
    "ice_shards": {
        **BASE_MAGIC,
        "name": "寒冰箭",
        "power": 30,
        "effects": [{"id": "FREEZE", "chance": 0.4}],
    }
}