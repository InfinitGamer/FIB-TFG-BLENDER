import bpy

class BakeTypePanelAuto(bpy.types.Panel):
    bl_idname ="BakeTypePanelAuto"
    bl_parent_id="AutomaticBakePanel"
    bl_label = "Bake Type"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FIB-TFG-BLENDER"
    def draw(self, context):
        layout = self.layout
        
        #cogemos la escena actual
        scene = context.scene
        
        #cogemos los settings del autobake
        autobake_settings = scene.autobake_settings
        
        #cogemos los elementos para la UI de bake
        UIbake_settings = scene.UIbake_settings

        #creamos selector del tipo del bake
        
        property_settings = layout.row()
        property_settings.prop(autobake_settings,"bake_type", text="Bake Type")
        
        pass_filter_values = ["COMBINED", "GLOSSY","DIFFUSE"]
        if autobake_settings.bake_type in pass_filter_values:
            pass_filter = layout.column()
            pass_filter.label(text="Lighting")
            pass_filter.prop_enum(autobake_settings,"pass_filter",value="DIRECT",text="Direct")
            pass_filter.prop_enum(autobake_settings,"pass_filter",value="INDIRECT",text="Indirect")
            pass_filter.prop_enum(autobake_settings,"pass_filter",value="COLOR",text="Color")
            
            if autobake_settings.bake_type == "COMBINED":
                pass_filter.label(text="Contributions")
                pass_filter.prop_enum(autobake_settings,"pass_filter",value="DIFFUSE",text="Diffuse")
                pass_filter.prop_enum(autobake_settings,"pass_filter",value="GLOSSY",text="Glossy")
                pass_filter.prop_enum(autobake_settings,"pass_filter",value="TRANSMISSION",text="Transmission")
                pass_filter.prop_enum(autobake_settings,"pass_filter",value="EMIT",text="Emit")
    