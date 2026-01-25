import pygame
import os

class AudioManager:
    def __init__(self):
        self.bgm_volume = 0.5
        self.sfx_volume = 0.5
        self.sounds = {}
        
        # 资源路径
        self.config_file = os.path.join(os.path.dirname(__file__), "config.json")
        self.bgm_path = os.path.join(os.path.dirname(__file__), "..", "Assets", "Aduio", "music.mp3")
        self.sfx_path = os.path.join(os.path.dirname(__file__), "..", "Assets", "Aduio", "Sound.wav")
        
        self.load_config()
        self.load_resources()

    def load_config(self):
        """加载音频配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    import json
                    data = json.load(f)
                    self.bgm_volume = max(0.0, min(1.0, data.get("bgm_volume", 0.5)))
                    self.sfx_volume = max(0.0, min(1.0, data.get("sfx_volume", 0.5)))
            except Exception as e:
                print(f"音频管理器加载配置失败: {e}")

    def load_resources(self):
        """加载所有音频资源"""
        # 加载背景音乐（流式）
        try:
            print(f"尝试加载背景音乐: {self.bgm_path}")
            print(f"文件存在: {os.path.exists(self.bgm_path)}")
            if os.path.exists(self.bgm_path):
                pygame.mixer.music.load(self.bgm_path)
                pygame.mixer.music.play(-1) # 循环播放
                pygame.mixer.music.set_volume(self.bgm_volume)
                print(f"✓ 背景音乐加载成功")
            else:
                print(f"✗ 背景音乐文件不存在")
        except Exception as e:
            print(f"✗ 背景音乐加载失败: {e}")

        # 加载按钮音效
        try:
            print(f"尝试加载按钮音效: {self.sfx_path}")
            print(f"文件存在: {os.path.exists(self.sfx_path)}")
            if os.path.exists(self.sfx_path):
                self.sounds["button"] = pygame.mixer.Sound(self.sfx_path)
                self.sounds["button"].set_volume(self.sfx_volume)
                print(f"✓ 按钮音效加载成功")
            else:
                print(f"✗ 按钮音效文件不存在")
        except Exception as e:
            print(f"✗ 按钮音效加载失败: {e}")
            self.sounds["button"] = None

    def set_bgm_volume(self, volume):
        """设置背景音乐音量"""
        self.bgm_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.bgm_volume)

    def set_sfx_volume(self, volume):
        """设置音效音量"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        if self.sounds.get("button"):
            self.sounds["button"].set_volume(self.sfx_volume)

    def play_sfx(self, name):
        """播放指定音效"""
        if name in self.sounds and self.sounds[name]:
            self.sounds[name].play()
