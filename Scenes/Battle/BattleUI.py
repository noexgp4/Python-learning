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
        
        # 数值标签在上方或旁边
        val_text = f"{label}: {int(current)} / {int(maximum)}"
        self.draw_text(val_text, (x, y - 22), color, "small")

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
        # 状态条放在控制区上方，长度拉长
        base_x, base_y = 100, sh - 280
        
        # 绘制长的 HP 条
        self.draw_bar(base_x, base_y, player.hp, player.max_hp, (50, 200, 50), width=600, label="HP")
        # 绘制长的 MP 条 (紧跟下方)
        self.draw_bar(base_x, base_y + 40, player.mp, player.max_mp, player.theme_color, width=600, label="MP")

    def draw_enemy_status(self, enemy):
        sw = self.screen.get_width()
        base_x, base_y = sw - 350, 100
        self.draw_text(enemy.name, (base_x, base_y), (255, 100, 100))
        self.draw_bar(base_x, base_y + 40, enemy.hp, enemy.max_hp, (200, 50, 50), width=250, label="")

    def draw_menu_grid(self, options, selected_idx, player_color):
        sw, sh = self.screen.get_width(), self.screen.get_height()
        # 控制按键区在底部，一行两个
        base_x, base_y = 100, sh - 180
        col_width = 320
        row_height = 50

        for i, opt in enumerate(options):
            col = i % 2
            row = i // 2
            x = base_x + col * col_width
            y = base_y + row * row_height
            
            is_selected = (i == selected_idx)
            color = player_color if is_selected else (200, 200, 200)
            
            # 绘制按钮框
            btn_rect = pygame.Rect(x, y, 280, 40)
            bg_color = (40, 40, 45) if not is_selected else (60, 60, 70)
            pygame.draw.rect(self.screen, bg_color, btn_rect)
            pygame.draw.rect(self.screen, color if is_selected else (100, 100, 100), btn_rect, 2)
            
            text_surf = UIConfig.render_text(opt, "normal", color)
            self.screen.blit(text_surf, (x + 140 - text_surf.get_width() // 2, y + 20 - text_surf.get_height() // 2))

    def draw_skill_menu_grid(self, player, selected_idx):
        sw, sh = self.screen.get_width(), self.screen.get_height()
        # 技能二级菜单也采用 2x2 网格
        panel_rect = pygame.Rect(80, sh - 200, 700, 180)
        s = pygame.Surface((panel_rect.width, panel_rect.height))
        s.set_alpha(230)
        s.fill((15, 15, 25))
        self.screen.blit(s, panel_rect)
        pygame.draw.rect(self.screen, player.theme_color, panel_rect, 2)

        for i, skill in enumerate(player.skills):
            col = i % 2
            row = i // 2
            x = panel_rect.x + 40 + col * 320
            y = panel_rect.y + 40 + row * 60
            
            is_selected = (i == selected_idx)
            can_afford = player.mp >= skill.get('cost', 0)
            
            if not can_afford: color = (80, 80, 80)
            elif is_selected: color = player.theme_color
            else: color = (255, 255, 255)
            
            skill_name = f"{'▶ ' if is_selected else ''}{skill['name']}"
            self.draw_text(skill_name, (x, y), color)
            self.draw_text(f"{skill.get('cost', 0)} MP", (x + 200, y + 4), color, "small")

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