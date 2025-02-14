import bpy


class MarginPanel(bpy.types.Panel):
    bl_idname = "MarginPanel"
    bl_label = "Margin"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    bl_parent_id = "ManualBakePanel"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        
        autobake_settings = scene.autobake_settings

        margin_type = layout.row()
        margin_type.prop(autobake_settings, "margin_type", text="Margin Type")

        margin = layout.row()
        split = margin.split(factor=0.2)
        split.label(text="Margin:")
        split.prop(autobake_settings, "margin", text="")
