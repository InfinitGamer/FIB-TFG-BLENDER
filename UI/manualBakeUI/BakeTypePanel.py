import bpy


class BakeTypePanel(bpy.types.Panel):
    bl_idname = "BakeTypePanel"
    bl_label = "Bake Type"
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

        # cogemos los elementos para la UI de bake
        UIbake_settings = scene.UIbake_settings

        # creamos selector del tipo del bake

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
