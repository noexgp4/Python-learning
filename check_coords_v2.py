import pytmx
import pygame
import sys

sys.stdout.reconfigure(encoding='utf-8')

pygame.init()
pygame.display.set_mode((1,1), pygame.NOFRAME)

map_path = r"e:\Python learning\Python-learning\Python-learning\Assets\Map\testmap.tmx"
tmx_data = pytmx.load_pygame(map_path, pixelalpha=True)

print("--- 检查所有物件层 ---")
for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledObjectGroup):
        print(f"图层: {layer.name}")
        for obj in layer:
            if hasattr(obj, 'gid') and obj.gid:
                print(f"  [TileObj] ID={obj.id}, GID={obj.gid}, x={obj.x}, y={obj.y}, h={obj.height}")
            elif layer.name == "Collision":
                print(f"  [RectObj] ID={obj.id}, x={obj.x}, y={obj.y}, h={obj.height}")

pygame.quit()
