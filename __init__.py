import bpy
import sys
import os
import subprocess
import pkg_resources
#installing dependencies

modules_to_need ={
    'numpy'
}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = modules_to_need - installed
if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
    



bl_info = {
    "name": "AutomatizationBaking",
    "author": "Jeremy Comino",
    "version": (0, 2, 0),
    "blender": (4, 2, 0),
    "description": "Auto Bake",
    "category": "Development",
}

# Obtener la ruta del directorio del addon
ADDON_FOLDER_PATH = os.path.dirname(__file__)

# Agregar la ruta al sys.path
sys.path.append(ADDON_FOLDER_PATH)

import algorithms.baking.BakingAutomatization as BK
import algorithms.switch.SwitchOperator as SO
import structures.ObjectName as ObjN
import structures.BakingSettings as BS
import structures.UIBakeSettings as UIB
import structures.PolygonsStructure as PS
import structures.ObjectInfo as OI
import structures.UISwitchSettings as UISS
import structures.CommunicationData as CD
import UI.AddonPanel as UIAP
import UI.manualBakeUI.BakeObject as UIBO
import UI.manualBakeUI.AddObject as UIAO
import UI.manualBakeUI.DeleteObject as UIDO
import UI.manualBakeUI.ObjectList as UIOL
import UI.manualBakeUI.ManualBakePanel as UIMBP
import UI.manualBakeUI.FolderSelector as UIFS
import UI.manualBakeUI.BakeTypePanel as UIBTP
import UI.manualBakeUI.ObjectsPanel as UIOP
import UI.manualBakeUI.DevicePanel as UIDP
import UI.manualBakeUI.ImageDimensionsPanel as UIIDP
import UI.manualBakeUI.MarginPanel as UIMP
import UI.manualBakeUI.DirectoryPanel as UIDEP
import UI.automaticBakeUI.AutomaticBakePanel as UIABP
import UI.automaticBakeUI.BakeTypePanelAuto as UIBTA
import UI.automaticBakeUI.ObjectsPanelAuto as UIOPA
import UI.automaticBakeUI.DirectoryPanelAuto as UIDPA
import UI.automaticBakeUI.SetAutomaticSettings as UISAS
import UI.automaticBakeUI.AutomaticPreferencesPanel as UIAPP
import UI.SwitchUI.SwitchButton as UISB
import UI.SwitchUI.SwitchPanel as UISP
import handlers.DeleteOperator as HDO
from handlers.UpdateModificationsHandler import execute

classes = [
    ObjN.ObjectName,
    BS.BakingSettings,
    CD.CommunicationData,
    UIB.UIBakeSettings,
    PS.PolygonsStructure,
    OI.ObjectInfo,
    UIAP.AddonPanel,
    UIMBP.ManualBakePanel,
    UIBO.BakeObject,
    UIAO.AddObject,
    UIDO.DeleteObject,
    UIOL.ObjectList,
    UIFS.FolderSelector,
    UIBTP.BakeTypePanel,
    UIOP.ObjectsPanel,
    UIDP.DevicePanel,
    UIIDP.ImageDimensionsPanel,
    UIMP.MarginPanel,
    UIDEP.DirectoryPanel,
    UIABP.AutomaticBakePanel,
    UISAS.SetAutomaticSettings,
    UIBTA.BakeTypePanelAuto,
    UIOPA.ObjectsPanelAuto,
    UIDPA.DirectoryPanelAuto,
    BK.AutomateBaking,
    UIAPP.AutomaticPreferencesPanel,
    UISS.UISwichSettings,
    SO.SwitchOperator,
    UISB.SwitchButton,
    UISP.SwitchPanel,
    HDO.DeleteOperator,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.UIbake_settings = bpy.props.PointerProperty(type=UIB.UIBakeSettings)
    bpy.types.Scene.autobake_settings = bpy.props.PointerProperty(
        type=BS.BakingSettings
    )
    bpy.types.Scene.switch_settings = bpy.props.CollectionProperty(type=OI.ObjectInfo)
    bpy.types.Scene.UIswitch_settings = bpy.props.PointerProperty(
        type=UISS.UISwichSettings
    )
    bpy.types.Scene.communication_data = bpy.props.PointerProperty(
        type=CD.CommunicationData
    )

    bpy.app.handlers.depsgraph_update_post.append(execute)

    HDO.apply_keybindings()
                        
   
    bpy.types.VIEW3D_MT_object_context_menu.append(HDO.custom_delete_menu)
def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(HDO.custom_delete_menu)

    HDO.unapply_keybindings()
                        
    bpy.app.handlers.depsgraph_update_post.remove(execute)

    del bpy.types.Scene.communication_data
    del bpy.types.Scene.UIswitch_settings
    del bpy.types.Scene.switch_settings
    del bpy.types.Scene.autobake_settings
    del bpy.types.Scene.UIbake_settings

    for cls in reversed(classes):  # Desregistrar en orden inverso
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
