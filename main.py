import pygame
import sys
import random

from Scenes.DataManager import data_manager
# --- 优先初始化数据管理器 ---
data_manager.load_all()

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
from Scenes.Battle.data.monsters_config import MONSTERS_DATA, ENEMY_GROUPS
from Assets.Map.SceneManager import SceneManager
from Scenes.CharacterMenuScene import CharacterMenuScene

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
scene_manager = SceneManager(screen) # 初始化地图场景管理器

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
character_menu_scene = None

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
    global current_state, show_confirm_dialog, story_scene, current_game_state, screen, confirm_selected_index, is_new_game, loading_progress, current_slot_id, world_scene, battle_scene, character_menu_scene
    
    while True:
        dt = clock.tick(60) / 1000.0
        # 1. 事件处理 (仅处理输入，不处理逻辑更新)
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
                                
                                # 先同步数据再保存
                                if current_game_state and scene_manager.current_scene:
                                    scene = scene_manager.current_scene
                                    if hasattr(scene, 'player'):
                                        current_game_state.player_hp = scene.player.hp
                                        current_game_state.player_mp = scene.player.mp
                                        current_game_state.player_x = scene.player.x
                                        current_game_state.player_y = scene.player.y
                                        current_game_state.current_map = getattr(scene, 'map_name', 'testmap.tmx')
                                
                                current_game_state.current_scene = "WORLD"
                                save_scene.save_game(current_game_state, current_slot_id)
                                save_scene.refresh_slots()
                                show_confirm_dialog = False
                                # 直接返回世界，不重新加载场景（防止玩家位置重置）
                                current_state = "WORLD" 
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
                                # 【加载/新建自适应模式】
                                if save_scene.slot_data[selected_index] is None:
                                    # 槽位为空：在此启动新游戏流程
                                    is_new_game = True
                                    current_slot_id = save_scene.slots[selected_index]
                                    story_scene = StoryScene(screen, "冒险者")
                                    current_state = "STORY"
                                else:
                                    # 槽位有档：执行加载
                                    current_slot_id = save_scene.slots[selected_index]
                                    loaded_state = save_scene.load_game(current_slot_id)
                                    if loaded_state:
                                        current_game_state = loaded_state
                                        # 智能跳转
                                        target = current_game_state.current_scene
                                        if target == "WORLD":
                                            start_loading("WORLD")
                                        else:
                                            story_scene = StoryScene(screen, current_game_state.job_name)
                                            start_loading("STORY")
                            else:
                                # 【新建/覆盖模式】(当前已有 current_game_state)
                                if save_scene.slot_data[selected_index] is None:
                                    # 空槽位直接保存
                                    current_slot_id = save_scene.slots[selected_index]
                                    current_game_state.current_scene = "WORLD"
                                    save_scene.save_game(current_game_state, current_slot_id)
                                    save_scene.refresh_slots()
                                    start_loading("WORLD")
                                else:
                                    # 已有存档，确认覆盖
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

                # --- 世界地图：仅处理按键事件，不更新逻辑 ---
                elif current_state == "WORLD":
                    if scene_manager.current_scene:
                        res, extra = scene_manager.current_scene.handle_events(event)
                        if res == "MENU":
                            current_state = "MENU"
                        elif res == "CHARACTER_MENU":
                            character_menu_scene = CharacterMenuScene(screen, current_game_state, scene_manager.current_scene.player, initial_tab=extra)
                            current_state = "CHARACTER_MENU"
                        elif res == "BATTLE":
                            # 先将世界地图的玩家属性同步回存档对象
                            if current_game_state and scene_manager.current_scene and hasattr(scene_manager.current_scene, 'player'):
                                p = scene_manager.current_scene.player
                                current_game_state.player_hp = p.hp
                                current_game_state.player_mp = p.mp
                                current_game_state.level = p.level
                                current_game_state.exp = p.exp
                                current_game_state.max_hp = p.max_hp
                                current_game_state.max_mp = p.max_mp

                            job_key = current_game_state.job_name if current_game_state else "学生"
                            player_ent = Entity.from_job(job_key)
                            if player_ent and current_game_state:
                                player_ent.hp = current_game_state.player_hp
                                player_ent.max_hp = current_game_state.max_hp
                                player_ent.mp = current_game_state.player_mp
                                player_ent.max_mp = current_game_state.max_mp
                                player_ent.atk = current_game_state.attack
                                player_ent.m_atk = current_game_state.m_attack
                                player_ent.def_val = current_game_state.defense
                                player_ent.spd = current_game_state.spd
                            enemy_ent = Entity.from_monster("Slime_Green")
                            battle_scene = BattleScene(screen, player_ent, enemy_ent)
                            current_state = "BATTLE"
                        elif res == "SAVE":
                            if current_game_state and scene_manager.current_scene:
                                scene = scene_manager.current_scene
                                if hasattr(scene, 'player'):
                                    current_game_state.player_hp = scene.player.hp
                                    current_game_state.player_mp = scene.player.mp
                                    current_game_state.player_x = scene.player.x
                                    current_game_state.player_y = scene.player.y
                                    current_game_state.current_map = getattr(scene, 'map_name', 'testmap.tmx')
                            save_scene.refresh_slots()
                            current_state = "SAVE_SELECT"
                        elif res == "CHEST_OPEN":
                            if current_game_state:
                                item_id = extra.get("item_id")
                                if item_id:
                                    current_game_state.inventory.append(item_id)
                                    print(f"【系统】获得物品: {item_id} 已加入背包 (事件触发)")

                # --- 战斗界面：处理输入 ---
                elif current_state == "BATTLE":
                    if battle_scene:
                        res = battle_scene.handle_input(event)
                        if res == "WORLD":
                            # 如果战败，尝试回档
                            if battle_scene.system.state == "LOSS":
                                if current_slot_id is not None:
                                    print(f"【战败】正在加载存档槽位: {current_slot_id}")
                                    loaded_state = save_scene.load_game(current_slot_id)
                                    if loaded_state:
                                        current_game_state = loaded_state
                                        start_loading("WORLD")
                                        continue
                                
                                # 没档或回档失败则回菜单
                                current_state = "MENU"
                                continue

                            # 胜利或撤退的情况
                            current_state = "WORLD"
                            # 同步战斗后的属性到存档对象
                            if current_game_state and battle_scene.system:
                                current_game_state.player_hp = battle_scene.system.player.hp
                                current_game_state.player_mp = battle_scene.system.player.mp
                                
                                # 如果战斗胜利，增加经验值和金币
                                if battle_scene.system.state == "WIN":
                                    total_exp = getattr(battle_scene.system, "total_exp", 0)
                                    total_gold = getattr(battle_scene.system, "total_gold", 0)
                                    current_game_state.gain_exp(total_exp)
                                    current_game_state.gold += total_gold
                                    # 额外同步升级后的上限
                                    current_game_state.max_hp = battle_scene.system.player.max_hp
                                    current_game_state.max_mp = battle_scene.system.player.max_mp
                                    print(f"【结算】获得 {total_exp} EXP 和 {total_gold} Gold")
                                
                                # --- 核心修复：同步到世界地图的 Player 对象，让 HUD 实时更新 ---
                                if world_scene and hasattr(world_scene, 'player'):
                                    world_scene.player.hp = current_game_state.player_hp
                                    world_scene.player.mp = current_game_state.player_mp
                                    world_scene.player.level = current_game_state.level
                                    world_scene.player.exp = current_game_state.exp
                                    world_scene.player.max_hp = current_game_state.max_hp
                                    world_scene.player.max_mp = current_game_state.max_mp

                # --- 角色菜单界面 ---
                elif current_state == "CHARACTER_MENU":
                    if character_menu_scene:
                        res = character_menu_scene.handle_input(event)
                        if res == "WORLD":
                            current_state = "WORLD"



        # 1.5 逻辑更新逻辑 (移出事件循环，确保每帧只执行一次)
        if current_state == "WORLD":
             if scene_manager.current_scene:
                update_res, update_data = scene_manager.current_scene.update(dt)
                if update_res == "TELEPORT":
                    if current_game_state:
                        # 1. 记录当前地图的“离开点”
                        # 使用 safe_pos（触发传送前的坐标），避免回来时直接踩在传送阵上
                        old_map = current_game_state.current_map
                        safe_x, safe_y = update_data.get("safe_pos", (world_scene.player.x, world_scene.player.y))
                        current_game_state.map_return_points[old_map] = (safe_x, safe_y)
                        
                        # 2. 设置新地图
                        target_map = update_data["map"]
                        current_game_state.current_map = target_map
                        
                        # 3. 决定出生位置：如果是“返回”性质的传送且存过位置，则使用记录的位置
                        if update_data.get("is_return") and target_map in current_game_state.map_return_points:
                            rx, ry = current_game_state.map_return_points[target_map]
                            current_game_state.player_x, current_game_state.player_y = rx, ry
                            print(f"【传送】检测到返回属性，回到 {target_map} 的历史位置: ({rx}, {ry})")
                        else:
                            current_game_state.player_x = update_data["pos"][0]
                            current_game_state.player_y = update_data["pos"][1]
                        
                        start_loading("WORLD")
                elif update_res == "BATTLE":
                    # 同步世界地图玩家属性到存档对象
                    if current_game_state and scene_manager.current_scene and hasattr(scene_manager.current_scene, 'player'):
                        p = scene_manager.current_scene.player
                        current_game_state.player_hp = p.hp
                        current_game_state.player_mp = p.mp
                        current_game_state.level = p.level
                        current_game_state.exp = p.exp
                        current_game_state.max_hp = p.max_hp
                        current_game_state.max_mp = p.max_mp

                    group_id = update_data.get("enemy_group")
                    group_data = ENEMY_GROUPS.get(group_id)
                    
                    # 【核心容错】如果指定的群组不存在，随机选一个
                    if not group_data:
                        available_keys = list(ENEMY_GROUPS.keys())
                        if available_keys:
                            rand_key = random.choice(available_keys)
                            group_data = ENEMY_GROUPS[rand_key]
                            print(f"【警告】未找到群组ID '{group_id}'，随机切换到: {rand_key}")

                    if group_data and group_data.get("enemies"):
                        # 1. 加载玩家实体
                        job_key = current_game_state.job_name if current_game_state else "学生"
                        player_ent = Entity.from_job(job_key)
                        if player_ent and current_game_state:
                            player_ent.hp = current_game_state.player_hp
                            player_ent.max_hp = current_game_state.max_hp
                            player_ent.mp = current_game_state.player_mp
                            player_ent.max_mp = current_game_state.max_mp
                            player_ent.atk = current_game_state.attack
                            player_ent.m_atk = current_game_state.m_attack
                            player_ent.def_val = current_game_state.defense
                            player_ent.spd = current_game_state.spd
                        
                        # 2. 【改进】加载群组中定义的所有怪物实体
                        enemy_entities = []
                        for enemy_info in group_data["enemies"]:
                            monster_id = enemy_info["id"]
                            # 处理 ID 模糊匹配
                            actual_key = next((k for k in MONSTERS_DATA.keys() if k.lower() == monster_id.lower()), monster_id)
                            enemy_ent = Entity.from_monster(actual_key)
                            if enemy_ent:
                                # 赋予初始坐标（用于 UI 布局参考）
                                enemy_ent.pos = enemy_info.get("pos", (100, 200))
                                enemy_entities.append(enemy_ent)
                        
                        if enemy_entities:
                            battle_scene = BattleScene(screen, player_ent, enemy_entities)
                            current_state = "BATTLE"
                            print(f"【战斗】切入战斗场景，包含 {len(enemy_entities)} 个敌人")
                        else:
                            print(f"【错误】群组中没有找到有效的怪物定义")
        
        # 2. 状态逻辑更新 (主要是 LOADING)
        if current_state == "LOADING":
            loading_progress += 0.02
            if loading_progress >= 1.0:
                loading_progress = 1.0
                current_state = loading_target_state
                # 当进入 WORLD 状态时初始化场景
                if current_state == "WORLD":
                    job_name = current_game_state.job_name if current_game_state else "学生"
                    # 使用存档中的坐标和地图名
                    spawn_pos = None
                    if current_game_state and current_game_state.player_x is not None:
                        spawn_pos = (current_game_state.player_x, current_game_state.player_y)
                    
                    map_name = current_game_state.current_map if current_game_state else "testmap.tmx"
                    
                    # 获取存好的属性
                    initial_stats = {
                        "hp": current_game_state.player_hp if current_game_state else None,
                        "mp": current_game_state.player_mp if current_game_state else None,
                        "level": current_game_state.level if current_game_state else 1,
                        "exp": current_game_state.exp if current_game_state else 0
                    }
                    
                    world_scene = WorldScene(screen, scene_manager, job_name, map_name=map_name, spawn_pos=spawn_pos, initial_stats=initial_stats)
                    scene_manager.switch_scene(world_scene) # 同步到管理器中
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
            if scene_manager.current_scene:
                # 注意：update 已经在事件循环前面的状态逻辑中跑过了，这里不要再跑
                scene_manager.current_scene.draw()
            else:
                # 备用显示
                screen.fill((50, 50, 100))
                title = UIConfig.render_text("正在进入世界...", type="title")
                UIConfig.draw_center_text(screen, title, 250)
        elif current_state == "CHARACTER_MENU":
            if scene_manager.current_scene:
                 scene_manager.current_scene.draw()
            if character_menu_scene:
                character_menu_scene.draw()
        
        elif current_state == "BATTLE":
            if battle_scene:
                battle_scene.update()
                battle_scene.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()