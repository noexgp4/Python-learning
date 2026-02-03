import pytmx
import pygame

pygame.init()
pygame.display.set_mode((1,1), pygame.NOFRAME)

map_path = r"e:\Python learning\Python-learning\Python-learning\Assets\Map\testmap.tmx"
tmx_data = pytmx.load_pygame(map_path, pixelalpha=True)

print("--- 检查 '物件层 6' 中的物件坐标 ---")
# 找出 '物件层 6'
for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == '物件层 6':
        for obj in layer:
            print(f"物件 ID={obj.id}, Name={obj.name}, GID={getattr(obj, 'gid', 'None')}")
            print(f"  原始坐标 (x, y): ({obj.x}, {obj.y})")
            print(f"  尺寸 (w, h): ({obj.width}, {obj.height})")
            if hasattr(obj, 'gid') and obj.gid:
                print(f"  [提示] 这是一个图块物件。")
                print(f"  如果 y 是底部，则 y - height = {obj.y - obj.height}")
                print(f"  如果 y 已经是顶部，则 y 就是顶部坐标。")

pygame.quit()
