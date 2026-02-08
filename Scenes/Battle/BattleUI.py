import pygame
from Scenes.text import UIConfig

class BattleUI:
    def __init__(self, screen):
        self.screen = screen
        self.damage_numbers = []

    def draw_text(self, text, pos, color=(255, 255, 255), size="normal"):
        surf = UIConfig.render_text(text, size, color)
        self.screen.blit(surf, pos)
        return surf

    def draw_character_portraits(self, player, enemy):
        sw, sh = self.screen.get_width(), self.screen.get_height()
        import os
        base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))

        # 同一水平线 Y 坐标
        ground_y = sh // 2 - 50

        # 1. 绘制敌人 (左侧)
        # 占位符或怪物图
        enemy_pos = (150, ground_y)
        pygame.draw.circle(self.screen, (200, 50, 50), (enemy_pos[0] + 50, enemy_pos[1] + 50), 50)
        self.draw_text(enemy.name, (enemy_pos[0] + 10, enemy_pos[1] + 110), (255, 100, 100), "small")

        # 2. 绘制玩家 (右侧)
        try:
            from Core.game_config import CLASSES
            job_data = CLASSES.get(player.job_name, {})
            avatar_path = job_data.get("avatar_path")
            if avatar_path:
                full_path = os.path.join(base_dir, avatar_path)
                if os.path.exists(full_path):
                    img = pygame.image.load(full_path).convert_alpha()
                    # 左右对半，玩家在右边，面向左边 (翻转)
                    img = pygame.transform.flip(img, True, False)
                    # 调整为合适大小 (如 200x200)
                    img = pygame.transform.scale(img, (200, 200))
                    self.screen.blit(img, (sw - 350, ground_y - 50))
        except: pass

    def draw_bar(self, x, y, current, maximum, color, width=400, height=15, label="HP"):
        # 背景
        pygame.draw.rect(self.screen, (20, 20, 20), (x, y, width, height))
        # 填充
        if maximum > 0:
            fill_w = int((max(0, current) / maximum) * (width - 4))
            if fill_w > 0:
                pygame.draw.rect(self.screen, color, (x + 2, y + 2, fill_w, height - 4))
        # 边框
        pygame.draw.rect(self.screen, (180, 160, 50), (x, y, width, height), 2)
        
        # 数值标签在下方（如果有标签）
        if label:
            val_text = f"{label}: {int(current)} / {int(maximum)}"
            self.draw_text(val_text, (x, y + height + 2), color, "small")

    def trigger_damage_num(self, value, pos):
        self.damage_numbers.append({
            'val': value,
            'x': pos[0],
            'y': pos[1],
            'ttl': 50,
            'vx': 1,
            'vy': -2
        })

    def draw_player_status(self, player):
        sw, sh = self.screen.get_width(), self.screen.get_height()
        # 玩家血条跟随玩家（右侧上方）
        base_x = sw - 380
        base_y = sh // 2 - 150
        bar_w = 280
        
        self.draw_bar(base_x, base_y, player.hp, player.max_hp, (50, 200, 50), width=bar_w, label="HP")
        self.draw_bar(base_x, base_y + 45, player.mp, player.max_mp, player.theme_color, width=bar_w, label="MP")

    def draw_enemy_status(self, enemy):
        sw, sh = self.screen.get_width(), self.screen.get_height()
        # 敌人血条跟随敌人（左侧上方）
        base_x = 100
        base_y = sh // 2 - 150
        bar_w = 280
        self.draw_text(enemy.name, (base_x, base_y - 40), (255, 100, 100))
        self.draw_bar(base_x, base_y, enemy.hp, enemy.max_hp, (200, 50, 50), width=bar_w, label="HP")

    def draw_menu_grid(self, options, selected_idx, player_color):
        sw, sh = self.screen.get_width(), self.screen.get_height()
        # 底栏占满宽度
        panel_h = 160
        base_y = sh - panel_h
        
        # 绘制底栏背景
        pygame.draw.rect(self.screen, (20, 20, 30), (0, base_y, sw, panel_h))
        pygame.draw.rect(self.screen, (100, 100, 100), (0, base_y, sw, panel_h), 2)
        
        # 选项在此分布
        start_x = 50
        col_width = (sw - 100) // 2
        row_height = 50

        for i, opt in enumerate(options):
            col = i % 2
            row = i // 2
            x = start_x + col * col_width
            y = base_y + 30 + row * row_height
            
            is_selected = (i == selected_idx)
            color = player_color if is_selected else (200, 200, 200)
            
            # 按钮框
            btn_w = col_width - 40
            btn_rect = pygame.Rect(x, y, btn_w, 40)
            bg_color = (40, 40, 45) if not is_selected else (60, 60, 70)
            pygame.draw.rect(self.screen, bg_color, btn_rect)
            pygame.draw.rect(self.screen, color if is_selected else (100, 100, 100), btn_rect, 2)
            
            text_surf = UIConfig.render_text(opt, "normal", color)
            self.screen.blit(text_surf, (x + btn_w // 2 - text_surf.get_width() // 2, y + 20 - text_surf.get_height() // 2))

    def draw_skill_menu_grid(self, player, selected_idx):
        sw, sh = self.screen.get_width(), self.screen.get_height()
        # 技能菜单全屏底栏
        panel_h = 160
        panel_rect = pygame.Rect(0, sh - panel_h, sw, panel_h)
        s = pygame.Surface((panel_rect.width, panel_rect.height))
        s.set_alpha(240)
        s.fill((15, 15, 25))
        self.screen.blit(s, panel_rect)
        pygame.draw.rect(self.screen, player.theme_color, panel_rect, 2)

        col_w = (sw - 100) // 2
        for i, skill in enumerate(player.active_skills):
            col = i % 2
            row = i // 2
            x = 50 + col * col_w
            y = panel_rect.y + 30 + row * 60
            
            is_selected = (i == selected_idx)
            can_afford = player.mp >= skill.get('cost', 0)
            
            if not can_afford: color = (80, 80, 80)
            elif is_selected: color = player.theme_color
            else: color = (255, 255, 255)
            
            skill_name = f"{'▶ ' if is_selected else ''}{skill['name']}"
            self.draw_text(skill_name, (x, y), color, size="small" if len(skill_name)>6 else "normal")
            self.draw_text(f"{skill.get('cost', 0)} MP", (x + col_w - 100, y + 4), color, "small")

    def update_and_draw_effects(self):
        for num in self.damage_numbers[:]:
            num['x'] += num['vx']
            num['y'] += num['vy']
            num['vy'] += 0.1
            num['ttl'] -= 1
            txt_surf = UIConfig.render_text(str(num['val']), "normal", (255, 50, 50))
            if num['ttl'] < 20:
                txt_surf.set_alpha(int(num['ttl'] / 20 * 255))
            self.screen.blit(txt_surf, (num['x'], num['y']))
            if num['ttl'] <= 0:
                self.damage_numbers.remove(num)