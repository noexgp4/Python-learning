import pygame
from Scenes.text import UIConfig, Label, Panel, ImageComponent
from Scenes.UIManager import UIManager
from Scenes.data.jobs_config import JOBS_DATA

# 为了兼容旧代码，将 JOBS_DATA 映射到 CLASSES
CLASSES = JOBS_DATA

class ClassSelectScene:
    def __init__(self, screen):
        self.screen = screen
        self.class_names = list(CLASSES.keys())
        self.selected_index = 0
        self.ui_manager = UIManager(self.screen)
        
        # 加载雪碧图
        self.sprites = []
        try:
            # 优先尝试加载我们提取的 PNG，如果失败则静默处理
            sprite_path = "Assets/Image/character_sprites.png"
            sheet = pygame.image.load(sprite_path).convert_alpha()
            for i in range(2):
                rect = pygame.Rect(i * 32, 0, 32, 32)
                sprite = sheet.subsurface(rect)
                # 放大图片使其更清晰且符合大屏显示 (32x32 -> 256x256)
                self.sprites.append(pygame.transform.scale(sprite, (256, 256)))
        except Exception as e:
            print(f"加载职业雪碧图失败: {e}")

    def draw(self):
        # 填充深色背景
        self.screen.fill(getattr(UIConfig, 'COLOR_DARK_BG', (30, 30, 30)))
        self.ui_manager.clear()
        
        # 1. 标题 (Label 自动支持 render_text)
        title_text = "请选择你的初始职业"
        tw = UIConfig.TITLE_FONT.size(title_text)[0]
        self.ui_manager.add_component(Label((self.screen.get_width() - tw)//2, 50, title_text, "title", UIConfig.COLOR_YELLOW))

        # 定义布局
        LEFT_COLUMN_X = 100
        RIGHT_COLUMN_X = 450
        
        # 2. 左侧：职业列表与属性
        for i, name in enumerate(self.class_names):
            is_selected = (i == self.selected_index)
            # 注意：JOBS_DATA 中使用的是 theme_color，而不是之前的 color
            color = CLASSES[name].get("theme_color", (150, 150, 150)) if is_selected else (150, 150, 150)
            display_text = f"▶ {name}" if is_selected else f"  {name}"
            self.ui_manager.add_component(Label(LEFT_COLUMN_X, 200 + i * 60, display_text, "normal", color))

            if is_selected:
                info = CLASSES[name]
                self.ui_manager.add_component(Label(LEFT_COLUMN_X + 20, 520, info["desc"], "small", (200, 200, 200)))
                self.ui_manager.add_component(Label(LEFT_COLUMN_X + 20, 555, f"生命值: {info['hp']}", "small", (255, 100, 100)))
                self.ui_manager.add_component(Label(LEFT_COLUMN_X + 20, 590, f"消耗值: {info['mp']}", "small", (100, 200, 255)))
                self.ui_manager.add_component(Label(LEFT_COLUMN_X + 20, 625, f"攻击力: {info['atk']}/{info['m_atk']}", "small", (100, 255, 100)))

        # 3. 右侧：职业配图
        selected_class = self.class_names[self.selected_index]
        sprite_idx = CLASSES[selected_class]["sprite_index"]
        
        if sprite_idx < len(self.sprites):
            char_sprite = self.sprites[sprite_idx]
            if selected_class == "程序员" and sprite_idx == 0:
                char_sprite = pygame.transform.flip(char_sprite, True, False)
            
            # 装饰框 (Panel)
            self.ui_manager.add_component(Panel(RIGHT_COLUMN_X - 20, 180, 296, 296, (60, 60, 60, 255), UIConfig.COLOR_YELLOW, 3, 15))
            # 图片 (ImageComponent)
            self.ui_manager.add_component(ImageComponent(RIGHT_COLUMN_X, 200, char_sprite))
        else:
            # 占位符
            self.ui_manager.add_component(Panel(RIGHT_COLUMN_X, 200, 256, 256, (100, 100, 100, 255), border_radius=10))
            self.ui_manager.add_component(Label(RIGHT_COLUMN_X + 80, 310, "图片加载中...", "small", (150, 150, 150)))
        
        self.ui_manager.draw()

    def update_selection(self, direction):
        self.selected_index = (self.selected_index + direction) % len(self.class_names)
