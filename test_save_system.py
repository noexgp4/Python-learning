from Core.save_system import SaveManager
from Core.game_state import GameState
import os

def test_save_load():
    print("=== 开始测试存档系统 ===")
    
    # 1. 初始化
    manager = SaveManager()
    state = GameState()
    
    # 2. 修改一些数据
    print("原始数据 -> 玩家Level:", state.level, "金币:", state.gold)
    state.level = 5
    state.gold = 999
    state.inventory.append("Sword")
    print("修改后数据 -> 玩家Level:", state.level, "金币:", state.gold, "物品:", state.inventory)
    
    # 3. 保存
    slot_id = 999 # 使用一个测试槽位
    print(f"正在保存到槽位 {slot_id}...")
    success = manager.save_game(state, slot_id)
    if not success:
        print("测试失败：保存失败")
        return

    # 4. 读取
    print(f"正在从槽位 {slot_id} 读取...")
    loaded_state = manager.load_game(slot_id)
    
    if loaded_state:
        print("读取数据 -> 玩家Level:", loaded_state.level, "金币:", loaded_state.gold, "物品:", loaded_state.inventory)
        
        # 5. 验证
        if loaded_state.level == 5 and loaded_state.gold == 999 and "Sword" in loaded_state.inventory:
            print(">>> 测试通过！数据一致。")
        else:
            print(">>> 测试失败！数据不一致。")
    else:
        print("测试失败：读取返回 None")

    print("=== 测试结束 ===")

if __name__ == "__main__":
    test_save_load()
