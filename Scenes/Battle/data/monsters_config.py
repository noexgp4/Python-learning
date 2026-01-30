MONSTERS_DATA = {
    "Slime": {
        "name": "绿史莱姆",
        "stats": {"hp": 60, "mp": 0, "atk": 12, "def": 5},
        "skills": ["basic_slash"], # 怪物也可以用玩家的技能！
        "ai": "random"
    },
    "Skeleton": {
        "name": "骷髅法师",
        "stats": {"hp": 120, "mp": 100, "atk": 5, "def": 2},
        "ai": "cautious", # 血少会加血的 AI
        "skills": ["shadow_bolt"]
    }
}
