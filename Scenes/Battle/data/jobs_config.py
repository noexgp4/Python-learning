from .skills_library import SKILLS_LIB

# 以代码中期望的结构导出职业数据，便于直接映射到 `CLASSES`。
JOBS = {
    "Warrior": {
        "name": "学生",
        "desc": "坚韧的前线战士，擅长近战物理攻击。",
        "hp": 200,
        "mp": 50,
        "atk": 25,
        "m_atk": 0,
        "def": 15,
        "spd": 8,
        "skills": ["basic_slash", "heavy_strike"],
        "sprite_index": 0,
        "theme_color": (200, 120, 100)
    },
    "Mage": {
        "name": "法师",
        "desc": "精通元素魔法，擅长范围与魔法伤害。",
        "hp": 100,
        "mp": 180,
        "atk": 5,
        "m_atk": 30,
        "def": 5,
        "spd": 10,
        "skills": ["fire_ball", "ice_shards"],
        "sprite_index": 1,
        "theme_color": (100, 140, 220)
    }
}

__all__ = ["JOBS"]