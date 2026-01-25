class GameState:
    def __init__(self):
        # 基础玩家属性
        self.player_hp = 100
        self.max_hp = 100
        self.level = 1
        self.exp = 0
        self.gold = 0
        
        # 战斗属性
        self.attack = 10
        self.defense = 5
        
        # 进度记录
        self.current_scene = "Battle" 
        self.unlocked_stages = [1]
        
        # 物品/装备
        self.inventory = [] 
        
    def to_dict(self):
        """序列化为字典"""
        return {
            "player_hp": self.player_hp,
            "max_hp": self.max_hp,
            "level": self.level,
            "exp": self.exp,
            "gold": self.gold,
            "attack": self.attack,
            "defense": self.defense,
            "current_scene": self.current_scene,
            "unlocked_stages": self.unlocked_stages,
            "inventory": self.inventory
        }
    
    def load_from_dict(self, data):
        """从字典加载数据"""
        self.player_hp = data.get("player_hp", 100)
        self.max_hp = data.get("max_hp", 100)
        self.level = data.get("level", 1)
        self.exp = data.get("exp", 0)
        self.gold = data.get("gold", 0)
        self.attack = data.get("attack", 10)
        self.defense = data.get("defense", 5)
        self.current_scene = data.get("current_scene", "Battle")
        self.unlocked_stages = data.get("unlocked_stages", [1])
        self.inventory = data.get("inventory", [])
