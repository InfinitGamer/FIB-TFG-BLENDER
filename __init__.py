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
import UI.AddonPanel as UIAP
import UI.manualBakeUI.AddObject as UIAO
import UI.manualBakeUI.DeleteObject as UIDO
import UI.manualBakeUI.ObjectList as UIOL
import UI.manualBakeUI.ManualBakePanel as MBP
def register():
    bpy.utils.register_class(ObjN.ObjectName)
    bpy.utils.register_class(BS.BakingSettings)
    bpy.utils.register_class(UIB.UIBakeSettings)

    bpy.utils.register_class(UIAP.AddonPanel)
    
    bpy.utils.register_class(UIAO.AddObject)
    bpy.utils.register_class(UIDO.DeleteObject)
    bpy.utils.register_class(UIOL.ObjectList)
    bpy.utils.register_class(MBP.ManualBakePanel)
    
    bpy.types.Scene.UIbake_settings = bpy.props.PointerProperty(type=UIB.UIBakeSettings)
    bpy.types.Scene.autobake_settings = bpy.props.PointerProperty(type=BS.BakingSettings)

    bpy.utils.register_class(BK.AutomateBaking)
    
def unregister():
    bpy.utils.unregister_class(BK.AutomateBaking)

    del bpy.types.Scene.autobake_settings
    del bpy.types.Scene.UIbake_settings

    
    bpy.utils.unregister_class(MBP.ManualBakePanel)
    bpy.utils.unregister_class(UIOL.ObjectList)
    bpy.utils.unregister_class(UIDO.DeleteObject)
    bpy.utils.unregister_class(UIAO.AddObject)

    bpy.utils.unregister_class(UIAP.AddonPanel)
    bpy.utils.unregister_class(UIB.UIBakeSettings)
    bpy.utils.unregister_class(BS.BakingSettings)
    bpy.utils.unregister_class(ObjN.ObjectName)
if __name__ == "__main__":
    register()