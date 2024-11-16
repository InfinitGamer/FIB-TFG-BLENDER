import bpy


class SwitchOperator(bpy.types.Operator):
    bl_idname = "scene.bake_switch"
    bl_label = "Switch Bake"
    bl_description = (
        "Changes between material original and bake from a previous bake process"
    )
    bl_options = {"REGISTER"}

    switch: bpy.props.BoolProperty()

    def execute(self, context):

        scene = context.scene

        info = scene.switch_settings

        for model_info in info:
            model: bpy.types.Object = scene.objects[model_info.object_name]

            polygons = model.data.polygons
            info_polygons = model_info.polygons

            for polygon_info in info_polygons:

                polygon: bpy.types.MeshPolygon = polygons[polygon_info.index]

                if not self.switch:
                    polygon.material_index = polygon_info.original_material_index

                else:
                    polygon.material_index = polygon_info.bake_material_index

        self.report(
            {"INFO"}, f"Models changed to {'baked' if self.switch else 'original'} ones"
        )
        return {"FINISHED"}
