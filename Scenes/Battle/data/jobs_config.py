from .skills_library import SKILLS_LIB

JOBS = {
    "Warrior": {
        "name": "学生",
        "stats": {"hp": 200, "mp": 50, "atk": 25, "def": 15},
        "skills": ["basic_slash", "heavy_strike"] # 只存 ID
    },
    "Mage": {
        "name": "法师",
        "stats": {"hp": 100, "mp": 180, "atk": 5, "def": 5},
        "skills": ["fire_ball", "ice_shards"]
    }
      }