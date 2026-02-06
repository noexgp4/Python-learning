import pygame
import json
import os
import os
from Scenes.text import UIConfig, Button, Label, ProgressBar, SelectBox
from Scenes.UIManager import UIManager

class SettingsScene:
    
    # 支持的分辨率列表
    RESOLUTIONS = [
        (800, 600),
        (1024, 768),
        (1280, 720),
        (1920, 1080),
    ]

    # 支持的语言列表
    LANGUAGES = ["zh", "en"]
    
    def __init__(self, screen, audio_manager, language_manager):
        self.screen = screen
        self.audio_manager = audio_manager
        self.language_manager = language_manager
        # self.font = pygame.font.SysFont("SimHei", 40)
        # self.small_font = pygame.font.SysFont("SimHei", 30)
        
        # 使用相对路径保存配置文件在 Core 目录
        self.config_file = os.path.join(os.path.dirname(__file__), "..", "Core", "config.json")
        
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
        self.temp_language = "zh"
        
        # 1. 先尝试加载存档
        self.load_config()
        
        # 3. 菜单选择项
        # 0: 背景音乐, 1: 音效, 2: 语言, 3: 分辨率, 4: 全屏, 5: 保存, 6: 恢复默认
        self.selected_item = 0
        
        # 4. 初始化UI管理器
        self.ui_manager = UIManager(self.screen)

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
                    self.audio_manager.set_bgm_volume(self.bgm_volume)
                    self.audio_manager.set_sfx_volume(self.sfx_volume)
                    # 加载分辨率
                    self.resolution_index = data.get("resolution_index", 0)
                    self.is_fullscreen = data.get("is_fullscreen", False)
                    # 加载语言
                    self.current_language = data.get("language", "zh")
                    self.language_manager.change_language(self.current_language)
                    
                    print(f"[OK] 从 {self.config_file} 加载配置成功")
                    print(f"  背景音乐音量: {int(self.bgm_volume*100)}%")
                    print(f"  音效音量: {int(self.sfx_volume*100)}%")
                    print(f"  分辨率: {self.RESOLUTIONS[self.resolution_index]}")
                    print(f"  全屏模式: {'是' if self.is_fullscreen else '否'}")
            except Exception as e:
                print(f"[ERROR] 加载配置失败: {e}，使用默认值")
                self._set_defaults()
        else:
            print(f"[INFO] 配置文件不存在，将在 {self.config_file} 创建")
            self._set_defaults()
        
        # 进入设置界面时，从当前值初始化临时值
        self.temp_bgm_volume = self.bgm_volume
        self.temp_sfx_volume = self.sfx_volume
        self.temp_resolution_index = self.resolution_index
        self.temp_is_fullscreen = self.is_fullscreen
        self.temp_language = getattr(self, "current_language", "zh")

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
            self.current_language = self.temp_language
            
            # 确保语言管理器状态同步
            self.language_manager.change_language(self.current_language)
            
            # 同时也需要告诉职业系统重新加载对应语言的翻译
            try:
                from Scenes.Battle.data.jobs_config import load_jobs_config
                load_jobs_config(self.current_language)
            except Exception as e:
                print(f"[Warning] Failed to reload jobs config: {e}")
            
            # 四舍五入到2位小数避免浮点数精度问题
            data = {
                "bgm_volume": round(self.bgm_volume, 2),
                "sfx_volume": round(self.sfx_volume, 2),
                "resolution_index": self.resolution_index,
                "is_fullscreen": self.is_fullscreen,
                "language": self.current_language
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[OK] 配置已保存到 {self.config_file}")
            print(f"  背景音乐: {int(self.bgm_volume*100)}%, 音效: {int(self.sfx_volume*100)}%")
            print(f"  分辨率: {self.RESOLUTIONS[self.resolution_index]}, 全屏: {self.is_fullscreen}")
            return True
        except Exception as e:
            print(f"[ERROR] 保存失败: {e}")
            print(f"  尝试保存位置: {self.config_file}")
            return False
    
    def cancel_settings(self):
        """取消设置，恢复之前保存的值"""
        self.temp_bgm_volume = self.bgm_volume
        self.temp_sfx_volume = self.sfx_volume
        self.temp_resolution_index = self.resolution_index
        self.temp_is_fullscreen = self.is_fullscreen
        self.temp_language = getattr(self, "current_language", "zh")
        self.language_manager.change_language(self.current_language)
        self.audio_manager.set_bgm_volume(self.bgm_volume)
        self.audio_manager.set_sfx_volume(self.sfx_volume)
        print("已取消设置改动")

    def reset_to_default(self):
        """恢复默认设置"""
        self.temp_bgm_volume = 0.5
        self.temp_sfx_volume = 0.5
        self.temp_resolution_index = 0
        self.temp_is_fullscreen = False
        self.temp_language = "zh"
        self.language_manager.change_language("zh") # 恢复默认时预览中文
        self.audio_manager.set_bgm_volume(self.temp_bgm_volume)
        self.audio_manager.set_sfx_volume(self.temp_sfx_volume)
        print("已恢复默认设置（未保存）")



    def update_volume(self, direction):
        """根据选中项更新对应的临时音量"""
        if self.selected_item == 0:  # 背景音乐
            self.temp_bgm_volume = max(0.0, min(1.0, self.temp_bgm_volume + direction * 0.1))
            self.audio_manager.set_bgm_volume(self.temp_bgm_volume)
        elif self.selected_item == 1:  # 音效
            self.temp_sfx_volume = max(0.0, min(1.0, self.temp_sfx_volume + direction * 0.1))
            self.audio_manager.set_sfx_volume(self.temp_sfx_volume)
        elif self.selected_item == 2:  # 语言
            # 找到当前语言索引
            current_idx = 0
            if self.temp_language in self.LANGUAGES:
                current_idx = self.LANGUAGES.index(self.temp_language)
            # 切换
            new_idx = (current_idx + direction) % len(self.LANGUAGES)
            self.temp_language = self.LANGUAGES[new_idx]
            # 实时预览
            self.language_manager.change_language(self.temp_language)
            
        elif self.selected_item == 3:  # 分辨率
            self.temp_resolution_index = (self.temp_resolution_index + direction) % len(self.RESOLUTIONS)
        elif self.selected_item == 4:  # 全屏切换
            self.temp_is_fullscreen = not self.temp_is_fullscreen
        elif self.selected_item == 5: # 保存按钮
            if direction > 0: # 向右切换到恢复默认
                self.selected_item = 6
        elif self.selected_item == 6: # 恢复默认按钮
            if direction < 0: # 向左切换到保存
                self.selected_item = 5

    def update_selection(self, direction):
        """更新菜单选择（0-6共7项）"""
        self.selected_item = (self.selected_item + direction) % 7

    def play_sfx(self, name):
        """播放音效"""
        self.audio_manager.play_sfx(name)

    def enter_settings(self):
        """进入设置界面时调用"""
        self.temp_bgm_volume = self.bgm_volume
        self.temp_sfx_volume = self.sfx_volume
        self.temp_resolution_index = self.resolution_index
        self.temp_is_fullscreen = self.is_fullscreen
        self.audio_manager.set_bgm_volume(self.bgm_volume)
        self.audio_manager.set_sfx_volume(self.sfx_volume)
        print(f"进入设置界面，当前音量 - 背景音乐: {int(self.bgm_volume*100)}%, 音效: {int(self.sfx_volume*100)}%")

    def draw(self):
        screen_width, screen_height = self.screen.get_size()
        self.screen.fill(UIConfig.COLOR_SCREEN_BG)
        self.ui_manager.clear() # 每一帧清空，重新构建UI组件树
        
        # 1. 绘制标题
        title_text_str = self.language_manager.get_text("settings", "title")
        title_width = UIConfig.TITLE_FONT.size(title_text_str)[0]
        self.ui_manager.add_component(Label(
            screen_width//2 - title_width//2, 
            int(screen_height * 0.02), 
            title_text_str, 
            "title", 
            UIConfig.COLOR_SETTINGS_TITLE
        ))
        
        # 2. 绘制各个设置项
        y_offset = int(screen_height * 0.12)
        item_spacing = int(screen_height * 0.13)
        
        # 背景音乐音量
        self._add_volume_ui(y_offset, self.language_manager.get_text("settings", "bgm"), self.temp_bgm_volume, 0)
        y_offset += item_spacing
        
        # 音效音量
        self._add_volume_ui(y_offset, self.language_manager.get_text("settings", "sfx"), self.temp_sfx_volume, 1)
        y_offset += item_spacing
        
        # 语言选择
        self._add_selectbox_ui(y_offset, self.language_manager.get_text("settings", "language"), 2)
        y_offset += item_spacing

        # 分辨率选择
        self._add_selectbox_ui(y_offset, self.language_manager.get_text("settings", "resolution"), 3)
        y_offset += item_spacing
        
        # 全屏切换
        self._add_selectbox_ui(y_offset, self.language_manager.get_text("settings", "display"), 4)
        y_offset += item_spacing
        
        # 3. 绘制保存和恢复按钮
        button_width = int(screen_width * 0.25)
        center_x = screen_width // 2
        btn_spacing = 40
        save_x = center_x - button_width - btn_spacing // 2
        reset_x = center_x + btn_spacing // 2
        
        self._add_button_ui(y_offset, self.language_manager.get_text("settings", "save"), 5, save_x, button_width)
        self._add_button_ui(y_offset, self.language_manager.get_text("settings", "reset"), 6, reset_x, button_width)
        
        # 4. 绘制底部提示
        tip_text = self.language_manager.get_text("settings", "tips")
        tip_width = UIConfig.SMALL_FONT.size(tip_text)[0]
        self.ui_manager.add_component(Label(
            screen_width//2 - tip_width//2,
            screen_height - 40,
            tip_text,
            "small",
            UIConfig.COLOR_SETTINGS_TIPS
        ))

        # 5. 执行统一绘制
        self.ui_manager.draw()

    def _add_volume_ui(self, y_pos, label, volume, item_id):
        """向任务管理器添加音量控制UI"""
        screen_width, screen_height = self.screen.get_size()
        is_selected = self.selected_item == item_id
        label_color = UIConfig.COLOR_SETTINGS_ACTIVE if is_selected else UIConfig.COLOR_SETTINGS_TEXT
        
        # 添加标签
        self.ui_manager.add_component(Label(int(screen_width * 0.15), y_pos, label, "normal", label_color))
        
        # 添加进度条
        bar_x = int(screen_width * 0.45)
        self.ui_manager.add_component(ProgressBar(bar_x, y_pos + 5, int(screen_width * 0.4), 35, volume, is_selected))
        
        # 添加百分比
        vol_text = f"{int(volume * 100)}%"
        self.ui_manager.add_component(Label(bar_x + int(screen_width * 0.4) + int(screen_width * 0.03), y_pos, vol_text, "normal", UIConfig.COLOR_WHITE))

    def _add_selectbox_ui(self, y_pos, label, item_id):
        """向任务管理器添加选择框UI"""
        screen_width, screen_height = self.screen.get_size()
        is_selected = self.selected_item == item_id
        label_color = UIConfig.COLOR_SETTINGS_ACTIVE if is_selected else UIConfig.COLOR_SETTINGS_TEXT
        
        # 添加标签
        self.ui_manager.add_component(Label(int(screen_width * 0.15), y_pos, label, "normal", label_color))
        
        # 确定显示文本
        display_text = ""
        if item_id == 2: # 语言
            lang_map = {"zh": "中文", "en": "English"}
            display_text = lang_map.get(self.temp_language, self.temp_language)
        elif item_id == 3: # 分辨率
            display_text = f"{self.RESOLUTIONS[self.temp_resolution_index][0]}x{self.RESOLUTIONS[self.temp_resolution_index][1]}"
        elif item_id == 4: # 全屏
            display_text = "全屏" if self.temp_is_fullscreen else "窗口"
            if self.language_manager.language == "en":
                display_text = "Fullscreen" if self.temp_is_fullscreen else "Window"

        # 添加选择框
        arrows_icon = self.language_manager.get_text("settings", "arrows")
        self.ui_manager.add_component(SelectBox(int(screen_width * 0.45), y_pos, int(screen_width * 0.4), 40, display_text, is_selected, icon=arrows_icon))

    def _add_button_ui(self, y_pos, text, item_id, x, width):
        """向任务管理器添加按钮UI"""
        is_selected = self.selected_item == item_id
        self.ui_manager.add_component(Button(
            x, y_pos, width, 50, text, UIConfig.NORMAL_FONT,
            UIConfig.COLOR_BTN_BASE, 
            UIConfig.COLOR_BORDER_HIGHLIGHT if is_selected else UIConfig.COLOR_BAR_BORDER,
            UIConfig.COLOR_YELLOW,
            UIConfig.COLOR_SETTINGS_TEXT
        )).selected = is_selected

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
