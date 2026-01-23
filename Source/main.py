import pygame
import sys
from menu import MainMenu  # 从 menu.py 导入 MainMenu 类
from settings import SettingsScene  # 导入设置类

# 初始化
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock() # 控制游戏帧率

# 创建菜单实例
menu_scene = MainMenu(screen)
settings_scene = SettingsScene(screen)  # 创建设置实例（会加载背景音乐）
menu_scene.set_sfx_callback(settings_scene.play_sfx)  # 将音效播放器注入菜单
current_state = "MENU"
print(f"游戏初始化完成，当前背景音乐音量: {int(settings_scene.bgm_volume*100)}%")

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
                            current_state = "BATTLE"
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
                        if settings_scene.selected_item == 2:  # 保存设置
                            settings_scene.save_config()
                        elif settings_scene.selected_item == 3:  # 恢复默认
                            settings_scene.reset_to_default()
                    elif event.key == pygame.K_ESCAPE:    # 按 ESC 返回菜单
                        settings_scene.cancel_settings()  # 取消设置改动
                        current_state = "MENU"
                    
        # 2. 根据状态渲染不同的文件内容
        if current_state == "MENU":
            menu_scene.draw()
        elif current_state == "BATTLE":
            # 这里以后可以调用 battle_scene.draw()
            screen.fill((50, 0, 0)) # 暂时用红色代表战斗界面
        elif current_state == "SETTINGS":
            settings_scene.draw()  # 绘制设置界面
            
        pygame.display.flip()
        clock.tick(60) # 限制每秒 60 帧，防止 CPU 占用过高

if __name__ == "__main__":
    main()