import sys
sys.path.append(r'e:/Python learning/Python-learning/Python-learning')
import pygame
from Scenes.world_scene import WorldScene
from Scenes.Battle.BattleScene import BattleScene
from Scenes.Battle.models.entity import Entity

pygame.init()
screen = pygame.display.set_mode((320, 240))

# 1. 世界场景，按 b 检测
ws = WorldScene(screen)
evt_b = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_b})
res = ws.handle_input(evt_b)
print('WorldScene handle_input K_b ->', res)

# 2. 构造玩家和敌人实体（使用符合 Entity.__init__ 的字典）
player_data = {
    'name': 'Hero',
    'hp': 120,
    'mp': 30,
    'atk': 20,
    'm_atk': 5,
    'def': 8,
    'skills': []
}
enemy_data = {
    'name': 'Green Slime',
    'hp': 60,
    'mp': 0,
    'atk': 10,
    'm_atk': 0,
    'def': 3,
    'skills': []
}
player = Entity(player_data)
enemy = Entity(enemy_data)

# 3. 创建 BattleScene 并执行一次普通攻击
bs = BattleScene(screen, player, enemy)
print('Before attack: enemy.hp =', enemy.hp)
# 模拟按下回车/空格进行普通攻击
evt_ret = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})
bs.handle_input(evt_ret)
# process_action is called inside handle_input and sets action_result
# 直接调用 update 以让系统处理死亡检查
bs.update()
print('After attack: enemy.hp =', enemy.hp)
print('BattleSystem state:', bs.system.state)

pygame.quit()
