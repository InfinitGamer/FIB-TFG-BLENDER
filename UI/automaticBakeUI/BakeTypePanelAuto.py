import bpy


class BakeTypePanelAuto(bpy.types.Panel):
    bl_idname = "BakeTypePanelAuto"
    bl_parent_id = "AutomaticBakePanel"
    bl_label = "Bake Type"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        autobake_settings = scene.autobake_settings

        property_settings = layout.row()
        property_settings.prop(autobake_settings, "bake_type", text="Bake Type")

        pass_filter_values = ["COMBINED", "GLOSSY", "DIFFUSE"]
        if autobake_settings.bake_type in pass_filter_values:
            pass_filter = layout.column()
            pass_filter.label(text="Lighting")

            row = pass_filter.row()
            split = row.split(factor=0.3)
            split.label(text="")
            split.prop(autobake_settings, "use_direct", text="Direct")

            row = pass_filter.row()
            split = row.split(factor=0.3)
            split.label(text="")
            split.prop(autobake_settings, "use_indirect", text="Indirect")

            row = pass_filter.row()
            split = row.split(factor=0.3)
            split.label(text="")
            split.prop(autobake_settings, "use_color", text="Color")

            if autobake_settings.bake_type == "COMBINED":
                pass_filter.label(text="Contributions")
                row = pass_filter.row()
                split = row.split(factor=0.3)
                split.label(text="")
                split.prop(autobake_settings, "use_diffuse", text="Diffuse")

                row = pass_filter.row()
                split = row.split(factor=0.3)
                split.label(text="")
                split.prop(autobake_settings, "use_glossy", text="Glossy")

                row = pass_filter.row()
                split = row.split(factor=0.3)
                split.label(text="")
                split.prop(autobake_settings, "use_transmission", text="Transmission")

                row = pass_filter.row()
                split = row.split(factor=0.3)
                split.label(text="")
                split.prop(autobake_settings, "use_emit", text="Emit")
