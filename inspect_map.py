import pytmx
import os

def inspect_tmx(filename):
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    tmx_data = pytmx.load_pygame(filename)
    print(f"Inspecting: {filename}")
    print(f"Total Layers: {len(tmx_data.layers)}")
    
    for i, layer in enumerate(tmx_data.layers):
        l_type = "TileLayer" if isinstance(layer, pytmx.TiledTileLayer) else "ObjectGroup" if isinstance(layer, pytmx.TiledObjectGroup) else "Unknown"
        l_class = getattr(layer, 'class', 'None')
        l_visible = getattr(layer, 'visible', 'Unknown')
        print(f"Layer {i}: Name='{layer.name}', Type={l_type}, Class='{l_class}', Visible={l_visible}")
        
        if isinstance(layer, pytmx.TiledObjectGroup):
            print(f"  Objects in '{layer.name}':")
            for obj in layer:
                obj_name = getattr(obj, 'name', 'None')
                obj_type = getattr(obj, 'type', 'None')
                obj_class = getattr(obj, 'class', 'None')
                print(f"    - Name: '{obj_name}', Type: '{obj_type}', Class: '{obj_class}', Rect: ({obj.x}, {obj.y}, {obj.width}, {obj.height})")
                if hasattr(obj, 'properties'):
                    print(f"      Properties: {obj.properties}")

base_dir = r"e:\Python learning\Python-learning\Python-learning"
inspect_tmx(os.path.join(base_dir, "Assets", "Map", "testmap.tmx"))
