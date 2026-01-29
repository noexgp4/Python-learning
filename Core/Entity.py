# 玩家类中的法师实例数据示例
mage_data = {
    "job": "法师",
    "hp": 80,
    "max_hp": 80,
    "mp": 120,
    "max_mp": 120,
    "atk": 5,   # 物理攻击很弱
    "m_atk": 25, # 魔法攻击很强
    "skills": [
        {"name": "小火球", "cost": 15, "damage": 40, "effect": "burn"},
        {"name": "寒冰箭", "cost": 20, "damage": 35, "effect": "slow"},
        {"name": "奥术爆发", "cost": 50, "damage": 80, "effect": "none"}
    ]
}