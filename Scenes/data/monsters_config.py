MONSTERS_DATA = {
    "Slime_Green": {
        "name": "绿史莱姆",
        "hp": 50, "mp": 0, "atk": 10, "def": 5, "spd": 5,
        "exp": 20, "gold": 10,
        "image_key": "slime_g", # 对应加载哪张立绘
        "ai_type": "AGGRESSIVE", # 攻击型 AI
        "skills": [
            {"name": "撞击", "type": "PHYSIC", "power": 10}
        ]
    },
    "Skeleton_Mage": {
        "name": "骷髅法师",
        "hp": 120, "mp": 100, "atk": 5, "def": 2, "spd": 12,
        "exp": 150, "gold": 80,
        "image_key": "sk_mage",
        "ai_type": "CAUTIOUS", # 血少会加血的 AI
        "skills": [
            {"name": "暗影箭", "type": "MAGIC", "power": 25, "cost": 15}
        ]
    }
}