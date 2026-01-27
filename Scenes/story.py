import pygame
import json
import os
from Scenes.text import UIConfig, Label, Panel, ImageComponent
from Scenes.UIManager import UIManager

class StoryScene:
    def __init__(self, screen, job_name):
        self.screen = screen
        self.job = job_name
        self.full_text = self._load_json_data("story.json", "intro")
        self.language_manager = getattr(pygame, 'language_manager', None) # 尝试获取全局语言管理器
        self.ui_manager = UIManager(self.screen)
        
        # 统一管理图片路径和映射
        self.illustrations = self._load_assets("Assets/Image/Illustrations", ["elder.png", "intro_boss.png"])
        self.line_to_image = {0: "intro_boss.png", 1: "elder.png"}
            
        self.current_line = 0
        self.display_char_count = 0  

    def _load_json_data(self, filename, key):
        """合并数据加载逻辑"""
        try:
            path = os.path.join(os.path.dirname(__file__), filename)
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f).get(key, [])
        except Exception as e:
            print(f"加载{filename}失败: {e}")
            return ["故事开始于迷雾之中...", "勇者 {job} 踏上了旅程。"]

    def _load_assets(self, base_path, names):
        """合并资源加载逻辑，减少 try-except 碎块"""
        assets = {}
        for name in names:
            path = os.path.join(base_path, name)
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    assets[name] = pygame.transform.scale(img, (400, 400))
                except pygame.error:
                    print(f"无法解析图片: {name}")
        return assets

    def draw(self):
        if not self.full_text: return
        self.screen.fill((0, 0, 0))
        self.ui_manager.clear()
        
        # 1. 插画显示逻辑
        img_name = self.line_to_image.get(self.current_line, "elder.png")
        active_img = self.illustrations.get(img_name)
        if active_img:
            # 使用 ImageComponent
            ix = self.screen.get_width() // 2 - 200
            iy = 20
            self.ui_manager.add_component(Panel(ix - 2, iy - 2, 404, 404, (0,0,0,0), (180, 150, 50), 2, 0))
            self.ui_manager.add_component(ImageComponent(ix, iy, active_img))

        # 2. 绘制下方文本区域
        current_full_text = self.full_text[self.current_line].replace("{job}", self.job)
        
        if self.display_char_count < len(current_full_text):
            self.display_char_count += 0.5
            
        visible_text = current_full_text[:int(self.display_char_count)]
        lines = self._wrap_text(visible_text, UIConfig.NORMAL_FONT, 700)

        # 文本框区域面板
        box_width, box_height = 760, 280
        box_x = (self.screen.get_width() - box_width) // 2
        box_y = 430
        self.ui_manager.add_component(Panel(box_x, box_y, box_width, box_height, (20, 20, 20, 180), (180, 150, 50, 255), 2, 15))
        
        # 文本渲染
        text_y_start = box_y + 30
        for i, line in enumerate(lines):
            lx = (self.screen.get_width() - UIConfig.NORMAL_FONT.size(line)[0]) // 2
            self.ui_manager.add_component(Label(lx, text_y_start + i * 40, line, "normal", (220, 220, 220)))

        # 3. 提示语
        if self.display_char_count >= len(current_full_text):
            # 优先从多语言管理器获取，否则使用默认值
            hint_text = "按下 空格键 继续..."
            if self.language_manager:
                hint_text = self.language_manager.get_text("prompt", "continue")
                
            hw = UIConfig.SMALL_FONT.size(hint_text)[0]
            self.ui_manager.add_component(Label(self.screen.get_width() - hw - 40, self.screen.get_height() - 40, hint_text, "small", (150, 150, 150)))

        self.ui_manager.draw()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            current_full_text = self.full_text[self.current_line].replace("{job}", self.job)
            
            # 合并逻辑：如果没播完则跳过，播完了则下一页
            if self.display_char_count < len(current_full_text):
                self.display_char_count = len(current_full_text)
            else:
                self.current_line += 1
                self.display_char_count = 0
                if self.current_line >= len(self.full_text):
                    return "BATTLE"
        return None

    def _wrap_text(self, text, font, max_width):
        """保持现状，这个辅助方法很清晰"""
        lines, current_line = [], ""
        for char in text:
            if font.size(current_line + char)[0] <= max_width:
                current_line += char
            else:
                lines.append(current_line)
                current_line = char
        lines.append(current_line)
        return lines