import json
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
monsters_json_path = os.path.join(current_dir, "monsters.json")

# 默认数据，防止加载失败
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
    }
}

# 尝试从 JSON 加载
if os.path.exists(monsters_json_path):
    try:
        with open(monsters_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data:
                MONSTERS_DATA = data
    except Exception as e:
        print(f"[Error] Failed to load monsters.json: {e}")


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
