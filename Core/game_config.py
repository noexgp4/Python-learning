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
        
        # 预加载头像与雪碧图
        self.avatars = {}
        self.sprites = []
        
        import os
        base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
        
        # 1. 加载头像 (由 jobs.json 提供的 avatar_path)
        for name, data in CLASSES.items():
            path = data.get("avatar_path")
            if path:
                try:
                    # 尝试多种可能的路径组合
                    full_path = os.path.join(base_dir, path)
                    if not os.path.exists(full_path):
                        # 尝试在 Characters/avatar 目录下找
                        filename = os.path.basename(path)
                        full_path = os.path.join(base_dir, "Assets", "Image", "Characters", "avatar", filename)
                    
                    if os.path.exists(full_path):
                        img = pygame.image.load(full_path).convert_alpha()
                        # 放大到 256x256
                        self.avatars[name] = pygame.transform.scale(img, (256, 256))
                    else:
                        print(f"找不到职业头像文件: {path}")
                except Exception as e:
                    print(f"加载职业头像失败 ({name}): {e}")

        # 2. 加载雪碧图 (作为备选)
        try:
            sprite_path = os.path.join(base_dir, "Assets", "Image", "character_sprites.png")
            if os.path.exists(sprite_path):
                sheet = pygame.image.load(sprite_path).convert_alpha()
                for i in range(2):
                    rect = pygame.Rect(i * 32, 0, 32, 32)
                    sprite = sheet.subsurface(rect)
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
            display_name = job_data.get("name", name)
            
            color = job_data.get("theme_color", (150, 150, 150)) if is_selected else (150, 150, 150)
            display_text = f"▶ {display_name}" if is_selected else f"  {display_name}"
            self.ui_manager.add_component(Label(LEFT_COLUMN_X, 200 + i * 60, display_text, "normal", color))

            if is_selected:
                info = job_data
                hp_label = get_text("class_select", "hp", "生命值")
                mp_label = get_text("class_select", "mp", "消耗值")
                atk_label = get_text("class_select", "atk", "攻击力")
                
                self.ui_manager.add_component(Label(LEFT_COLUMN_X + 20, 520, info.get("desc", ""), "small", (200, 200, 200)))
                self.ui_manager.add_component(Label(LEFT_COLUMN_X + 20, 555, f"{hp_label}: {info.get('hp', 0)}", "small", (255, 100, 100)))
                self.ui_manager.add_component(Label(LEFT_COLUMN_X + 20, 590, f"{mp_label}: {info.get('mp', 0)}", "small", (100, 200, 255)))
                self.ui_manager.add_component(Label(LEFT_COLUMN_X + 20, 625, f"{atk_label}: {info.get('atk', 0)}/{info.get('m_atk', 0)}", "small", (100, 255, 100)))

        # 3. 右侧：职业配图
        selected_class = self.class_names[self.selected_index]
        job_info = CLASSES[selected_class]
        
        # 优先使用精美头像
        display_img = self.avatars.get(selected_class)
        
        # 如果没有头像，回退到雪碧图
        if not display_img:
            sprite_idx = job_info.get("sprite_index", 0)
            if sprite_idx < len(self.sprites):
                display_img = self.sprites[sprite_idx]
                # 针对特定职业做翻转处理（可选）
                if selected_class == "程序员" and sprite_idx == 0:
                    display_img = pygame.transform.flip(display_img, True, False)

        if display_img:
            # 装饰框 (Panel)
            self.ui_manager.add_component(Panel(RIGHT_COLUMN_X - 20, 180, 296, 296, (60, 60, 60, 255), UIConfig.COLOR_YELLOW, 3, 15))
            # 图片 (ImageComponent)
            self.ui_manager.add_component(ImageComponent(RIGHT_COLUMN_X, 200, display_img))
        else:
            # 最终占位符
            self.ui_manager.add_component(Panel(RIGHT_COLUMN_X, 200, 256, 256, (100, 100, 100, 255), border_radius=10))
            self.ui_manager.add_component(Label(RIGHT_COLUMN_X + 80, 310, "图片加载中...", "small", (150, 150, 150)))
        
        self.ui_manager.draw()

    def update_selection(self, direction):
        self.selected_index = (self.selected_index + direction) % len(self.class_names)
