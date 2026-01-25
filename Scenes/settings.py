import pygame
import json
import os

class SettingsScene:
    
    # 支持的分辨率列表
    RESOLUTIONS = [
        (800, 600),
        (1024, 768),
        (1280, 720),
        (1920, 1080),
    ]
    
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("SimHei", 40)
        self.small_font = pygame.font.SysFont("SimHei", 30)
        
        # 使用相对路径保存配置文件在 Scenes 目录
        self.config_file = os.path.join(os.path.dirname(__file__), "config.json")
        
        # 初始化音量属性
        self.bgm_volume = 0.5
        self.sfx_volume = 0.5
        
        # 初始化显示属性
        self.resolution_index = 0  # 默认 800x600
        self.is_fullscreen = False
        
        # 初始化临时属性（用于调整设置但未保存时）
        self.temp_bgm_volume = 0.5
        self.temp_sfx_volume = 0.5
        self.temp_resolution_index = 0
        self.temp_is_fullscreen = False
        
        # 1. 先尝试加载存档
        self.load_config()
        
        # 2. 资源路径整合 - 使用绝对路径避免相对路径问题
        self.bgm_path = os.path.join(os.path.dirname(__file__), "..", "Assets", "Aduio", "music.mp3")
        self.sounds = {}
        self.load_all_resources()
        
        # 3. 菜单选择项
        # 0: 背景音乐, 1: 音效, 2: 分辨率, 3: 全屏, 4: 保存, 5: 恢复默认
        self.selected_item = 0
        
        # 4. 初始应用音量（必须在加载资源后）
        pygame.mixer.music.set_volume(self.bgm_volume)
        if self.sounds.get("button"):
            self.sounds["button"].set_volume(self.sfx_volume)

    def load_config(self):
        """从文件读取音量和显示设置"""
        print(f"尝试从 {self.config_file} 加载配置...")
        print(f"配置文件存在: {os.path.exists(self.config_file)}")
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 加载音量
                    self.bgm_volume = max(0.0, min(1.0, data.get("bgm_volume", 0.5)))
                    self.sfx_volume = max(0.0, min(1.0, data.get("sfx_volume", 0.5)))
                    # 加载分辨率
                    self.resolution_index = data.get("resolution_index", 0)
                    self.is_fullscreen = data.get("is_fullscreen", False)
                    print(f"✓ 从 {self.config_file} 加载配置成功")
                    print(f"  背景音乐音量: {int(self.bgm_volume*100)}%")
                    print(f"  音效音量: {int(self.sfx_volume*100)}%")
                    print(f"  分辨率: {self.RESOLUTIONS[self.resolution_index]}")
                    print(f"  全屏模式: {'是' if self.is_fullscreen else '否'}")
            except Exception as e:
                print(f"✗ 加载配置失败: {e}，使用默认值")
                self._set_defaults()
        else:
            print(f"✗ 配置文件不存在，将在 {self.config_file} 创建")
            self._set_defaults()
        
        # 进入设置界面时，从当前值初始化临时值
        self.temp_bgm_volume = self.bgm_volume
        self.temp_sfx_volume = self.sfx_volume
        self.temp_resolution_index = self.resolution_index
        self.temp_is_fullscreen = self.is_fullscreen

    def _set_defaults(self):
        """设置默认值"""
        self.bgm_volume = 0.5
        self.sfx_volume = 0.5
        self.resolution_index = 0
        self.is_fullscreen = False

    def save_config(self):
        """将临时设置保存到文件"""
        try:
            # 将临时值提交为正式值
            self.bgm_volume = max(0.0, min(1.0, self.temp_bgm_volume))
            self.sfx_volume = max(0.0, min(1.0, self.temp_sfx_volume))
            self.resolution_index = self.temp_resolution_index
            self.is_fullscreen = self.temp_is_fullscreen
            
            # 四舍五入到2位小数避免浮点数精度问题
            data = {
                "bgm_volume": round(self.bgm_volume, 2),
                "sfx_volume": round(self.sfx_volume, 2),
                "resolution_index": self.resolution_index,
                "is_fullscreen": self.is_fullscreen
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✓ 配置已保存到 {self.config_file}")
            print(f"  背景音乐: {int(self.bgm_volume*100)}%, 音效: {int(self.sfx_volume*100)}%")
            print(f"  分辨率: {self.RESOLUTIONS[self.resolution_index]}, 全屏: {self.is_fullscreen}")
            return True
        except Exception as e:
            print(f"✗ 保存失败: {e}")
            print(f"  尝试保存位置: {self.config_file}")
            return False
    
    def cancel_settings(self):
        """取消设置，恢复之前保存的值"""
        self.temp_bgm_volume = self.bgm_volume
        self.temp_sfx_volume = self.sfx_volume
        self.temp_resolution_index = self.resolution_index
        self.temp_is_fullscreen = self.is_fullscreen
        pygame.mixer.music.set_volume(self.bgm_volume)
        if self.sounds.get("button"):
            self.sounds["button"].set_volume(self.sfx_volume)
        print("已取消设置改动")

    def reset_to_default(self):
        """恢复默认设置"""
        self.temp_bgm_volume = 0.5
        self.temp_sfx_volume = 0.5
        self.temp_resolution_index = 0
        self.temp_is_fullscreen = False
        pygame.mixer.music.set_volume(self.temp_bgm_volume)
        if self.sounds.get("button"):
            self.sounds["button"].set_volume(self.temp_sfx_volume)
        print("已恢复默认设置（未保存）")

    def load_all_resources(self):
        # 加载背景音乐（流式）
        try:
            print(f"尝试加载背景音乐: {self.bgm_path}")
            print(f"文件存在: {os.path.exists(self.bgm_path)}")
            pygame.mixer.music.load(self.bgm_path)
            pygame.mixer.music.play(-1) # 循环播放
            print(f"✓ 背景音乐加载成功")
        except Exception as e:
            print(f"✗ 背景音乐加载失败: {e}")

        # 加载按钮音效
        try:
            sound_path = os.path.join(os.path.dirname(__file__), "..", "Assets", "Aduio", "Sound.wav")
            print(f"尝试加载按钮音效: {sound_path}")
            print(f"文件存在: {os.path.exists(sound_path)}")
            self.sounds["button"] = pygame.mixer.Sound(sound_path)
            self.sounds["button"].set_volume(self.sfx_volume)
            print(f"✓ 按钮音效加载成功")
        except Exception as e:
            print(f"✗ 按钮音效加载失败: {e}")
            self.sounds["button"] = None

    def update_volume(self, direction):
        """根据选中项更新对应的临时音量"""
        if self.selected_item == 0:  # 背景音乐
            self.temp_bgm_volume = max(0.0, min(1.0, self.temp_bgm_volume + direction * 0.1))
            pygame.mixer.music.set_volume(self.temp_bgm_volume)
        elif self.selected_item == 1:  # 音效
            self.temp_sfx_volume = max(0.0, min(1.0, self.temp_sfx_volume + direction * 0.1))
            if self.sounds.get("button"):
                self.sounds["button"].set_volume(self.temp_sfx_volume)
        elif self.selected_item == 2:  # 分辨率
            self.temp_resolution_index = (self.temp_resolution_index + direction) % len(self.RESOLUTIONS)
        elif self.selected_item == 3:  # 全屏切换
            self.temp_is_fullscreen = not self.temp_is_fullscreen

    def update_selection(self, direction):
        """更新菜单选择（0-5共6项）"""
        self.selected_item = (self.selected_item + direction) % 6

    def play_sfx(self, name):
        """播放音效"""
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()

    def enter_settings(self):
        """进入设置界面时调用"""
        self.temp_bgm_volume = self.bgm_volume
        self.temp_sfx_volume = self.sfx_volume
        self.temp_resolution_index = self.resolution_index
        self.temp_is_fullscreen = self.is_fullscreen
        pygame.mixer.music.set_volume(self.bgm_volume)
        if self.sounds.get("button"):
            self.sounds["button"].set_volume(self.sfx_volume)
        print(f"进入设置界面，当前音量 - 背景音乐: {int(self.bgm_volume*100)}%, 音效: {int(self.sfx_volume*100)}%")

    def draw(self):
        screen_width, screen_height = self.screen.get_size()
        self.screen.fill((40, 40, 40))
        
        # 绘制标题
        title_font = pygame.font.SysFont("SimHei", 60)
        title_text = title_font.render("游戏设置", True, (255, 215, 0))
        self.screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, int(screen_height * 0.02)))
        
        # 绘制各个设置项
        y_offset = int(screen_height * 0.12)
        item_spacing = int(screen_height * 0.15)
        
        # 背景音乐音量
        self._draw_volume_control(y_offset, "背景音乐", self.temp_bgm_volume, 0)
        y_offset += item_spacing
        
        # 音效音量
        self._draw_volume_control(y_offset, "音效", self.temp_sfx_volume, 1)
        y_offset += item_spacing
        
        # 分辨率选择
        self._draw_resolution_control(y_offset, 2)
        y_offset += item_spacing - int(screen_height * 0.03)
        
        # 全屏切换
        self._draw_fullscreen_control(y_offset, 3)
        y_offset += item_spacing - int(screen_height * 0.03)
        
        # 保存和恢复按钮
        self._draw_button(y_offset, "保存设置", 4)
        y_offset += int(screen_height * 0.08)
        self._draw_button(y_offset, "恢复默认", 5)
        
        # 绘制提示文字
        tip_font = pygame.font.SysFont("SimHei", 20)
        tip_text = tip_font.render("↑↓ 选择  ← → 调节  Enter 确认  ESC 返回", True, (200, 200, 200))
        self.screen.blit(tip_text, (screen_width//2 - tip_text.get_width()//2, screen_height - 40))

    def _draw_volume_control(self, y_pos, label, volume, item_id):
        """绘制音量控制条"""
        screen_width, screen_height = self.screen.get_size()
        label_color = (255, 255, 0) if self.selected_item == item_id else (255, 255, 255)
        is_selected = self.selected_item == item_id
        
        # 绘制标签
        label_text = self.font.render(label, True, label_color)
        self.screen.blit(label_text, (int(screen_width * 0.05), y_pos))
        
        # 绘制音量控制条
        bar_x = int(screen_width * 0.35)
        bar_y = y_pos + 5
        bar_width = int(screen_width * 0.4)
        bar_height = 35
        
        # 边框颜色
        border_color = (100, 200, 255) if is_selected else (100, 100, 100)
        pygame.draw.rect(self.screen, border_color, (bar_x, bar_y, bar_width, bar_height), 3)
        
        # 填充条
        fill_width = int(bar_width * volume)
        pygame.draw.rect(self.screen, (100, 200, 255), (bar_x, bar_y, fill_width, bar_height))
        
        # 百分比文字
        vol_text = self.font.render(f"{int(volume * 100)}%", True, (255, 255, 0))
        self.screen.blit(vol_text, (bar_x + bar_width + int(screen_width * 0.03), bar_y + bar_height//2 - vol_text.get_height()//2))

    def _draw_resolution_control(self, y_pos, item_id):
        """绘制分辨率选择"""
        screen_width, screen_height = self.screen.get_size()
        is_selected = self.selected_item == item_id
        label_color = (255, 255, 0) if is_selected else (255, 255, 255)
        
        # 绘制标签
        label_text = self.font.render("分辨率", True, label_color)
        self.screen.blit(label_text, (int(screen_width * 0.05), y_pos))
        
        # 绘制分辨率选项
        res_text = f"{self.RESOLUTIONS[self.temp_resolution_index][0]}x{self.RESOLUTIONS[self.temp_resolution_index][1]}"
        res_color = (100, 200, 255) if is_selected else (200, 200, 200)
        res_display = self.font.render(res_text, True, res_color)
        
        # 绘制选择框
        box_x = int(screen_width * 0.35)
        box_y = y_pos
        box_width = int(screen_width * 0.4)
        box_height = 40
        
        border_color = (100, 200, 255) if is_selected else (100, 100, 100)
        pygame.draw.rect(self.screen, border_color, (box_x, box_y, box_width, box_height), 3)
        if is_selected:
            pygame.draw.rect(self.screen, (50, 150, 200), (box_x, box_y, box_width, box_height))
        
        self.screen.blit(res_display, (box_x + box_width//2 - res_display.get_width()//2, box_y + box_height//2 - res_display.get_height()//2))
        
        # 绘制箭头提示
        arrow_text = self.small_font.render("< >", True, (150, 150, 150))
        self.screen.blit(arrow_text, (box_x + box_width + int(screen_width * 0.03), box_y + box_height//2 - arrow_text.get_height()//2))

    def _draw_fullscreen_control(self, y_pos, item_id):
        """绘制全屏选择"""
        screen_width, screen_height = self.screen.get_size()
        is_selected = self.selected_item == item_id
        label_color = (255, 255, 0) if is_selected else (255, 255, 255)
        
        # 绘制标签
        label_text = self.font.render("显示模式", True, label_color)
        self.screen.blit(label_text, (int(screen_width * 0.05), y_pos))
        
        # 绘制全屏状态
        mode_text = "全屏" if self.temp_is_fullscreen else "窗口"
        mode_color = (100, 200, 255) if is_selected else (200, 200, 200)
        mode_display = self.font.render(mode_text, True, mode_color)
        
        # 绘制选择框
        box_x = int(screen_width * 0.35)
        box_y = y_pos
        box_width = int(screen_width * 0.4)
        box_height = 40
        
        border_color = (100, 200, 255) if is_selected else (100, 100, 100)
        pygame.draw.rect(self.screen, border_color, (box_x, box_y, box_width, box_height), 3)
        if is_selected:
            pygame.draw.rect(self.screen, (50, 150, 200), (box_x, box_y, box_width, box_height))
        
        self.screen.blit(mode_display, (box_x + box_width//2 - mode_display.get_width()//2, box_y + box_height//2 - mode_display.get_height()//2))
        
        # 绘制提示
        tip_text = self.small_font.render("← → 切换", True, (150, 150, 150))
        self.screen.blit(tip_text, (box_x + box_width + int(screen_width * 0.03), box_y + box_height//2 - tip_text.get_height()//2))

    def _draw_button(self, y_pos, text, item_id):
        """绘制按钮"""
        screen_width, screen_height = self.screen.get_size()
        button_color = (100, 200, 255) if self.selected_item == item_id else (100, 100, 100)
        is_selected = self.selected_item == item_id
        
        # 绘制按钮背景
        button_x = int(screen_width * 0.2)
        button_width = int(screen_width * 0.6)
        button_rect = pygame.Rect(button_x, y_pos, button_width, 50)
        pygame.draw.rect(self.screen, button_color, button_rect, 3)
        if is_selected:
            pygame.draw.rect(self.screen, (50, 150, 200), button_rect)
        
        # 绘制按钮文字
        text_color = (255, 255, 0) if is_selected else (255, 255, 255)
        button_text = self.font.render(text, True, text_color)
        self.screen.blit(button_text, (screen_width//2 - button_text.get_width()//2, y_pos + 50//2 - button_text.get_height()//2))

    def get_current_resolution(self):
        """获取当前分辨率"""
        return self.RESOLUTIONS[self.resolution_index]

    def is_fullscreen_mode(self):
        """是否全屏模式"""
        return self.is_fullscreen

    def apply_resolution_change(self):
        """应用分辨率和全屏设置（需要在 main.py 中调用）"""
        width, height = self.RESOLUTIONS[self.resolution_index]
        flags = pygame.FULLSCREEN if self.is_fullscreen else 0
        self.screen = pygame.display.set_mode((width, height), flags)
        print(f"分辨率已改变为 {width}x{height}，全屏: {self.is_fullscreen}")
        return self.screen  # 返回新的屏幕对象
