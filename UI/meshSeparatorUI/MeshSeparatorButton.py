import bpy
class MeshSeparatorButton(bpy.types.Operator):
    bl_idname = "ui.mesh_separator"
    bl_label = "Mesh separator button"
    bl_description = "Button to execute the mesh separator button"
    bl_options = {"REGISTER"}



    def execute(self, context):

        bpy.ops.mesh.separator()
        return {"FINISHED"}
