import pygame

class Camera:
    """相机系统，用于跟随玩家并显示地图的一部分"""
    
    def __init__(self, screen_width, screen_height, map_width, map_height, zoom=1.0):
        """
        初始化相机
        
        Args:
            screen_width: 屏幕宽度
            screen_height: 屏幕高度
            map_width: 地图宽度（像素）
            map_height: 地图高度（像素）
            zoom: 缩放比例（>1表示放大，<1表示缩小）
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height
        self.zoom = zoom
        
        # 相机位置（左上角坐标）
        self.x = 0
        self.y = 0
        
        # 视口大小（缩放后的视野范围）
        self.viewport_width = screen_width / zoom
        self.viewport_height = screen_height / zoom
    
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
        
        # 让目标居中（考虑缩放后的视口）
        self.x = target_center_x - self.viewport_width / 2
        self.y = target_center_y - self.viewport_height / 2
        
        # 限制相机不要超出地图边界
        self.x = max(0, min(self.x, self.map_width - self.viewport_width))
        self.y = max(0, min(self.y, self.map_height - self.viewport_height))
    
    def apply(self, surface, map_surface):
        """
        应用相机效果，绘制地图的可见部分（支持缩放）
        
        Args:
            surface: 屏幕Surface
            map_surface: 地图Surface
        """
        # 定义相机在地图上的视口，确保不超出地图边界
        camera_x = max(0, min(self.x, self.map_width - self.viewport_width))
        camera_y = max(0, min(self.y, self.map_height - self.viewport_height))
        camera_width = min(self.viewport_width, self.map_width - camera_x)
        camera_height = min(self.viewport_height, self.map_height - camera_y)
        
        camera_rect = pygame.Rect(
            int(camera_x),
            int(camera_y),
            int(camera_width),
            int(camera_height)
        )
        
        if self.zoom == 1.0:
            # 无缩放时直接绘制
            surface.blit(map_surface, (0, 0), camera_rect)
        else:
            # 有缩放时，先裁剪后再缩放
            try:
                cropped = map_surface.subsurface(camera_rect)
                scaled = pygame.transform.scale(
                    cropped,
                    (self.screen_width, self.screen_height)
                )
                surface.blit(scaled, (0, 0))
            except ValueError:
                # 如果subsurface失败，直接绘制整个地图
                scaled = pygame.transform.scale(
                    map_surface,
                    (int(self.map_width * self.zoom), int(self.map_height * self.zoom))
                )
                surface.blit(scaled, (-int(camera_x * self.zoom), -int(camera_y * self.zoom)))
    
    def set_zoom(self, zoom):
        """
        设置缩放比例
        
        Args:
            zoom: 缩放比例（>1表示放大，<1表示缩小）
        """
        if zoom > 0:
            self.zoom = zoom
            self.viewport_width = self.screen_width / zoom
            self.viewport_height = self.screen_height / zoom
            
            # 重新限制相机边界，确保视口不超出地图
            self.x = max(0, min(self.x, self.map_width - self.viewport_width))
            self.y = max(0, min(self.y, self.map_height - self.viewport_height))
    
    def get_offset(self):
        """获取相机偏移量，用于绘制其他对象"""
        return (-self.x, -self.y)
