import bpy


class ObjectList(bpy.types.UIList):

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        # Mostrar el nombre del objeto
        objeto = item
        layout.label(text=objeto.object_name, icon="OBJECT_DATAMODE")
