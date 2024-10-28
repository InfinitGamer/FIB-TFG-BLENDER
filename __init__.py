import bpy
import sys
import os

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
import structures.ObjectName as ObjN
import structures.BakingSettings as BS
import structures.UIBakeSettings as UIB
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

# Lista de clases para registro y desregistro
classes = [
    ObjN.ObjectName,
    BS.BakingSettings,
    UIB.UIBakeSettings,
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
    UIBTA.BakeTypePanelAuto,
    UIOPA.ObjectsPanelAuto,
    UIDPA.DirectoryPanelAuto,
    BK.AutomateBaking,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.UIbake_settings = bpy.props.PointerProperty(type=UIB.UIBakeSettings)
    bpy.types.Scene.autobake_settings = bpy.props.PointerProperty(type=BS.BakingSettings)

def unregister():
    del bpy.types.Scene.autobake_settings
    del bpy.types.Scene.UIbake_settings

    for cls in reversed(classes):  # Desregistrar en orden inverso
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
