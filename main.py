import pygame
import sys
import random
from Scenes.menu import MainMenu
from Scenes.settings import SettingsScene
from Core.audio import AudioManager
from Core.save_system import SaveManager
from Core.game_state import GameState
from Core.game_config import CLASSES
from Core.game_config import ClassSelectScene
from Scenes.story import StoryScene
from Scenes.text import UIConfig, Panel, Label, ProgressBar
from Scenes.UIManager import UIManager
from Scenes.world_scene import WorldScene
from Scenes.Battle.BattleScene import BattleScene
from Scenes.Battle.models.entity import Entity
from Language.language_manager import LanguageManager

# --- 初始化 Pygame ---
pygame.init()

audio_manager = AudioManager()
language_manager = LanguageManager("zh")
pygame.language_manager = language_manager

# --- 屏幕初始化 ---
temp_screen = pygame.display.set_mode((800, 600))
settings_scene = SettingsScene(temp_screen, audio_manager, language_manager)
screen = settings_scene.apply_resolution_change()
settings_scene.screen = screen
pygame.display.set_caption("像素勇者")
pygame.key.stop_text_input() # 关键：禁用 IME 文本输入，防止按键拦截

clock = pygame.time.Clock()

# --- 实例创建 ---
menu_scene = MainMenu(screen, language_manager)
menu_scene.set_sfx_callback(audio_manager.play_sfx)
save_scene = SaveManager(screen)
class_select_scene = ClassSelectScene(screen)
global_ui_manager = UIManager(screen)

# --- 游戏全局变量 ---
current_state = "MENU"
current_game_state = None
story_scene = None
world_scene = None
battle_scene = None
show_confirm_dialog = False
confirm_selected_index = 0
is_new_game = False
current_slot_id = None  # 记录当前正在使用的存档槽位

# --- 加载页专用变量 ---
loading_progress = 0
loading_target_state = "MENU"
loading_tips = [
    "温馨提示：多喝水对身体好，冒险也是。",
    "传闻中，程序员职业拥有翻转世界（镜像）的能力。",
    "进度条其实是用来骗你的时间感，我也一样。",
    "勇者在战斗中如果血量不足，记得查看背包。",
    "装备的边框颜色通常代表了它的稀有程度。"
]
current_tip = ""

def start_loading(target_state):
    """启动加载界面"""
    global current_state, loading_progress, loading_target_state, current_tip
    loading_progress = 0
    loading_target_state = target_state
    current_tip = random.choice(loading_tips)
    current_state = "LOADING"

def main():
    global current_state, show_confirm_dialog, story_scene, current_game_state, screen, confirm_selected_index, is_new_game, loading_progress, current_slot_id, world_scene, battle_scene
    
    while True:
        # 1. 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # --- 主菜单 ---
                if current_state == "MENU":
                    if event.key == pygame.K_UP:
                        menu_scene.update_selection(-1)
                    elif event.key == pygame.K_DOWN:
                        menu_scene.update_selection(1)
                    elif event.key == pygame.K_RETURN:
                        menu_scene.play_button_sound()
                        if menu_scene.selected_index == 0:   # 开始冒险
                            is_new_game = True
                            story_scene = StoryScene(screen, "冒险者")
                            current_state = "STORY"
                        elif menu_scene.selected_index == 1: # 加载存档
                            is_new_game = False
                            current_game_state = None  # 重置状态，确保存档界面进入“加载”模式
                            save_scene.refresh_slots()
                            current_state = "SAVE_SELECT"
                        elif menu_scene.selected_index == 2: # 游戏设置
                            settings_scene.enter_settings()
                            current_state = "SETTINGS"
                        elif menu_scene.selected_index == 3: # 退出游戏
                            pygame.quit()
                            sys.exit()

                # --- 剧情界面 ---
                elif current_state == "STORY":
                    if story_scene:
                        result = story_scene.handle_input(event)
                        if result == "WORLD":
                            if is_new_game:
                                current_state = "CLASS_SELECT"
                            else:
                                start_loading("WORLD")

                # --- 职业选择 ---
                elif current_state == "CLASS_SELECT":
                    if event.key == pygame.K_UP:
                        class_select_scene.update_selection(-1)
                    elif event.key == pygame.K_DOWN:
                        class_select_scene.update_selection(1)
                    elif event.key == pygame.K_RETURN:
                        selected_class = class_select_scene.class_names[class_select_scene.selected_index]
                        current_game_state = GameState(job_name=selected_class)
                        # 选完职业后直接进入地图加载页
                        start_loading("WORLD")
                    elif event.key == pygame.K_ESCAPE:
                        current_state = "MENU"

                # --- 存档选择 ---
                elif current_state == "SAVE_SELECT":
                    if show_confirm_dialog:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            confirm_selected_index = 1 - confirm_selected_index
                        elif event.key == pygame.K_RETURN:
                            if confirm_selected_index == 0: # 确认覆盖
                                current_slot_id = save_scene.get_selected_slot()
                                # 保存前更新当前场景状态
                                current_game_state.current_scene = "WORLD"
                                save_scene.save_game(current_game_state, current_slot_id)
                                save_scene.refresh_slots()
                                show_confirm_dialog = False
                                start_loading("WORLD")
                            else:
                                show_confirm_dialog = False
                        elif event.key == pygame.K_ESCAPE:
                            show_confirm_dialog = False
                    else:
                        if event.key == pygame.K_UP:
                            save_scene.update_selection(-1)
                        elif event.key == pygame.K_DOWN:
                            save_scene.update_selection(1)
                        elif event.key == pygame.K_ESCAPE:
                            current_state = "MENU"
                        elif event.key == pygame.K_DELETE:
                            save_scene.delete_save(save_scene.selected_index)
                        elif event.key == pygame.K_RETURN:
                            selected_index = save_scene.selected_index
                            if current_game_state is None:
                                    current_slot_id = save_scene.slots[selected_index]
                                    current_game_state = save_scene.load_game(current_slot_id)
                                    if current_game_state:
                                        # 智能跳转：如果存档记录在 WORLD，则直接进入地图
                                        target = current_game_state.current_scene
                                        if target == "WORLD":
                                            start_loading("WORLD")
                                        else:
                                            story_scene = StoryScene(screen, current_game_state.job_name)
                                            start_loading("STORY")
                            else:
                                # 新建建档逻辑
                                if save_scene.slot_data[selected_index] is None:
                                    current_slot_id = save_scene.slots[selected_index]
                                    save_scene.save_game(current_game_state, current_slot_id)
                                    save_scene.refresh_slots()
                                    start_loading("WORLD")
                                else:
                                    show_confirm_dialog = True
                                    confirm_selected_index = 1

                # --- 设置界面 ---
                elif current_state == "SETTINGS":
                    if event.key == pygame.K_UP:
                        settings_scene.update_selection(-1)
                    elif event.key == pygame.K_DOWN:
                        settings_scene.update_selection(1)
                    elif event.key == pygame.K_LEFT:
                        settings_scene.update_volume(-1)
                    elif event.key == pygame.K_RIGHT:
                        settings_scene.update_volume(1)
                    elif event.key == pygame.K_RETURN:
                        if settings_scene.selected_item == 5:
                            settings_scene.save_config()
                            settings_scene.apply_resolution_change()
                            screen = settings_scene.screen
                        elif settings_scene.selected_item == 6:
                            settings_scene.reset_to_default()
                    elif event.key == pygame.K_ESCAPE:
                        settings_scene.cancel_settings()
                        current_state = "MENU"

                # --- 世界地图 ---
                elif current_state == "WORLD":
                    if world_scene:
                        res = world_scene.handle_input(event)
                        if res == "MENU":
                            current_state = "MENU"
                        elif res == "BATTLE":
                            # 1. 根据存档中的职业名称初始化玩家实体
                            job_key = current_game_state.job_name if current_game_state else "学生"
                            player_ent = Entity.from_job(job_key)
                            
                            # 2. 从存档同步实时属性
                            if player_ent and current_game_state:
                                player_ent.hp = current_game_state.player_hp
                                player_ent.mp = current_game_state.player_mp
                            
                            # 3. 初始化怪物实体
                            enemy_ent = Entity.from_monster("Slime_Green")
                            
                            battle_scene = BattleScene(screen, player_ent, enemy_ent)
                            current_state = "BATTLE"
                        elif res == "SAVE":
                            # 进入存档选择界面进行保存
                            save_scene.refresh_slots()
                            current_state = "SAVE_SELECT"

                # --- 战斗界面 ---
                elif current_state == "BATTLE":
                    if battle_scene:
                        res = battle_scene.handle_input(event)
                        if res == "WORLD":
                            current_state = "WORLD"
                            # 1. 同步战斗后的属性到存档对象
                            if current_game_state:
                                current_game_state.player_hp = battle_scene.system.player.hp
                                current_game_state.player_mp = battle_scene.system.player.mp
                                # 取消自动存档，仅同步数值

        # 2. 状态逻辑更新 (主要是 LOADING)
        if current_state == "LOADING":
            loading_progress += 0.02
            if loading_progress >= 1.0:
                loading_progress = 1.0
                current_state = loading_target_state
                # 当进入 WORLD 状态时初始化场景
                if current_state == "WORLD":
                    world_scene = WorldScene(screen)
                elif current_state == "BATTLE":
                    # 可以在这里初始化，但我们目前在事件中手动初始化了
                    pass

        # 3. 渲染
        if current_state == "MENU":
            menu_scene.draw()
        elif current_state == "STORY":
            if story_scene: story_scene.draw()
        elif current_state == "CLASS_SELECT":
            class_select_scene.draw()
        elif current_state == "SAVE_SELECT":
            save_scene.draw()
            if show_confirm_dialog:
                global_ui_manager.clear()
                global_ui_manager.add_component(Panel(0, 0, screen.get_width(), screen.get_height(), (0, 0, 0, 180), border_radius=0))
                dw, dh = 500, 200
                dx, dy = (screen.get_width() - dw)//2, (screen.get_height() - dh)//2
                global_ui_manager.add_component(Panel(dx, dy, dw, dh, (40, 40, 40, 255), UIConfig.COLOR_YELLOW, 3, 15))
                msg_text = "存档已存在，是否覆盖？"
                mw = UIConfig.NORMAL_FONT.size(msg_text)[0]
                global_ui_manager.add_component(Label((screen.get_width() - mw)//2, dy + 40, msg_text, "normal", UIConfig.COLOR_WHITE))
                btns = ["是", "否"]
                for i, btn_text in enumerate(btns):
                    is_btn_selected = (confirm_selected_index == i)
                    btn_text_color = UIConfig.COLOR_PALETTE_BLACK if is_btn_selected else UIConfig.COLOR_GRAY
                    bx = dx + 150 + i * 150
                    by = dy + 120
                    if is_btn_selected:
                        global_ui_manager.add_component(Panel(bx - 10, by - 5, 60, 45, (*UIConfig.COLOR_YELLOW, 255), UIConfig.COLOR_YELLOW, 2, 5))
                    global_ui_manager.add_component(Label(bx, by, btn_text, "normal", btn_text_color))
                global_ui_manager.draw()
        elif current_state == "LOADING":
            screen.fill((20, 20, 20)) # 使用深黑灰色作为加载底色
            # 绘制加载页文字
            lt_text = "资源加载中..."
            lt_width = UIConfig.TITLE_FONT.size(lt_text)[0]
            UIConfig.draw_center_text(screen, UIConfig.render_text(lt_text, "title", UIConfig.COLOR_YELLOW), screen.get_height() // 2 - 80)
            
            # 使用现有的 ProgressBar 组件渲染进度条
            bar_w = 500
            bar_x = (screen.get_width() - bar_w) // 2
            bar_y = screen.get_height() // 2 + 20
            loading_bar = ProgressBar(bar_x, bar_y, bar_w, 20, loading_progress, is_selected=True)
            loading_bar.draw(screen)
            
            # 绘制随机提示
            tip_surf = UIConfig.render_text(current_tip, "small", (150, 150, 150))
            UIConfig.draw_center_text(screen, tip_surf, screen.get_height() - 80)
            
        elif current_state == "SETTINGS":
            settings_scene.draw()
        elif current_state == "WORLD":
            if world_scene:
                world_scene.update()
                world_scene.draw()
            else:
                # 备用显示
                screen.fill((50, 50, 100))
                title = UIConfig.render_text("正在进入世界...", type="title")
                UIConfig.draw_center_text(screen, title, 250)
        
        elif current_state == "BATTLE":
            if battle_scene:
                battle_scene.update()
                battle_scene.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()