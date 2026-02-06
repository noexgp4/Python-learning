import pygame
from Scenes.text import UIConfig, Label, Panel, ImageComponent
from Scenes.UIManager import UIManager
from Scenes.Battle.data.jobs_config import JOBS as JOBS_DATA

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
            import os
            base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
            sprite_path = os.path.join(base_dir, "Assets", "Image", "character_sprites.png")
            sheet = pygame.image.load(sprite_path).convert_alpha()
            for i in range(2):
                rect = pygame.Rect(i * 32, 0, 32, 32)
                sprite = sheet.subsurface(rect)
                # 放大图片使其更清晰且符合大屏显示 (32x32 -> 256x256)
                self.sprites.append(pygame.transform.scale(sprite, (256, 256)))
        except Exception as e:
            print(f"加载职业雪碧图失败: {e}")

    def draw(self):
        # 尝试获取语言管理器
        lang_manager = getattr(pygame, 'language_manager', None)
        def get_text(cat, key, default):
            if lang_manager: return lang_manager.get_text(cat, key)
            return default

        # 填充深色背景
        self.screen.fill(getattr(UIConfig, 'COLOR_DARK_BG', (30, 30, 30)))
        self.ui_manager.clear()
        
        # 1. 标题
        title_text = get_text("class_select", "title", "请选择你的初始职业")
        tw = UIConfig.TITLE_FONT.size(title_text)[0]
        self.ui_manager.add_component(Label((self.screen.get_width() - tw)//2, 50, title_text, "title", UIConfig.COLOR_YELLOW))

        # 定义布局
        LEFT_COLUMN_X = 100
        RIGHT_COLUMN_X = 450
        
        # 2. 左侧：职业列表与属性
        for i, name in enumerate(self.class_names):
            is_selected = (i == self.selected_index)
            job_data = CLASSES[name]
            # 获取本地化的职业名称 (通过 jobs_config 已经合并进来的 'name' 字段)
            display_name = job_data.get("name", name)
            
            color = job_data.get("theme_color", (150, 150, 150)) if is_selected else (150, 150, 150)
            display_text = f"▶ {display_name}" if is_selected else f"  {display_name}"
            self.ui_manager.add_component(Label(LEFT_COLUMN_X, 200 + i * 60, display_text, "normal", color))

            if is_selected:
                info = job_data
                # 获取翻译后的标签
                hp_label = get_text("class_select", "hp", "生命值")
                mp_label = get_text("class_select", "mp", "消耗值")
                atk_label = get_text("class_select", "atk", "攻击力")
                
                self.ui_manager.add_component(Label(LEFT_COLUMN_X + 20, 520, info.get("desc", ""), "small", (200, 200, 200)))
                self.ui_manager.add_component(Label(LEFT_COLUMN_X + 20, 555, f"{hp_label}: {info.get('hp', 0)}", "small", (255, 100, 100)))
                self.ui_manager.add_component(Label(LEFT_COLUMN_X + 20, 590, f"{mp_label}: {info.get('mp', 0)}", "small", (100, 200, 255)))
                self.ui_manager.add_component(Label(LEFT_COLUMN_X + 20, 625, f"{atk_label}: {info.get('atk', 0)}/{info.get('m_atk', 0)}", "small", (100, 255, 100)))

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
