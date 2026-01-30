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

__all__ = ["MONSTERS_DATA"]
