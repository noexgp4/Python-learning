class GameState:
    def __init__(self, job_name="勇者"):
        from Core.game_config import CLASSES
        # 基础玩家属性
        self.job_name = job_name
        
        # 获取职业配置
        config = CLASSES.get(job_name, {"hp": 100, "atk": 10, "def": 5, "spd": 10})
        
        self.player_hp = config.get("hp", 100)
        self.max_hp = config.get("hp", 100)
        self.player_mp = config.get("mp", 50)
        self.max_mp = config.get("mp", 50)
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.m_attack = config.get("m_atk", 0)
        
        # 战斗属性
        self.attack = config.get("atk", 10)
        self.defense = config.get("def", 5)
        self.spd = config.get("spd", 10)
        
        # 进度记录
        self.current_scene = "STORY" 
        self.current_map = "testmap.tmx" # 默认地图
        self.player_x = None  # None 表示使用地图默认出生点
        self.player_y = None
        self.unlocked_stages = [1]
        
        # 物品/装备
        self.inventory = [] 
        
    def to_dict(self):
        """序列化为字典"""
        return {
            "job_name": self.job_name,
            "player_hp": self.player_hp,
            "max_hp": self.max_hp,
            "player_mp": self.player_mp,
            "max_mp": self.max_mp,
            "level": self.level,
            "exp": self.exp,
            "gold": self.gold,
            "attack": self.attack,
            "m_attack": self.m_attack,
            "defense": self.defense,
            "spd": self.spd,
            "current_scene": self.current_scene,
            "current_map": self.current_map,
            "player_x": self.player_x,
            "player_y": self.player_y,
            "unlocked_stages": self.unlocked_stages,
            "inventory": self.inventory
        }
    
    def load_from_dict(self, data):
        """从字典加载数据"""
        self.job_name = data.get("job_name", "勇者")
        self.player_hp = data.get("player_hp", 100)
        self.max_hp = data.get("max_hp", 100)
        self.player_mp = data.get("player_mp", 50)
        self.max_mp = data.get("max_mp", 50)
        self.level = data.get("level", 1)
        self.exp = data.get("exp", 0)
        self.gold = data.get("gold", 0)
        self.attack = data.get("attack", 10)
        self.m_attack = data.get("m_attack", 0)
        self.defense = data.get("defense", 5)
        self.spd = data.get("spd", 10)
        self.current_scene = data.get("current_scene", "Battle")
        self.current_map = data.get("current_map", "testmap.tmx")
        self.player_x = data.get("player_x")
        self.player_y = data.get("player_y")
        self.unlocked_stages = data.get("unlocked_stages", [1])
        self.inventory = data.get("inventory", [])
