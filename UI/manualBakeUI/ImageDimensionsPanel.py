import bpy


class ImageDimensionsPanel(bpy.types.Panel):
    bl_idname = "ImageDimensionsPanel"
    bl_label = "Image Dimensions"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    bl_parent_id = "ManualBakePanel"

    def draw(self, context):
        layout = self.layout
        # cogemos la escena actual
        scene = context.scene

        # cogemos los settings del autobake
        autobake_settings = scene.autobake_settings

        width_settings = layout.row()
        split_w = width_settings.split(factor=0.2)
        split_w.label(text="Width:")
        split_w.prop(autobake_settings, "width", text="")

        height_settings = layout.row()
        split_h = height_settings.split(factor=0.2)
        split_h.label(text="Height:")
        split_h.prop(autobake_settings, "height", text="")
