import pygame
import sys
from Scenes.menu import MainMenu  # 从 menu.py 导入 MainMenu 类
from Scenes.settings import SettingsScene  # 导入设置类
from Core.audio import AudioManager
from Core.save_system import SaveManager  # 导入存档管理类
from Core.game_state import GameState # 导入游戏状态类
from Core.game_config import ClassSelectScene # 导入职业选择类
from Scenes.story import StoryScene # 导入剧情类
from Scenes.text import UIConfig, Panel, Label # 导入 UI 配置
from Scenes.UIManager import UIManager

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

# 创建职业选择实例
class_select_scene = ClassSelectScene(screen)

# 剧情实例 (动态创建)
story_scene = None
current_game_state = None

# 覆盖存档确认状态
show_confirm_dialog = False
confirm_selected_index = 0 # 0为是，1为否
global_ui_manager = UIManager(screen)

current_state = "MENU"
print(f"游戏初始化完成，分辨率: {screen.get_size()}，当前背景音乐音量: {int(settings_scene.bgm_volume*100)}%")

def main():
    global current_state, show_confirm_dialog, story_scene, current_game_state, screen, confirm_selected_index
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
                
                elif current_state == "STORY":
                    if story_scene:
                        result = story_scene.handle_input(event)
                        if result == "BATTLE":
                            current_state = "BATTLE"

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
                    elif event.key == pygame.K_DELETE:
                        # 删除选中的存档
                        save_scene.delete_save(save_scene.selected_index)
                    elif event.key == pygame.K_RETURN:
                        selected_index = save_scene.selected_index
                        # 如果正在显示确认对话框
                        if show_confirm_dialog:
                            if confirm_selected_index == 0:
                                # 确认覆盖
                                print(f"正在覆盖槽位 {selected_index + 1}...")
                                new_game = GameState()
                                save_scene.save_game(new_game, save_scene.slots[selected_index])
                                save_scene.refresh_slots()
                                show_confirm_dialog = False
                                current_state = "CLASS_SELECT"
                            else:
                                # 选择否，取消
                                show_confirm_dialog = False
                        else:
                            # 判断是否已有存档
                            if save_scene.slot_data[selected_index] is None:
                                # 创建空档
                                print(f"正在槽位 {selected_index + 1} 创建新存档...")
                                new_game = GameState()
                                save_scene.save_game(new_game, save_scene.slots[selected_index])
                                save_scene.refresh_slots()
                                current_state = "CLASS_SELECT"
                            else:
                                # 已有存档
                                show_confirm_dialog = True
                                confirm_selected_index = 1 # 默认为“否”更安全
                    
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        if show_confirm_dialog:
                            confirm_selected_index = 1 - confirm_selected_index # 切换 0 和 1
                    
                    elif event.key == pygame.K_ESCAPE:
                        if show_confirm_dialog:
                            show_confirm_dialog = False
                        else:
                            current_state = "MENU"
                    
                elif current_state == "CLASS_SELECT":
                    if event.key == pygame.K_UP:
                        class_select_scene.update_selection(-1)
                    elif event.key == pygame.K_DOWN:
                        class_select_scene.update_selection(1)
                    elif event.key == pygame.K_RETURN:
                        # 确认选择职业
                        selected_class = class_select_scene.class_names[class_select_scene.selected_index]
                        print(f"已选择职业: {selected_class}")
                        
                        # 初始化 GameState 并保存
                        current_game_state = GameState(job_name=selected_class)
                        selected_slot = save_scene.slots[save_scene.selected_index]
                        save_scene.save_game(current_game_state, selected_slot)
                        
                        # 初始化剧情
                        story_scene = StoryScene(screen, selected_class)
                        current_state = "STORY"
                    elif event.key == pygame.K_ESCAPE:
                        current_state = "SAVE_SELECT"
                    
        # 2. 根据状态渲染不同的内容
        if current_state == "MENU":
            menu_scene.draw()
        elif current_state == "SAVE_SELECT":
            # 如果有 save_scene.draw() 则调用
            if 'save_scene' in locals() or 'save_scene' in globals():
                save_scene.draw()
                
            # 如果处于确认状态，使用 global_ui_manager 绘制弹窗
            if show_confirm_dialog:
                global_ui_manager.clear()
                # 1. 昏暗背景 (Panel 支持半透明)
                global_ui_manager.add_component(Panel(0, 0, screen.get_width(), screen.get_height(), (0, 0, 0, 180), border_radius=0))
                
                # 2. 对话框本体
                dw, dh = 500, 200
                dx, dy = (screen.get_width() - dw)//2, (screen.get_height() - dh)//2
                global_ui_manager.add_component(Panel(dx, dy, dw, dh, (40, 40, 40, 255), UIConfig.COLOR_YELLOW, 3, 15))
                
                # 3. 文字
                msg_text = "存档已存在，是否覆盖？"
                mw = UIConfig.NORMAL_FONT.size(msg_text)[0]
                global_ui_manager.add_component(Label((screen.get_width() - mw)//2, dy + 40, msg_text, "normal", UIConfig.COLOR_WHITE))
                
                # 4. 按钮
                btns = ["是", "否"]
                for i, btn_text in enumerate(btns):
                    is_btn_selected = (confirm_selected_index == i)
                    btn_color = UIConfig.COLOR_YELLOW if is_btn_selected else (150, 150, 150)
                    bx = dx + 150 + i * 150
                    by = dy + 120
                    
                    if is_btn_selected:
                        # 选中框效果可以用 Panel 的透明背景 + 描边模拟
                        global_ui_manager.add_component(Panel(bx - 10, by - 5, 60, 45, (0,0,0,0), UIConfig.COLOR_YELLOW, 2, 5))
                    
                    global_ui_manager.add_component(Label(bx, by, btn_text, "normal", btn_color))
                
                global_ui_manager.draw()
        elif current_state == "SETTINGS":
            settings_scene.draw()  # 绘制设置界面
        elif current_state == "CLASS_SELECT":
            class_select_scene.draw()  # 绘制职业选择界面
        elif current_state == "STORY":
            if story_scene:
                story_scene.draw()
        elif current_state == "BATTLE":
            screen.fill((50, 50, 100)) # 战斗界面占位
            title = UIConfig.render_text("战斗关卡加载中...", type="title")
            UIConfig.draw_center_text(screen, title, 250)
            
        pygame.display.flip()
        clock.tick(60) # 限制每秒 60 帧，防止 CPU 占用过高

if __name__ == "__main__":
    main()