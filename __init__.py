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


import algorithms.baking.BakingAutomatization as BK
import structures.ObjectName as ObjN
import structures.BakingSettings as BS
import structures.UIBakeSettings as UIB

def register():
    bpy.utils.register_class(ObjN.ObjectName)
    bpy.utils.register_class(BS.BakingSettings)
    bpy.utils.register_class(UIB.UIBakeSettings)

    bpy.types.Scene.UIbake_settings = bpy.props.PointerProperty(type=UIB.UIBakeSettings)
    bpy.types.Scene.autobake_settings = bpy.props.PointerProperty(type=BS.BakingSettings)

    bpy.utils.register_class(BK.AutomateBaking)
    
def unregister():
    bpy.utils.unregister_class(BK.AutomateBaking)

    del bpy.types.Scene.autobake_settings
    del bpy.types.Scene.UIbake_settings

    bpy.utils.unregister_class(UIB.UIBakeSettings)
    bpy.utils.unregister_class(BS.BakingSettings)
    bpy.utils.unregister_class(ObjN.ObjectName)
if __name__ == "__main__":
    register()