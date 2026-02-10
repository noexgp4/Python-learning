# Scenes/Battle/data/enemy_groups.py

ENEMY_GROUPS = {
    "forest_slime": {
        "name": "一群史莱姆",
        "bg_image": "Assets/Image/Battle/forest_bg.png", # 战斗背景图
        "enemies": [
            {"id": "slime_green", "pos": (100, 200)}, # 史莱姆 A
            {"id": "slime_green", "pos": (150, 250)}, # 史莱姆 B
            {"id": "bat_blue",    "pos": (200, 150)}, # 混入一只小蝙蝠
        ]
    },
    "boss_dragon": {
        "name": "恶龙巢穴",
        "bg_image": "Assets/Image/Battle/cave_bg.png",
        "enemies": [
            {"id": "red_dragon", "pos": (300, 200)}
        ]
    }
}