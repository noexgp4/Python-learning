from .skills_library import SKILLS_LIB

_BASE_SPRITE_CONFIG = {
    "frame_size": (16, 24),  # 原始尺寸
    "cols": 4,               # 4 帧动画
    "rows": 8,               # 4 个方向（下、左、右、上）
    "render_size": (32, 48), # 缩放后的渲染尺寸（保持比例）
}
# 职业数据定义
_WARRIOR = {
    **_BASE_SPRITE_CONFIG,
    "name": "学生",
    "desc": "坚韧的前线战士，擅长近战物理攻击。",
    "hp": 200,
    "mp": 50,
    "atk": 25,
    "m_atk": 0,
    "def": 15,
    "spd": 8,
    "skills": ["basic_slash", "heavy_strike"],
    "sprite_path": "Assets/Image/Characters/character.png", 
    "sprite_index": 0,
    "world_speed": 100,
    "theme_color": (200, 120, 100)
}

_MAGE = {
    **_BASE_SPRITE_CONFIG,
    "name": "法师",
    "desc": "精通元素魔法，擅长范围与魔法伤害。",
    "hp": 100,
    "mp": 180,
    "atk": 5,
    "m_atk": 30,
    "def": 5,
    "spd": 10,
    "skills": ["fire_ball", "ice_shards"],
    "sprite_path": "Assets/Image/Characters/character.png", 
    "sprite_index": 1,
    "world_speed": 100,
    "theme_color": (100, 140, 220)
}

# 以英文 key 为主，同时支持中文别名（因为 GameState 使用中文职业名）
JOBS = {
    "Warrior": _WARRIOR,
    "Mage": _MAGE,
    # 中文别名映射
    "学生": _WARRIOR,
    "法师": _MAGE,
}

__all__ = ["JOBS"]