MONSTERS_DATA = {
    "Slime_Green": {
        "name": "绿史莱姆",
        "hp": 60,
        "mp": 0,
        "atk": 12,
        "def": 5,
        "skills": ["basic_slash"],
        "ai": "random",
        "image_key": "slime_green"
    },
    "Skeleton_Mage": {
        "name": "骷髅法师",
        "hp": 120,
        "mp": 100,
        "atk": 5,
        "def": 2,
        "ai": "cautious",
        "skills": ["shadow_bolt"],
        "image_key": "skeleton_mage"
    }
}

ENEMY_GROUPS = {
    "Slime_Green": {
        "name": "一群史莱姆",
        "bg_image": "Assets/Image/Battle/forest_bg.png", # 战斗背景图
        "enemies": [
            {"id": "Slime_Green", "pos": (100, 200)}, # 史莱姆 A
            {"id": "Slime_Green", "pos": (150, 250)}, # 史莱姆 B
            {"id": "Skeleton_Mage",    "pos": (200, 150)}, # 混入一只小蝙蝠
        ]
    },
    "Skeleton_Mage": {
        "name": "骷髅法师",
        "bg_image": "Assets/Image/Battle/cave_bg.png",
        "enemies": [
            {"id": "Skeleton_Mage", "pos": (200, 150)},
            {"id": "Slime_Green", "pos": (100, 200)},
            {"id": "Skeleton_Mage", "pos": (300, 200)},
        ]
    }
}
__all__ = ["MONSTERS_DATA", "ENEMY_GROUPS"]
