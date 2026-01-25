import json
import os
import time
from .game_state import GameState

class SaveManager:
    def __init__(self):
        # 存档目录放在项目根目录下的 Saves 文件夹
        self.save_dir = os.path.join(os.path.dirname(__file__), "..", "Saves")
        self._ensure_save_dir()
        
    def _ensure_save_dir(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            
    def get_save_path(self, slot_id):
        return os.path.join(self.save_dir, f"save_{slot_id}.json")
    
    def save_game(self, game_state: GameState, slot_id: int):
        """保存游戏状态到指定槽位"""
        try:
            data = game_state.to_dict()
            # 添加元数据
            save_data = {
                "timestamp": time.time(),
                "time_str": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "data": data
            }
            
            with open(self.get_save_path(slot_id), 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            print(f"存档成功: 槽位 {slot_id}")
            return True
        except Exception as e:
            print(f"存档失败: {e}")
            return False
            
    def load_game(self, slot_id: int) -> GameState:
        """从指定槽位加载游戏"""
        path = self.get_save_path(slot_id)
        if not os.path.exists(path):
            print(f"存档文件不存在: {path}")
            return None
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
                
            game_state = GameState()
            game_state.load_from_dict(save_data["data"])
            print(f"读档成功: 槽位 {slot_id} ({save_data.get('time_str')})")
            return game_state
        except Exception as e:
            print(f"读档失败: {e}")
            return None

    def get_save_slots_info(self):
        """获取所有存档槽位的简要信息"""
        info = {} # slot_id -> info dict
        for filename in os.listdir(self.save_dir):
            if filename.startswith("save_") and filename.endswith(".json"):
                try:
                    slot_id = int(filename.split("_")[1].split(".")[0])
                    path = os.path.join(self.save_dir, filename)
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        info[slot_id] = {
                            "time": data.get("time_str", "Unknown"),
                            "level": data["data"].get("level", 1)
                        }
                except:
                    continue
        return info
