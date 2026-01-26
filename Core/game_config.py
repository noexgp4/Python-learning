from Scenes.text import UIConfig

# 职业初始属性配置
CLASSES = {
    "学生": {"hp": 120, "atk": 10, "desc": "高生命值，擅长近战", "color": (200, 50, 50)},
    "上班族": {"hp": 80, "atk": 20, "desc": "脆皮但魔法伤害极高", "color": (50, 100, 255)},
    "程序员": {"hp": 90, "atk": 15, "desc": "高暴击，身手敏捷", "color": (50, 200, 50)}
}
class ClassSelectScene:
    def __init__(self, screen):
        self.screen = screen
        self.class_names = list(CLASSES.keys())
        self.selected_index = 0

    def draw(self):
        self.screen.fill(UIConfig.COLOR_BG)
        
        # 1. 标题
        title = UIConfig.render_text("请选择你的职业", type="title", color=UIConfig.COLOR_YELLOW)
        UIConfig.draw_center_text(self.screen, title, 80)

        # 2. 遍历职业列表
        for i, name in enumerate(self.class_names):
            is_selected = (i == self.selected_index)
            color = CLASSES[name]["color"] if is_selected else (150, 150, 150)
            
            # 如果选中，加个小箭头
            display_text = f"> {name} <" if is_selected else name
            
            surf = UIConfig.render_text(display_text, type="normal", color=color)
            UIConfig.draw_center_text(self.screen, surf, 250 + i * 80)

            # 3. 显示当前选中职业的详细信息
            if is_selected:
                info = CLASSES[name]
                desc_surf = UIConfig.render_text(info["desc"], type="small", color=(200, 200, 200))
                stat_surf = UIConfig.render_text(f"初始生命: {info['hp']}  攻击力: {info['atk']}", type="small")
                
                UIConfig.draw_center_text(self.screen, desc_surf, 500)
                UIConfig.draw_center_text(self.screen, stat_surf, 540)

    def update_selection(self, direction):
        self.selected_index = (self.selected_index + direction) % len(self.class_names)