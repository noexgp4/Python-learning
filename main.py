import pygame
import sys
from Scenes.menu import MainMenu  # 从 menu.py 导入 MainMenu 类
from Scenes.settings import SettingsScene  # 导入设置类
from Core.audio import AudioManager
from Core.save_system import SaveManager  # 导入存档管理类
from Core.game_state import GameState # 导入游戏状态类

# 初始化 pygame
# 初始化 pygame
pygame.init()

from Core.audio import AudioManager
from Language.language_manager import LanguageManager

# 初始化 pygame
pygame.init()

audio_manager = AudioManager()
language_manager = LanguageManager("zh")  # 默认语言为中文

# 先创建一个临时屏幕用于初始化 SettingsScene
temp_screen = pygame.display.set_mode((800, 600))

# 创建设置实例（会加载保存的分辨率配置）
settings_scene = SettingsScene(temp_screen, audio_manager, language_manager)

# 根据加载的分辨率配置创建实际屏幕
screen = settings_scene.apply_resolution_change()

# 更新屏幕引用
settings_scene.screen = screen
pygame.display.set_caption("像素勇者")

clock = pygame.time.Clock() # 控制游戏帧率

# 创建菜单实例
menu_scene = MainMenu(screen, language_manager)
menu_scene.set_sfx_callback(audio_manager.play_sfx)  # 将音效播放器注入菜单

# 创建存档实例
save_scene = SaveManager(screen) 

current_state = "MENU"
print(f"游戏初始化完成，分辨率: {screen.get_size()}，当前背景音乐音量: {int(settings_scene.bgm_volume*100)}%")

def main():
    global current_state
    while True:
        # 1. 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if current_state == "MENU":
                    if event.key == pygame.K_UP:
                        menu_scene.update_selection(-1) # 向上选
                    elif event.key == pygame.K_DOWN:
                        menu_scene.update_selection(1)  # 向下选
                    elif event.key == pygame.K_RETURN:  # 按下回车键
                        menu_scene.play_button_sound()  # 播放按钮音效
                        # 判断选中的是哪个选项
                        if menu_scene.selected_index == 0:   # "开始冒险"
                            save_scene.refresh_slots()     # 每次进入前刷新数据
                            current_state = "SAVE_SELECT"
                        elif menu_scene.selected_index == 1: # "加载存档"
                            current_state = "LOADING"
                        elif menu_scene.selected_index == 2: # "游戏设置"
                            settings_scene.enter_settings()  # 进入设置，重新加载保存的值
                            current_state = "SETTINGS"
                        elif menu_scene.selected_index == 3: # "退出游戏"
                            pygame.quit()
                            sys.exit()

                # 设置界面控制
                elif current_state == "SETTINGS":
                    if event.key == pygame.K_UP:
                        settings_scene.update_selection(-1)  # 向上选
                    elif event.key == pygame.K_DOWN:
                        settings_scene.update_selection(1)   # 向下选
                    elif event.key == pygame.K_LEFT:
                        settings_scene.update_volume(-1)  # 减小音量
                    elif event.key == pygame.K_RIGHT:
                        settings_scene.update_volume(1)   # 增加音量
                    elif event.key == pygame.K_RETURN:    # 按下回车键
                        # 判断选中的是哪个选项
                        if settings_scene.selected_item == 5:  # 保存设置
                            settings_scene.save_config()
                            settings_scene.apply_resolution_change()  # 应用分辨率变更
                            screen = settings_scene.screen  # 更新屏幕对象
                        elif settings_scene.selected_item == 6:  # 恢复默认
                            settings_scene.reset_to_default()
                    elif event.key == pygame.K_ESCAPE:    # 按 ESC 返回菜单
                        settings_scene.cancel_settings()  # 取消设置改动
                        current_state = "MENU"
                
                elif current_state == "SAVE_SELECT":
                    if event.key == pygame.K_UP: 
                        save_scene.update_selection(-1)
                    elif event.key == pygame.K_DOWN: 
                        save_scene.update_selection(1)
                    elif event.key == pygame.K_ESCAPE: 
                        current_state = "MENU"
                    elif event.key == pygame.K_RETURN:
                        selected_index = save_scene.selected_index
                        # 判断是否已有存档
                        if save_scene.slot_data[selected_index] is None:
                            # 创建新存档
                            print(f"正在槽位 {selected_index + 1} 创建新存档...")
                            new_game = GameState()
                            save_scene.save_game(new_game, save_scene.slots[selected_index])
                            save_scene.refresh_slots() # 刷新显示
                            current_state = "BATTLE" # 进入游戏
                        else:
                            # 加载存档
                            print(f"加载槽位 {selected_index + 1} 的存档")
                            # 这里可以添加加载逻辑，比如 game_manager.load(save_scene.slots[selected_index])
                            current_state = "BATTLE"
                    
        # 2. 根据状态渲染不同的内容
        if current_state == "MENU":
            menu_scene.draw()
        elif current_state == "SAVE_SELECT":
            # 如果有 save_scene.draw() 则调用
            if 'save_scene' in locals() or 'save_scene' in globals():
                save_scene.draw()
        elif current_state == "SETTINGS":
            settings_scene.draw()  # 绘制设置界面
            
        pygame.display.flip()
        clock.tick(60) # 限制每秒 60 帧，防止 CPU 占用过高

if __name__ == "__main__":
    main()