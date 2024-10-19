import bpy
bl_info = {
    "name": "AutomatizationBaking",
    "author": "Jeremy Comino",
    "version": (0, 2, 0),
    "blender": (4, 2, 0),
    "description": "Auto Bake",
    "category": "Development",
}
import sys
import os

# Obtener la ruta del directorio del addon
ADDON_FOLDER_PATH = os.path.dirname(__file__)
# Agregar la ruta al sys.path
sys.path.append(ADDON_FOLDER_PATH)


import algorithm.baking.BakingAutomatization as BK
def register():
    bpy.utils.register_class(BK.AutomateBaking)

def unregister():
    bpy.utils.unregister_class(BK.AutomateBaking)

if __name__ == "__main__":
    register()