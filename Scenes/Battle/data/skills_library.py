from .constants import *

# --- 技能模板 (Templates) ---
BASE_PHYSIC = {"type": TYPE_PHYSIC, "color": C_RED, "cost": 10}
BASE_MAGIC  = {"type": TYPE_MAGIC, "color": C_BLUE, "cost": 25}

# --- 核心技能库 (字典) ---
SKILLS_LIB = {
    # --主动技能--
    "aim": {
        "id": "aim",
        "name": "狙击",
        "cost": 1,
        "power": 20,
        "cooldown": 2,
        "duration": 4,
        "desc": "瞄准单个目标,每回合增加100%暴击伤害，最多四回合，结束时造成暴击伤害"
    },
    "shotgun": {
        "id": "shotgun",
        "name": "霰弹枪",
        "cost": 1,
        "power": 20,
        "cooldown": 0,
        "desc": "射击目标弹射到后方玩家,后方玩家受到20%伤害,消耗1子弹"
    },
    "Revolver": {
        "id": "Revolver",
        "name": "左轮",
        "cost": 2,
        "power": 20,
        "cooldown": 0,
        "desc": "对最近的随机目标进行两次快速射击,消耗2子弹"
    },
    "Loading": {
        "id": "Loading",
        "name": "装填",        
        "cost": 0,
        "power": 0,
        "cooldown": 0,
        "desc": "装填子弹"
    },
    "Hawkeye": {
        "id": "Hawkeye",
        "name": "鹰眼",
        "cost": 5,
        "power": 0,
        "cooldown": 3,
        "duration": 3,
        "desc": "进入鹰眼状态持续3回合,并可以查看到目标怪物的血量状态。"
    },
    "magic_absorb": {
        "id": "magic_absorb",
        "name": "魔法吸收",
        "cost": 0,
        "power": 0,
        "cooldown": 0,
        "desc": "吸收目标100点魔法值,没有魔法值时造成伤害"
    },
    
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
        "desc": "对单体造成重击，有几率眩晕。"
    },
    "fire_ball": {
        **BASE_MAGIC,
        "id": "fire_ball",
        "name": "火球术",
        "power": 40,
        "effects": [{"id": "BURN", "chance": 0.5}],
        "desc": "对多个目标释放8颗火球,8颗按目标人数分摊数量"
    },
    "drain_magic": {
        **BASE_MAGIC,
        "id": "drain_magic",
        "name": "吸取魔法",
        "power": 20,
        "effects": [{"id": "DRAIN_MAGIC", "chance": 0.5}],
        "desc": "吸取目标一定比例的魔法值，没有魔法值时转为造成伤害"
    },
    "ice_shards": { 
        **BASE_MAGIC,
        "id": "ice_shards",
        "name": "寒冰箭",
        "power": 30,
        "effects": [{"id": "FREEZE", "chance": 0.4}],
        "desc": "对多个目标释放8颗寒冰箭,8颗按目标人数分摊数量"
    },
    # --被动技能--
    "greedy": {
        "id": "greedy",
        "name": "贪婪",
        "desc": "释放技能时有10%的概率重复释放3次"
    },
    "bleed": {
        "id": "bleed",
        "name": "流血",
        "desc": "受到伤害时，有几率造成流血。"
    },
    "stun": {
        "id": "stun",
        "name": "眩晕",
        "desc": "受到伤害时，有几率眩晕。"
    },
    "burn": {
        "id": "burn",
        "name": "燃烧",
        "desc": "受到伤害时，有几率燃烧。"
    },
    "freeze": {
        "id": "freeze",
        "name": "冻结",
        "desc": "受到伤害时，有几率冻结。"
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