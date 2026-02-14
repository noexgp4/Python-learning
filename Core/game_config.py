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
        self.selected_skill_index = 0 # 当前预览的技能索引
        self.ui_manager = UIManager(self.screen)
        
        # 预加载头像与雪碧图
        self.avatars = {}
        self.sprites = []
        
        from Scenes.Battle.data.skills_library import SKILLS_LIB
        self.skills_lib = SKILLS_LIB

        import os
        base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
        
        # 1. 加载头像 (由 jobs.json 提供的 avatar_path)
        for name, data in CLASSES.items():
            path = data.get("avatar_path")
            if path:
                try:
                    full_path = os.path.join(base_dir, path)
                    if not os.path.exists(full_path):
                        filename = os.path.basename(path)
                        full_path = os.path.join(base_dir, "Assets", "Image", "Characters", "avatar", filename)
                    
                    if os.path.exists(full_path):
                        img = pygame.image.load(full_path).convert_alpha()
                        # UI 需要头像比例。根据设计图估计。此处放大到 160x160。
                        self.avatars[name] = pygame.transform.scale(img, (160, 160))
                except Exception as e:
                    print(f"加载职业头像失败 ({name}): {e}")

    def draw(self):
        # 尝试获取语言管理器
        lang_manager = getattr(pygame, 'language_manager', None)
        def get_text(cat, key, default):
            if lang_manager: return lang_manager.get_text(cat, key)
            return default

        # 1. 填充深色背景并清理 UI
        self.screen.fill(getattr(UIConfig, 'COLOR_DARK_BG', (20, 20, 20)))
        self.ui_manager.clear()
        
        sw, sh = self.screen.get_width(), self.screen.get_height()

        # 2. 标题
        title_text = get_text("class_select", "title", "请选择你的初始角色")
        title_surf = UIConfig.TITLE_FONT.render(title_text, True, UIConfig.COLOR_WHITE)
        tx = (sw - title_surf.get_width()) // 2
        self.screen.blit(title_surf, (tx, 45))

        # 3. 主白色大容器 ( rounded rect )
        margin = 40
        cw, ch = sw - margin * 2, sh - 160
        cx, cy = margin, 130
        self.ui_manager.add_component(Panel(cx, cy, cw, ch, (255, 255, 255, 255), border_radius=25))

        # --- 左侧：职业选择列表 (淡蓝色) ---
        lw = 280
        lx, ly = cx + 20, cy + 20
        lh = ch - 40
        self.ui_manager.add_component(Panel(lx, ly, lw, lh, (200, 240, 255, 255), border_radius=15))

        # 渲染职业项
        for i, name in enumerate(self.class_names):
            is_selected = (i == self.selected_index)
            job_data = CLASSES[name]
            display_name = job_data.get("name", name)
            
            ix, iy = lx + 15, ly + 20 + i * 55
            iw, ih = lw - 30, 45
            
            if is_selected:
                # 选中的背景块
                self.ui_manager.add_component(Panel(ix, iy, iw, ih, (255, 255, 255, 255), border_width=1, border_radius=8))
                text_color = (0, 0, 0)
            else:
                text_color = (100, 130, 150)
            
            self.ui_manager.add_component(Label(ix + 15, iy + 5, display_name, "normal", text_color))

        # --- 右侧：详细内容区 ---
        rx = lx + lw + 20
        ry = ly
        rw = cw - lw - 60
        rh = lh

        selected_class = self.class_names[self.selected_index]
        job_info = CLASSES[selected_class]
        stats = job_info.get("initial_stats", {})

        # 4. 职业配图 (右上角 A)
        display_img = self.avatars.get(selected_class)
        if display_img:
            # 装饰框
            self.ui_manager.add_component(Panel(rx, ry, 170, 170, (255, 200, 150, 255), UIConfig.COLOR_PALETTE_GOLD, 2, 10))
            self.ui_manager.add_component(ImageComponent(rx + 5, ry + 5, display_img))
        
        # 5. 属性列表 (右上角 B)
        # 物理攻击，魔法攻击，护甲，魔抗，装弹量，生命值
        stat_x = rx + 190
        stat_y = ry + 5
        stat_labels = [
            ("物理攻击", stats.get("atk", 0)),
            ("魔法攻击", stats.get("m_atk", 0)),
            ("护甲", stats.get("def", 0)),
            ("魔抗", 15), # 暂用固定值或默认值
            ("法杖能量" if selected_class == "Mage" else "装弹量", stats.get("mp", 0)),
            ("生命值", stats.get("hp", 0))
        ]
        
        for i, (label, val) in enumerate(stat_labels):
            sy = stat_y + i * 28
            msg = f"{label}: {val}"
            # 画一个带下划线的容器
            pygame.draw.line(self.screen, (150, 150, 150), (stat_x, sy + 22), (stat_x + 120, sy + 22), 1)
            self.ui_manager.add_component(Label(stat_x, sy, msg, "small", (50, 50, 50)))

        # 6. 职业简介 (右上角 C)
        desc_x = stat_x + 150
        desc_w = (cx + cw) - desc_x - 30
        self.ui_manager.add_component(Panel(desc_x, ry, desc_w, 150, (210, 250, 255, 255), border_radius=10))
        # 这里的文本需要简单的换行处理，或者使用多个 Label
        desc_text = job_info.get("desc", "擅长远程攻击，拥有超高爆发攻击力。")
        self._add_multiline_label(desc_text, desc_x + 15, ry + 15, desc_w - 30, (50, 50, 50))

        # 7. 技能列表 (右下角 D)
        skill_y = ry + 190
        skill_ids = job_info.get("skills", [])
        sw_item = 180
        sh_item = 220
        self.ui_manager.add_component(Panel(rx, skill_y, sw_item, sh_item, (210, 250, 255, 255), border_radius=10))
        
        for i, s_id in enumerate(skill_ids[:4]): # 最多显示4个
            is_s_selected = (i == self.selected_skill_index)
            skill_info = self.skills_lib.get(s_id, {"name": "未知技能"})
            sname = skill_info.get("name")
            
            sx, sy = rx + 15, skill_y + 40 + i * 40
            if is_s_selected:
                pygame.draw.rect(self.screen, (255, 255, 255), (sx - 5, sy - 5, sw_item - 20, 32), border_radius=4)
                pygame.draw.rect(self.screen, (0, 150, 255), (sx - 5, sy - 5, sw_item - 20, 32), 1, border_radius=4)
            
            self.ui_manager.add_component(Label(sx, sy, sname, "small", (0, 0, 0) if is_s_selected else (80, 100, 120)))

        # 8. 技能详情 (右下角 E)
        detail_x = rx + sw_item + 20
        detail_w = (cx + cw) - detail_x - 30
        self.ui_manager.add_component(Panel(detail_x, skill_y, detail_w, sh_item, (210, 250, 255, 255), border_radius=10))
        
        if skill_ids:
            cur_skill = self.skills_lib.get(skill_ids[self.selected_skill_index % len(skill_ids)], {})
            s_desc = cur_skill.get("desc", "暂无详细描述。")
            self._add_multiline_label(s_desc, detail_x + 20, skill_y + 20, detail_w - 40, (0, 0, 0))

        self.ui_manager.draw()

    def _add_multiline_label(self, text, x, y, max_w, color):
        """简单的多行文本辅助，将文字加入 UI 管理器"""
        words = list(text) # 单字分割支持中文
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word
            if UIConfig.SMALL_FONT.size(test_line)[0] < max_w:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        
        for i, line in enumerate(lines):
            self.ui_manager.add_component(Label(x, y + i * 25, line, "small", color))

    def update_selection(self, direction):
        self.selected_index = (self.selected_index + direction) % len(self.class_names)
        self.selected_skill_index = 0 # 切换职业时重置技能预览

    def update_skill_selection(self, direction):
        """支持左右/额外按键切换技能预览"""
        job_info = CLASSES[self.class_names[self.selected_index]]
        skills = job_info.get("skills", [])
        if skills:
            self.selected_skill_index = (self.selected_skill_index + direction) % len(skills)
