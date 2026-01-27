import json
import os
import time
from .game_state import GameState
from .game_config import CLASSES
from Scenes.text import UIConfig, ProgressBar, Panel, Label, ImageComponent  # 导入 UI 配置和控件
from Scenes.UIManager import UIManager
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
        
        self.ui_manager = UIManager(self.screen)
        
        # 加载职业预览图
        self.sprites = {}
        try:
            sprite_path = os.path.join(os.path.dirname(__file__), "..", "Assets", "Image", "character_sprites.png")
            if os.path.exists(sprite_path):
                sheet = pygame.image.load(sprite_path).convert_alpha()
                for i in range(2): # 假设目前只有两个基础造型
                    rect = pygame.Rect(i * 32, 0, 32, 32)
                    sprite = sheet.subsurface(rect)
                    # 缩放到适合存档槽位的高度 (约 80x80)
                    self.sprites[i] = pygame.transform.scale(sprite, (80, 80))
        except Exception as e:
            print(f"存档界面加载雪碧图失败: {e}")
            
        self.refresh_slots() # 初始化时加载一次数据
    def refresh_slots(self):
        """读取本地文件夹，查看哪些槽位有存档"""
        self.slot_data = []
        for i in self.slots:
            path = self.get_save_path(i)
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        self.slot_data.append(json.load(f))
                except Exception as e:
                    print(f"解析存档失败 {path}: {e}")
                    self.slot_data.append(None)
            else:
                self.slot_data.append(None) # None 代表空档位  
    def draw(self):
        """绘制存档界面"""
        sw, sh = self.screen.get_size()
        self.screen.fill(UIConfig.COLOR_BG) # 填充背景
        self.ui_manager.clear()
        
        # 绘制标题
        self.ui_manager.add_component(Label(50, 50, "选择存档", "title", UIConfig.COLOR_WHITE))
        
        # 绘制三个存档槽位
        margin_x = 40  # 左右间距
        slot_w = sw - (margin_x * 2)
        slot_h = 120
        
        for i, data in enumerate(self.slot_data):
            x = margin_x
            y = 150 + i * (slot_h + 20)
            is_selected = (self.selected_index == i)
            
            # 1. 容器面板
            border_color = UIConfig.COLOR_BORDER_HIGHLIGHT if is_selected else UIConfig.COLOR_BAR_BORDER
            # 统一使用配置中的全黄色
            bg_color = (*UIConfig.COLOR_YELLOW, 255) if is_selected else UIConfig.COLOR_PANEL_BG
            self.ui_manager.add_component(Panel(x, y, slot_w, slot_h, bg_color, border_color, 3, 10))
            
            # 2. 内容
            px, py = x + 30, y + (slot_h - 32) // 2
            content_text_color = UIConfig.COLOR_PALETTE_BLACK if is_selected else UIConfig.COLOR_WHITE
            level_text_color = UIConfig.COLOR_PALETTE_BLACK if is_selected else UIConfig.COLOR_YELLOW
            
            # 右侧职业预览图区域
            img_size = 90
            ix = x + slot_w - img_size - 20
            iy = y + (slot_h - img_size) // 2
            
            if data:
                time_text = data.get("time_str", "Unknown Time")
                self.ui_manager.add_component(Label(px, py, time_text, "normal", content_text_color))
                
                level_text = f"Lv. {data['data'].get('level', 1)}"
                # 等级放在中间靠右
                self.ui_manager.add_component(Label(x + slot_w // 2 + 50, py + 5, level_text, "normal", level_text_color))
                
                # 绘制职业图片
                job_name = data['data'].get("job_name", "勇者")
                if job_name in CLASSES:
                    sprite_idx = CLASSES[job_name]["sprite_index"]
                    if sprite_idx in self.sprites:
                        char_img = self.sprites[sprite_idx]
                        # 镜像逻辑（程序员翻转）
                        if job_name == "程序员" and sprite_idx == 0:
                            char_img = pygame.transform.flip(char_img, True, False)
                        
                        # 绘制预览图背景框（可选，增加层次感）
                        inner_bg = (0,0,0,50) if not is_selected else (255,255,255,50)
                        self.ui_manager.add_component(Panel(ix-5, iy-5, img_size+10, img_size+10, inner_bg, border_radius=5))
                        self.ui_manager.add_component(ImageComponent(ix, iy, char_img))
            else:
                empty_text_color = UIConfig.COLOR_PALETTE_BLACK if is_selected else UIConfig.COLOR_GRAY
                self.ui_manager.add_component(Label(px, py + 15, f"槽位 {i+1}: 空档", "normal", empty_text_color))
                
                # 绘制空框
                frame_color = (0,0,0,60) if not is_selected else (255,255,255,80)
                self.ui_manager.add_component(Panel(ix, iy, img_size, img_size, frame_color, UIConfig.COLOR_BAR_BORDER, 1, 5))
        
        # 3. 操作提示
        tip_text = "Enter: 选择/创建  ESC: 返回  Del: 删除存档"
        tw = UIConfig.SMALL_FONT.size(tip_text)[0]
        self.ui_manager.add_component(Label(
            sw // 2 - tw // 2, 
            sh - 40, 
            tip_text, 
            "small", 
            UIConfig.COLOR_GRAY_LIGHT
        ))
        
        self.ui_manager.draw()

    def delete_save(self, slot_index):
        """删除指定索引的存档"""
        slot_id = self.slots[slot_index]
        path = self.get_save_path(slot_id)
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"存档已删除: 槽位 {slot_id}")
                self.refresh_slots()
                return True
            except Exception as e:
                print(f"删除存档失败: {e}")
        return False

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
