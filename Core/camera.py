import pygame

class Camera:
    """相机系统，用于跟随玩家并显示地图的一部分"""
    
    def __init__(self, screen_width, screen_height, map_width, map_height):
        """
        初始化相机
        
        Args:
            screen_width: 屏幕宽度
            screen_height: 屏幕高度
            map_width: 地图宽度（像素）
            map_height: 地图高度（像素）
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height
        
        # 相机位置（左上角坐标）
        self.x = 0
        self.y = 0
    
    def update(self, target_x, target_y, target_width=32, target_height=32):
        """
        更新相机位置，使目标居中显示
        
        Args:
            target_x: 目标X坐标
            target_y: 目标Y坐标
            target_width: 目标宽度
            target_height: 目标高度
        """
        # 计算目标的中心
        target_center_x = target_x + target_width // 2
        target_center_y = target_y + target_height // 2
        
        # 让目标居中
        self.x = target_center_x - self.screen_width // 2
        self.y = target_center_y - self.screen_height // 2
        
        # 限制相机不要超出地图边界
        self.x = max(0, min(self.x, self.map_width - self.screen_width))
        self.y = max(0, min(self.y, self.map_height - self.screen_height))
    
    def apply(self, surface, map_surface):
        """
        应用相机效果，绘制地图的可见部分
        
        Args:
            surface: 屏幕Surface
            map_surface: 地图Surface
        """
        # 绘制地图的一部分到屏幕
        surface.blit(
            map_surface,
            (0, 0),
            pygame.Rect(self.x, self.y, self.screen_width, self.screen_height)
        )
    
    def get_offset(self):
        """获取相机偏移量，用于绘制其他对象"""
        return (-self.x, -self.y)
