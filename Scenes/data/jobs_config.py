JOBS_DATA = {
    "学生": {
        "name": "学生",
        "hp": 120, "mp": 50, "atk": 15, "m_atk": 5, "def": 12, "spd": 10,
        "desc": "高生命值，擅长近战",
        "theme_color": (200, 50, 50),
        "sprite_index": 0,
        "skills": [
            {"name": "奋力一击", "cost": 10, "type": "PHYSIC", "power": 25},
            {"name": "读书笔记", "cost": 20, "type": "MAGIC", "power": 15}
        ]
    },
    "上班族": {
        "name": "上班族",
        "hp": 80, "mp": 100, "atk": 10, "m_atk": 30, "def": 6, "spd": 15,
        "desc": "脆皮但魔法伤害极高",
        "theme_color": (50, 100, 255),
        "sprite_index": 1,
        "skills": [
            {"name": "午休充电", "cost": 30, "type": "MAGIC", "power": 50},
            {"name": "报表攻击", "cost": 15, "type": "MAGIC", "power": 30}
        ]
    },
    "程序员": {
        "name": "程序员",
        "hp": 95, "mp": 120, "atk": 12, "m_atk": 20, "def": 8, "spd": 12,
        "desc": "高暴击，身手敏捷",
        "theme_color": (50, 200, 50),
        "sprite_index": 0,
        "skills": [
            {"name": "编写Bug", "cost": 25, "type": "MAGIC", "power": 45},
            {"name": "修复Bug", "cost": 15, "type": "MAGIC", "power": 35}
        ]
    },
    "Mage": {
        "name": "法师",
        "hp": 80, "mp": 150, "atk": 5, "m_atk": 25, "def": 5, "spd": 8,
        "desc": "掌控元素的奥秘",
        "theme_color": (100, 150, 255),
        "sprite_index": 1,
        "skills": [
            {"name": "火球术", "cost": 20, "type": "FIRE", "power": 40},
            {"name": "奥术冲击", "cost": 40, "type": "MAGIC", "power": 70}
        ]
    },
    "Warrior": {
        "name": "战士",
        "hp": 150, "mp": 40, "atk": 20, "m_atk": 0, "def": 15, "spd": 6,
        "desc": "钢铁般的意志与躯体",
        "theme_color": (255, 100, 100),
        "sprite_index": 0,
        "skills": [
            {"name": "重劈", "cost": 0, "type": "PHYSIC", "power": 30},
            {"name": "旋风斩", "cost": 15, "type": "PHYSIC", "power": 50}
        ]
    }
}