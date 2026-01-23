import pygame
import json
import os

class SettingsScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("SimHei", 40)
        self.config_file = "config.json"
        
        # 1. 先尝试加载存档，再初始化
        self.volume = self.load_config()
        
        # 2. 资源路径整合
        self.bgm_path = r"Source\Aduio\music.mp3"
        self.sounds = {}
        self.load_all_resources()
        
        # 3. 初始应用音量
        pygame.mixer.music.set_volume(self.volume)

    def load_config(self):
        """从文件读取音量设置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    return data.get("volume", 0.5)
            except:
                return 0.5
        return 0.5

    def save_config(self):
        """将当前音量保存到文件"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({"volume": self.volume}, f)
            print("配置已保存")
        except Exception as e:
            print(f"保存失败: {e}")

    def load_all_resources(self):
        # 加载背景音乐（流式）
        try:
            pygame.mixer.music.load(self.bgm_path)
            pygame.mixer.music.play(-1) # 循环播放
        except:
            print("背景音乐加载失败")

        # 加载按钮音效
        try:
            sound_path = r"Source\Aduio\Sound.wav"
            self.sounds["button"] = pygame.mixer.Sound(sound_path)
            self.sounds["button"].set_volume(self.volume)
        except:
            print("按钮音效加载失败")
            self.sounds["button"] = None

    def update_volume(self, direction):
        self.volume = max(0.0, min(1.0, self.volume + direction * 0.1))
        pygame.mixer.music.set_volume(self.volume)
        if self.sounds["button"]:
            self.sounds["button"].set_volume(self.volume)
        
        # 每次调节后自动保存，或者在退出设置界面时保存
        self.save_config()

    def play_sfx(self, name):
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()

    def draw(self):
        self.screen.fill((40, 40, 40))
        # 绘制逻辑（同前，此处略...）
        val_text = self.font.render(f"音量: {int(self.volume * 100)}%", True, (255, 255, 0))
        self.screen.blit(val_text, (400 - val_text.get_width()//2, 300))