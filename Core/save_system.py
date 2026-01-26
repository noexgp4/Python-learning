import json
import os
import time
from .game_state import GameState
from Scenes.text import UIConfig, ProgressBar  # 导入 UI 配置和控件
import pygame

class SaveManager:
    def __init__(self, screen):
        self.screen = screen
        self.selected_index = 0
        self.slots = [1, 2, 3] # 三个槽位
        self.slot_data = []
        
        # 存档目录设置
        self.save_dir = os.path.join(os.path.dirname(__file__), "..", "Saves")
        self._ensure_save_dir()
        
        self.refresh_slots() # 初始化时加载一次数据
    def refresh_slots(self):
        """读取本地文件夹，查看哪些槽位有存档"""
        self.slot_data = []
        for i in self.slots:
            path = f"Saves/save_{i}.json"
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    self.slot_data.append(json.load(f))
            else:
                self.slot_data.append(None) # None 代表空档位  
    def draw(self):
        """绘制存档界面"""
        self.screen.fill(UIConfig.COLOR_BG) # 填充背景
        
        # 绘制标题
        title_text = "选择存档"
        title_surf = UIConfig.render_text(title_text, "title", UIConfig.COLOR_WHITE)
        self.screen.blit(title_surf, (50, 50))
        
        # 绘制三个存档槽位
        for i, data in enumerate(self.slot_data):
            x = 50
            y = 150 + i * 120
            
            if data:
                # 有存档的情况
                # 显示时间
                time_text = data.get("time_str", "Unknown Time")
                time_surf = UIConfig.render_text(time_text, "normal", UIConfig.COLOR_WHITE)
                self.screen.blit(time_surf, (x, y))
                
                # 显示等级
                level_text = f"Lv. {data['data'].get('level', 1)}"
                level_surf = UIConfig.render_text(level_text, "normal", UIConfig.COLOR_YELLOW)
                self.screen.blit(level_surf, (x, y + 40))
                
                # 绘制进度条 (可选，这里简单显示)
                progress_bar = ProgressBar(x, y + 80, 300, 20, 0.8, self.selected_index == i)
                progress_bar.draw(self.screen)
            else:
                # 空档位的情况
                empty_text = "空档"
                empty_surf = UIConfig.render_text(empty_text, "normal", UIConfig.COLOR_GRAY)
                self.screen.blit(empty_surf, (x, y))
                
                # 绘制空进度条
                progress_bar = ProgressBar(x, y + 40, 300, 20, 0, self.selected_index == i)
                progress_bar.draw(self.screen)
                
        pygame.display.flip()

    def update_selection(self, direction):
        """更新选中项"""
        self.selected_index = (self.selected_index + direction) % len(self.slots)
        
    def get_selected_slot(self):
        """获取当前选中的槽位ID"""
        return self.slots[self.selected_index]             
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
