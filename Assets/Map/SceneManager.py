import pygame

class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.current_scene = None
        self.is_running = True

    def switch_scene(self, new_scene):
        """切换场景的核心方法"""
        # 如果有旧场景，可以在这里执行清理工作
        self.current_scene = new_scene

    def run(self):
        """主循环交给管理器调度"""
        clock = pygame.time.Clock()
        while self.is_running:
            dt = clock.tick(60) / 1000.0  # 统一计算 delta time
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.is_running = False
                
                # 将事件传递给当前场景
                if self.current_scene:
                    self.current_scene.handle_events(event)

            # 更新当前场景逻辑
            if self.current_scene:
                self.current_scene.update(dt)

            # 渲染当前场景
            if self.current_scene:
                self.current_scene.draw(self.screen)
            
            pygame.display.flip()