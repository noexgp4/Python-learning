import pygame
import json
import os

class SettingsScene:
    
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("SimHei", 40)
        self.small_font = pygame.font.SysFont("SimHei", 30)
        
        # 使用绝对路径保存配置文件
        self.config_file = os.path.join(os.path.dirname(__file__), "config.json")
        
        # 初始化音量属性，防止访问错误
        self.bgm_volume = 0.5
        self.sfx_volume = 0.5
        
        # 初始化临时音量（用于调整设置但未保存时）
        self.temp_bgm_volume = 0.5
        self.temp_sfx_volume = 0.5
        
        # 1. 先尝试加载存档，再初始化
        self.load_config()
        
        # 2. 资源路径整合 - 使用相对路径指向上级 Assets 文件夹
        self.bgm_path = os.path.join(os.path.dirname(__file__), "..", "Assets", "Aduio", "music.mp3")
        self.sounds = {}
        self.load_all_resources()
        
        # 3. 菜单选择项
        self.selected_item = 0  # 0: 背景音乐, 1: 音效, 2: 保存, 3: 恢复默认
        
        # 4. 初始应用音量（必须在加载资源后）
        pygame.mixer.music.set_volume(self.bgm_volume)
        if self.sounds.get("button"):
            self.sounds["button"].set_volume(self.sfx_volume)

    def load_config(self):
        """从文件读取音量设置"""
        print(f"尝试从 {self.config_file} 加载配置...")
        print(f"配置文件存在: {os.path.exists(self.config_file)}")
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 确保读取的值在 0.0-1.0 范围内
                    self.bgm_volume = max(0.0, min(1.0, data.get("bgm_volume", 0.5)))
                    self.sfx_volume = max(0.0, min(1.0, data.get("sfx_volume", 0.5)))
                    print(f"✓ 从 {self.config_file} 加载配置成功")
                    print(f"  背景音乐音量: {int(self.bgm_volume*100)}%")
                    print(f"  音效音量: {int(self.sfx_volume*100)}%")
            except Exception as e:
                print(f"✗ 加载配置失败: {e}，使用默认值")
                self.bgm_volume = 0.5
                self.sfx_volume = 0.5
        else:
            print(f"✗ 配置文件不存在，将在 {self.config_file} 创建")
            self.bgm_volume = 0.5
            self.sfx_volume = 0.5
        
        # 进入设置界面时，从当前值初始化临时值
        self.temp_bgm_volume = self.bgm_volume
        self.temp_sfx_volume = self.sfx_volume

    def save_config(self):
        """将临时音量保存到文件和生效状态"""
        try:
            # 将临时音量提交为正式音量（确保范围正确）
            self.bgm_volume = max(0.0, min(1.0, self.temp_bgm_volume))
            self.sfx_volume = max(0.0, min(1.0, self.temp_sfx_volume))
            
            # 四舍五入到2位小数避免浮点数精度问题
            data = {
                "bgm_volume": round(self.bgm_volume, 2),
                "sfx_volume": round(self.sfx_volume, 2)
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✓ 配置已保存到 {self.config_file}")
            print(f"  背景音乐: {int(self.bgm_volume*100)}%, 音效: {int(self.sfx_volume*100)}%")
            return True
        except Exception as e:
            print(f"✗ 保存失败: {e}")
            print(f"  尝试保存位置: {self.config_file}")
            return False
    
    def cancel_settings(self):
        """取消设置，恢复之前保存的值"""
        self.temp_bgm_volume = self.bgm_volume
        self.temp_sfx_volume = self.sfx_volume
        pygame.mixer.music.set_volume(self.bgm_volume)
        if self.sounds.get("button"):
            self.sounds["button"].set_volume(self.sfx_volume)
        print("已取消设置改动")

    def reset_to_default(self):
        """恢复默认设置"""
        self.temp_bgm_volume = 0.5
        self.temp_sfx_volume = 0.5
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
        """根据选中项更新对应的临时音量（不立即应用）"""
        if self.selected_item == 0:  # 背景音乐
            self.temp_bgm_volume = max(0.0, min(1.0, self.temp_bgm_volume + direction * 0.1))
            # 实时预览音量
            pygame.mixer.music.set_volume(self.temp_bgm_volume)
        elif self.selected_item == 1:  # 音效
            self.temp_sfx_volume = max(0.0, min(1.0, self.temp_sfx_volume + direction * 0.1))
            # 实时预览音量
            if self.sounds.get("button"):
                self.sounds["button"].set_volume(self.temp_sfx_volume)

    def update_selection(self, direction):
        """更新菜单选择"""
        self.selected_item = (self.selected_item + direction) % 4

    def play_sfx(self, name):
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()

    def enter_settings(self):
        """进入设置界面时调用，重新初始化临时值"""
        self.temp_bgm_volume = self.bgm_volume
        self.temp_sfx_volume = self.sfx_volume
        pygame.mixer.music.set_volume(self.bgm_volume)
        if self.sounds.get("button"):
            self.sounds["button"].set_volume(self.sfx_volume)
        print(f"进入设置界面，当前音量 - 背景音乐: {int(self.bgm_volume*100)}%, 音效: {int(self.sfx_volume*100)}%")

    def draw(self):
        self.screen.fill((40, 40, 40))
        
        # 绘制标题
        title_font = pygame.font.SysFont("SimHei", 60)
        title_text = title_font.render("游戏设置", True, (255, 215, 0))
        self.screen.blit(title_text, (400 - title_text.get_width()//2, 30))
        
        # 绘制背景音乐控制
        self._draw_volume_control(100, "背景音乐", self.temp_bgm_volume, 0)
        
        # 绘制音效控制
        self._draw_volume_control(210, "音效", self.temp_sfx_volume, 1)
        
        # 绘制按钮
        self._draw_button(330, "保存设置", 2)
        self._draw_button(410, "恢复默认", 3)
        
        # 绘制提示文字
        tip_font = pygame.font.SysFont("SimHei", 24)
        tip_text = tip_font.render("↑↓ 选择  ← → 调节  Enter 确认  ESC 返回", True, (200, 200, 200))
        self.screen.blit(tip_text, (400 - tip_text.get_width()//2, 520))

    def _draw_volume_control(self, y_pos, label, volume, item_id):
        """绘制音量控制条"""
        # 选中状态
        label_color = (255, 255, 0) if self.selected_item == item_id else (255, 255, 255)
        is_selected = self.selected_item == item_id
        
        # 绘制标签
        label_text = self.font.render(label, True, label_color)
        self.screen.blit(label_text, (100, y_pos))
        
        # 绘制音量控制条
        bar_x = 100
        bar_y = y_pos + 50
        bar_width = 500
        bar_height = 35
        
        # 边框颜色
        border_color = (100, 200, 255) if is_selected else (100, 100, 100)
        pygame.draw.rect(self.screen, border_color, (bar_x, bar_y, bar_width, bar_height), 3)
        
        # 填充条
        fill_width = int(bar_width * volume)
        pygame.draw.rect(self.screen, (100, 200, 255), (bar_x, bar_y, fill_width, bar_height))
        
        # 百分比文字
        vol_text = self.font.render(f"{int(volume * 100)}%", True, (255, 255, 0))
        self.screen.blit(vol_text, (bar_x + bar_width + 30, bar_y + bar_height//2 - vol_text.get_height()//2))

    def _draw_button(self, y_pos, text, item_id):
        """绘制按钮"""
        button_color = (100, 200, 255) if self.selected_item == item_id else (100, 100, 100)
        is_selected = self.selected_item == item_id
        
        # 绘制按钮背景
        button_rect = pygame.Rect(200, y_pos, 400, 50)
        pygame.draw.rect(self.screen, button_color, button_rect, 3)
        if is_selected:
            pygame.draw.rect(self.screen, (50, 150, 200), button_rect)
        
        # 绘制按钮文字
        text_color = (255, 255, 0) if is_selected else (255, 255, 255)
        button_text = self.font.render(text, True, text_color)
        self.screen.blit(button_text, (400 - button_text.get_width()//2, y_pos + 50//2 - button_text.get_height()//2))

