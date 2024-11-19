import bpy

class DeleteOperator(bpy.types.Operator):
    bl_idname = "object.delete_override"
    bl_label = "Object Delete Operator"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print("!!!!")
        scene: bpy.types.Scene = context.scene
        selected_object: list[bpy.types.Object] = context.selected_objects
        switch_settings: bpy.types.bpy_prop_collection = scene.switch_settings
        
        for obj in selected_object:
            index: int = switch_settings.find(obj.name)
            if index >= 0:
                switch_settings.remove(index)

        bpy.ops.object.delete()
        return {'FINISHED'}

def apply_keybindings():
    keyconfig = bpy.context.window_manager.keyconfigs.default
    if keyconfig:
        for keymap in keyconfig.keymaps:
            if keymap.name == "Object Mode":
                for keymap_item in keymap.keymap_items:
                    if keymap_item.idname == "object.delete":
                        keymap_item.idname = DeleteOperator.bl_idname

def unapply_keybindings():
    keyconfig = bpy.context.window_manager.keyconfigs.default
    if keyconfig:
        for keymap in keyconfig.keymaps:
            if keymap.name == "Object Mode":
                for keymap_item in keymap.keymap_items:
                    if keymap_item.idname == DeleteOperator.bl_idname:
                        keymap_item.idname = "object.delete"

# Paso 2: Modificar el menú contextual de clic derecho
def custom_delete_menu(self, context):
    layout = self.layout
   
    # Agregar el operador 'Delete' personalizado
    layout.operator(DeleteOperator.bl_idname, text="Delete Everywhere")
            

