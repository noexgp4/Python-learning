import pygame
from Scenes.text import UIConfig, Panel, Label, ImageComponent, ProgressBar
from Scenes.UIManager import UIManager
from Scenes.DataManager import data_manager

class CharacterMenuScene:
    def __init__(self, screen, game_state, player_entity, initial_tab="STATS"):
        self.screen = screen
        self.game_state = game_state
        self.player = player_entity
        self.ui_manager = UIManager(self.screen)
        
        # 标签页定义
        self.tabs = ["STATS", "INVENTORY", "SKILLS"]
        self.tab_names = {
            "STATS": "属性 (I)",
            "INVENTORY": "背包 (B)",
            "SKILLS": "技能 (K)"
        }
        self.current_tab = initial_tab
        
        # 加载头像
        self.avatar = self._load_avatar()
        
        # 布局常量
        self.sidebar_w = 280
        self.content_x = 320
        self.content_y = 100
        self.content_w = screen.get_width() - self.content_x - 40
        self.content_h = screen.get_height() - 140

    def _load_avatar(self):
        """加载职业头像"""
        job_data = data_manager.jobs.get(self.game_state.job_name, {})
        path = job_data.get("avatar_path")
        if path:
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            full_path = os.path.join(base_dir, path)
            if os.path.exists(full_path):
                try:
                    img = pygame.image.load(full_path).convert_alpha()
                    return pygame.transform.scale(img, (200, 200))
                except:
                    pass
        return None

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:
                return "WORLD"
            # 快捷键切换标签
            if event.key == pygame.K_i:
                self.current_tab = "STATS"
            elif event.key == pygame.K_b:
                self.current_tab = "INVENTORY"
            elif event.key == pygame.K_k:
                self.current_tab = "SKILLS"
            
            # Q/E 循环切换
            elif event.key == pygame.K_q:
                idx = self.tabs.index(self.current_tab)
                self.current_tab = self.tabs[(idx - 1) % len(self.tabs)]
            elif event.key == pygame.K_e:
                idx = self.tabs.index(self.current_tab)
                self.current_tab = self.tabs[(idx + 1) % len(self.tabs)]
        return None

    def draw(self):
        # 1. 绘制半透明背景遮罩
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        self.ui_manager.clear()
        
        # 2. 绘制主面板
        self.ui_manager.add_component(Panel(20, 20, self.screen.get_width() - 40, self.screen.get_height() - 40, (30, 30, 30, 255), UIConfig.COLOR_YELLOW, 2, 20))
        
        # 3. 绘制侧边栏（头像和基础信息）
        self._draw_sidebar()
        
        # 4. 绘制标签页头
        self._draw_tabs()
        
        # 5. 绘制当前标签页内容
        if self.current_tab == "STATS":
            self._draw_stats()
        elif self.current_tab == "INVENTORY":
            self._draw_inventory()
        elif self.current_tab == "SKILLS":
            self._draw_skills()
            
        self.ui_manager.draw()

    def _draw_sidebar(self):
        # 头像框
        self.ui_manager.add_component(Panel(40, 60, 220, 220, (50, 50, 50, 255), UIConfig.COLOR_GRAY, 1, 10))
        if self.avatar:
            self.ui_manager.add_component(ImageComponent(50, 70, self.avatar))
        
        # 名字和职业
        job_data = data_manager.jobs.get(self.game_state.job_name, {})
        display_name = job_data.get("name", self.game_state.job_name)
        self.ui_manager.add_component(Label(40, 300, display_name, "title", UIConfig.COLOR_YELLOW))
        
        # 等级和经验
        lv_text = f"等级 {self.game_state.level}"
        self.ui_manager.add_component(Label(40, 360, lv_text, "normal", UIConfig.COLOR_WHITE))
        
        from Scenes.Battle.data.level_config import get_required_exp
        req_exp = get_required_exp(self.game_state.level)
        exp_progress = self.game_state.exp / req_exp if req_exp > 0 else 1.0
        
        self.ui_manager.add_component(Label(40, 400, "经验值", "small", UIConfig.COLOR_GRAY_LIGHT))
        self.ui_manager.add_component(ProgressBar(40, 430, 220, 15, exp_progress, is_selected=True))
        exp_val_text = f"{self.game_state.exp} / {req_exp}"
        self.ui_manager.add_component(Label(40, 455, exp_val_text, "small", UIConfig.COLOR_GRAY))

        # 金币
        gold_text = f"金币: {self.game_state.gold}"
        self.ui_manager.add_component(Label(40, 500, gold_text, "normal", (255, 215, 0)))

    def _draw_tabs(self):
        tab_x = self.content_x
        tab_w = 150
        for i, tab in enumerate(self.tabs):
            is_active = (self.current_tab == tab)
            color = UIConfig.COLOR_YELLOW if is_active else UIConfig.COLOR_GRAY
            bg_color = (60, 60, 60, 255) if is_active else (40, 40, 40, 255)
            
            self.ui_manager.add_component(Panel(tab_x + i * (tab_w + 10), 40, tab_w, 45, bg_color, color, 2, 10))
            text = self.tab_names[tab]
            tx = tab_x + i * (tab_w + 10) + (tab_w - UIConfig.SMALL_FONT.size(text)[0]) // 2
            self.ui_manager.add_component(Label(tx, 52, text, "small", color))

    def _draw_stats(self):
        # 1. 基础属性展示 (左侧)
        stats_list = [
            ("生命值", f"{self.game_state.player_hp} / {self.game_state.max_hp}", (255, 100, 100)),
            ("魔法值", f"{self.game_state.player_mp} / {self.game_state.max_mp}", (100, 150, 255)),
            ("物理攻击", f"{self.game_state.attack}", UIConfig.COLOR_WHITE),
            ("魔法攻击", f"{self.game_state.m_attack}", UIConfig.COLOR_WHITE),
            ("物理防御", f"{self.game_state.defense}", UIConfig.COLOR_WHITE),
            ("移动速度", f"{self.game_state.spd}", UIConfig.COLOR_WHITE)
        ]
        
        half_w = self.content_w // 2 - 10
        item_h = 55
        spacing = 12
        
        # 绘制左侧标题
        self.ui_manager.add_component(Label(self.content_x, self.content_y - 40, "核心属性", "normal", UIConfig.COLOR_YELLOW))
        
        for i, (label, val, color) in enumerate(stats_list):
            y = self.content_y + i * (item_h + spacing)
            self.ui_manager.add_component(Panel(self.content_x, y, half_w, item_h, (40, 40, 40, 255), border_radius=10))
            self.ui_manager.add_component(Label(self.content_x + 15, y + 12, label, "small", UIConfig.COLOR_GRAY_LIGHT))
            self.ui_manager.add_component(Label(self.content_x + half_w - 120, y + 12, val, "small", color))

        # 2. 装备展示 (右侧)
        equip_x = self.content_x + half_w + 20
        self.ui_manager.add_component(Label(equip_x, self.content_y - 40, "当前穿搭", "normal", UIConfig.COLOR_YELLOW))
        
        slots = [
            ("武器", "weapon", "weapons"),
            ("头部", "head", "armors"),
            ("身体", "armor", "armors")
        ]
        
        slot_h = item_h * 1.6
        for i, (slot_label, key, category) in enumerate(slots):
            y = self.content_y + i * (slot_h + spacing)
            # 插槽背景
            self.ui_manager.add_component(Panel(equip_x, y, half_w, slot_h, (45, 45, 45, 255), UIConfig.COLOR_GRAY, 1, 12))
            
            # 槽位名
            self.ui_manager.add_component(Label(equip_x + 15, y + 8, slot_label, "small", UIConfig.COLOR_GRAY))
            
            # 获取装备数据
            item_id = self.game_state.equipped.get(key)
            item_name = "未装备"
            item_color = (100, 100, 100)
            attr_text = "---"
            
            if item_id:
                item_data = data_manager.equips.get(category, {}).get(item_id)
                if item_data:
                    item_name = item_data.get("name", item_id)
                    item_color = UIConfig.COLOR_WHITE
                    # 属性概览
                    if category == "weapons":
                        atk = item_data.get("atk", 0)
                        attr_text = f"攻击 +{atk}"
                    else:
                        df = item_data.get("def", 0)
                        spd = item_data.get("spd", 0)
                        parts = []
                        if df: parts.append(f"防御 +{df}")
                        if spd: parts.append(f"速度 +{spd}")
                        attr_text = " ".join(parts) if parts else "装饰品"
            
            # 装备名称和属性
            self.ui_manager.add_component(Label(equip_x + 15, y + 35, item_name, "normal", item_color))
            self.ui_manager.add_component(Label(equip_x + 15, y + 65, attr_text, "small", UIConfig.COLOR_GRAY_LIGHT))

    def _draw_inventory(self):
        # 背包网格建议 4x4 或 5x5
        cols = 5
        slot_size = 80
        spacing = 20
        
        inventory = self.game_state.inventory
        for i in range(25): # 显示 25 个格子
            row = i // cols
            col = i % cols
            x = self.content_x + col * (slot_size + spacing)
            y = self.content_y + row * (slot_size + spacing)
            
            self.ui_manager.add_component(Panel(x, y, slot_size, slot_size, (45, 45, 45, 255), (100, 100, 100), 1, 8))
            
            if i < len(inventory):
                item = inventory[i]
                # 这里可以根据物品 ID 显示图标或名字缩写
                item_name = str(item)[:4]
                self.ui_manager.add_component(Label(x + 5, y + 25, item_name, "small", UIConfig.COLOR_WHITE))
        
        if not inventory:
            self.ui_manager.add_component(Label(self.content_x, self.content_y + 100, "背包里空空如也...", "normal", UIConfig.COLOR_GRAY))

    def _draw_skills(self):
        # 获取职业技能
        job_data = data_manager.jobs.get(self.game_state.job_name, {})
        skills_ids = job_data.get("skills", [])
        
        # 导入技能库获取详细描述
        from Scenes.Battle.data.skills_library import SKILLS_LIB
        
        for i, skill_id in enumerate(skills_ids):
            y = self.content_y + i * 90
            skill_info = SKILLS_LIB.get(skill_id, {"name": skill_id, "desc": "未知技能"})
            
            self.ui_manager.add_component(Panel(self.content_x, y, self.content_w, 80, (40, 40, 40, 255), UIConfig.COLOR_BLUE, 1, 12))
            
            # 技能名称
            name = skill_info.get("name", skill_id)
            self.ui_manager.add_component(Label(self.content_x + 20, y + 10, name, "normal", UIConfig.COLOR_PALETTE_GOLD))
            
            # 消耗
            cost = skill_info.get("cost", 0)
            cost_text = f"MP: {cost}" if cost > 0 else "无消耗"
            self.ui_manager.add_component(Label(self.content_x + self.content_w - 120, y + 15, cost_text, "small", (100, 200, 255)))
            
            # 描述
            desc = skill_info.get("desc", "")
            self.ui_manager.add_component(Label(self.content_x + 25, y + 45, desc, "small", (180, 180, 180)))
        
        if not skills_ids:
            self.ui_manager.add_component(Label(self.content_x, self.content_y + 100, "还没有学习任何技能。", "normal", UIConfig.COLOR_GRAY))