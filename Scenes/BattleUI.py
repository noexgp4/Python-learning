import pygame

class BattleUI:
    def __init__(self, screen, font_config):
        self.screen = screen
        self.font_config = font_config # 引用你之前的 UIConfig
        
        # 伤害数字列表，存储 {'val': 50, 'pos': (x,y), 'ttl': 60}
        self.damage_numbers = []
        
        # 血条平滑动画用的“显示血量”
        self.player_display_hp = 0
        self.enemy_display_hp = 0

    def trigger_damage_num(self, value, pos):
        """当逻辑层算出伤害时，调用此方法产生飘字"""
        self.damage_numbers.append({
            'val': value,
            'x': pos[0] + 50, # 稍微偏移一下位置
            'y': pos[1] - 20,
            'ttl': 60,       # 生存时间 (frames)
            'alpha': 255
        })

    def draw_stat_bar(self, x, y, w, h, current, maximum, display_hp, color):
        """带缓动效果的血条"""
        # 计算背景
        pygame.draw.rect(self.screen, (30, 30, 30), (x, y, w, h))
        
        # 缓动逻辑：让显示血量慢慢靠近实际血量
        if display_hp < current: display_hp += 1
        if display_hp > current: display_hp -= 1
        
        # 计算比例
        fill_w = int((display_hp / maximum) * (w - 4))
        if fill_w > 0:
            pygame.draw.rect(self.screen, color, (x + 2, y + 2, fill_w, h - 4))
            
        # 绘制精美边框
        pygame.draw.rect(self.screen, (200, 200, 200), (x, y, w, h), 2)
        return display_hp # 返回更新后的显示血量

    def draw_menu(self, menu_options, selected_index):
        """绘制战斗指令菜单"""
        panel_rect = pygame.Rect(100, 800, 400, 240)
        # 绘制半透明底色
        s = pygame.Surface((panel_rect.width, panel_rect.height))
        s.set_alpha(180)
        s.fill((10, 10, 20))
        self.screen.blit(s, (panel_rect.x, panel_rect.y))
        pygame.draw.rect(self.screen, (180, 150, 50), panel_rect, 3)

        for i, option in enumerate(menu_options):
            color = (255, 215, 0) if i == selected_index else (255, 255, 255)
            text = f"> {option}" if i == selected_index else f"  {option}"
            # 假设你 UIConfig 有 render_text 方法
            surf = self.font_config.render_text(text, "normal", color)
            self.screen.blit(surf, (panel_rect.x + 40, panel_rect.y + 40 + i * 50))

    def update_and_draw_effects(self):
        """处理伤害数字的飘动和消失"""
        for num in self.damage_numbers[:]:
            num['y'] -= 1      # 向上飘
            num['ttl'] -= 1    # 生命周期减少
            
            # 渲染数字
            txt_surf = self.font_config.render_text(str(num['val']), "normal", (255, 50, 50))
            # 简单的透明度淡出效果
            if num['ttl'] < 20:
                txt_surf.set_alpha(int(num['ttl'] / 20 * 255))
            
            self.screen.blit(txt_surf, (num['x'], num['y']))
            
            if num['ttl'] <= 0:
                self.damage_numbers.remove(num)