import bpy
import os
from structures.ObjectInfo import ObjectInfo
from structures.PolygonsStructure import PolygonsStructure


class AutomateBaking(bpy.types.Operator):

    bl_idname = "scene.autobake"
    bl_label = "AutomateBaking"
    # parameters
    bake_type: bpy.props.EnumProperty(
        items=[
            ("COMBINED", "Combined", "Combined Bake"),
            ("AO", "Ao", "Ambient Occlusion"),
            ("EMIT", "Emit", "Emit Bake"),
            ("ENVIRONMENT", "Environment", "Environment Bake"),
            ("ROUGHNESS", "Roughness", "Roughness Bake"),
            ("DIFFUSE", "Diffuse", "Diffuse Bake"),
            ("GLOSSY", "Glossy", "Glossy Bake"),
        ],
        default="COMBINED",
    )  # type: ignore
    device: bpy.props.EnumProperty(
        items=[
            ("GPU", "Gpu", "GPU Device"),
            ("CPU", "Cpu", "CPU Device"),
        ],
        default="CPU",
    )  # type: ignore
    width: bpy.props.IntProperty(min=1, default=1, subtype="PIXEL")  # type: ignore

    height: bpy.props.IntProperty(min=1, default=1, subtype="PIXEL")  # type: ignore

    margin: bpy.props.IntProperty(min=0, default=0, subtype="PIXEL")  # type: ignore

    margin_type: bpy.props.EnumProperty(
        items=[
            (
                "ADJACENT_FACES",
                "Adjacent Faces",
                "Use pixels from adjacent faces across UV seams",
            ),
            ("EXTEND", "Extend", "Extend border pixels outwards"),
        ]
    )  # type: ignore

    pass_filter: bpy.props.EnumProperty(
        items=[
            ("DIRECT", "Direct", "Direct light"),
            ("INDIRECT", "Indirect", "Indirect light"),
            ("COLOR", "Color", "Base color"),
            ("EMIT", "Emit", "Emit contribution"),
            ("DIFFUSE", "Diffuse", "Diffuse contribution"),
            ("GLOSSY", "Glossy", "Glossy contribution"),
            ("TRANSMISSION", "Transmission", "Transmission Contribution"),
        ],
        options={"ENUM_FLAG"},
    )  # type: ignore

    path: bpy.props.StringProperty(subtype="DIR_PATH")  # type: ignore

    @staticmethod
    def get_used_materials_index(model: bpy.types.Object) -> set[int]:

        used_material: set[int] = set()
        polygons: bpy.types.MeshPolygons = model.data.polygons
        for polygon in polygons:
            used_material.add(polygon.material_index)

        return used_material

    @staticmethod
    def create_bake_material(
        model: bpy.types.Object, image: bpy.types.Image, bake_type: str
    ) -> dict[int, int]:

        map_material_original_to_bake: dict[int, int] = {}

        suffix: str = f"_{bake_type.lower()}_baked"

        used_material_index: set[int] = AutomateBaking.get_used_materials_index(model)

        for index in used_material_index:

            material_original = AutomateBaking.get_model_material(model.data, index)

            # cogemos el nombre de la imagen
            material_name: str = material_original.name + suffix

            # creamos material
            material_bake: bpy.types.Material = bpy.data.materials.new(
                name=material_name
            )

            # habilitamos el uso de nodos
            material_bake.use_nodes = True

            # limpiamos todos los nodos que se han creado al construirse el material
            tree_node = material_bake.node_tree
            tree_node.nodes.clear()
            tree_node.links.clear()

            # creamos nodo textura
            texture_node: bpy.types.ShaderNodeTexImage = tree_node.nodes.new(
                type="ShaderNodeTexImage"
            )

            # asignamos la imagen al nodo
            texture_node.image = image

            # creamos nodo output

            output_node: bpy.types.ShaderNodeOutputMaterial = tree_node.nodes.new(
                type="ShaderNodeOutputMaterial"
            )
            output_node.location = (150, 0)

            # creamos link
            tree_node.links.new(
                texture_node.outputs["Color"], output_node.inputs["Surface"]
            )

            # introducimos material en el modelo
            model.data.materials.append(material_bake)

            # decimos en que posicion del material está
            material_baked_index = len(model.data.materials) - 1

            # guardamos el conjunto key value
            map_material_original_to_bake[index] = material_baked_index

        # devolvemos el diccionario
        return map_material_original_to_bake

    @staticmethod
    def count_files_with_prefix(path, prefix) -> int:
        try:
            # List of files that start with the prefix
            files_with_prefix = [f for f in os.listdir(path) if f.startswith(prefix)]
            return len(files_with_prefix)
        except FileNotFoundError:
            return 0

    @staticmethod
    def attach_material_to_polygons(
        model_setting: ObjectInfo, material_dicc: dict[int, int]
    ):

        for polygon in model_setting.polygons:

            polygon.bake_material_index = material_dicc.get(
                polygon.original_material_index
            )

    @staticmethod
    def get_image(name: str, path: str, width: int, height: int) -> bpy.types.Image:
        # comprobamos todas la ocurrencias en el fichero "path" que comienzan por "name"
        number_ocurrences = AutomateBaking.count_files_with_prefix(path, name)

        # si hay ocurrencias, ponemos un numero para diferenciarla de las demás
        if number_ocurrences > 0:
            name = name + f".{number_ocurrences}"

        # creamos imagen
        image: bpy.types.Image = bpy.data.images.new(name, width, height)
        return image

    @staticmethod
    def get_model_material(model: bpy.types.Mesh, index) -> bpy.types.Material:
        material = model.materials[index]
        return material

    @staticmethod
    def prepare_model(
        model: bpy.types.Object,
        model_setting: ObjectInfo,
        image: bpy.types.Image,
        bake_type: str,
    ):
        # añadimos información sobre el modelo en sus settings
        model_setting.name = model.name
        model_setting.bake_type = bake_type.lower()
        model_setting.is_valid = True
        # extraemos la mesh del modelo
        mesh: bpy.types.Mesh = model.data
        # nos recorremos cada uno de los poligonos para setearlos
        for face in mesh.polygons:
            # extraemos el indice del material
            material_index = face.material_index

            polygon_setting: PolygonsStructure = model_setting.polygons.add()
            polygon_setting.index = face.index
            polygon_setting.original_material_index = material_index

            # extraemos el material
            material: bpy.types.Material = AutomateBaking.get_model_material(
                mesh, material_index
            )
            material_baked_name = f"{material.name}_baked"

            # comprobamos si el material ha sido ya previamente tratado
            material_baked_index: int = mesh.materials.find(material_baked_name)

            if material_baked_index == -1:
                # copiamos material para no afectar al original
                material_baked: bpy.types.Material = material.copy()
                material_baked.name = f"{material.name}_baked"

                # activamos el uso de nodos si no está ya activado
                if not material_baked.use_nodes:
                    material_baked.use_nodes = True

                # accedemos al arbol de nodos
                tree_node: bpy.types.NodeTree = material_baked.node_tree
                nodes: bpy.types.Nodes = tree_node.nodes

                # creamos nodo donde se alojará la imagen a hacer baking
                image_texture_node: bpy.types.ShaderNodeTexImage = nodes.new(
                    type="ShaderNodeTexImage"
                )
                # asignamos un nombre distintivo para poder posteriormente hacer busquedas

                image_texture_node.name = "node_for_baking"
                # asignamos la imagen al nodo
                image_texture_node.image = image

                # Ajustamos la posicion del nodo
                image_texture_node.location = (0, 0)

                # dejamos seleccionado el nodo que acabamos de crear
                image_texture_node.select = True

                # dejamos activo este nodo
                nodes.active = image_texture_node

                # cogemos y añadimos el material a la lista de materiales del objeto
                mesh.materials.append(material_baked)

                # extraemos el indice donde esta guardado el material creado
                index: int = mesh.materials.find(material_baked.name)
                face.material_index = index

                # guardamos el material y su transformación en el diccionario
            else:
                face.material_index = material_baked_index

    @staticmethod
    def configure_bake(device: str):
        # para hacer bake seleccionamos un motor (de momento lo dejamos en cycles)
        bpy.context.scene.render.engine = "CYCLES"

        # en el caso del motor gráfico de CYCLES se puede elegir si lo hace la CPU o GPU
        bpy.context.scene.cycles.device = device

    def execute_bake(
        self,
        model: bpy.types.Object,
        bake_type: str,
        margin: int,
        margin_type: str,
        pass_filter: set[str],
    ):

        # ponemos el modelo como el objeto activo
        bpy.context.view_layer.objects.active = model
        for obj in bpy.context.scene.objects:
            if obj.name != model.name:
                obj.select_set(False)  # Deseleccionar objetos que no son el activo
            else:
                obj.select_set(True)
        try:
            bpy.ops.object.bake(
                type=bake_type,
                pass_filter=pass_filter,
                margin=margin,
                margin_type=margin_type,
                use_clear=True,
                save_mode="INTERNAL",
            )
            self.report({"INFO"}, f"{model.name} was baked successfully")
        except Exception as e:
            self.report({"ERROR"}, f"{model.name} was not baked due to an error")
            raise e

    @staticmethod
    def save_image(image: bpy.types.Image, path: str):
        image.filepath_raw = f"{path}\\{image.name}.png"
        image.file_format = "PNG"
        image.save()

    @staticmethod
    def restore_materials(model: bpy.types.Object):
        mesh: bpy.types.Mesh = model.data
        materials_to_delete: set[str] = set()
        # volvemos a poner en cada poligono su material original
        for face in mesh.polygons:
            index_material = face.material_index
            name_material_baked = mesh.materials[index_material].name
            materials_to_delete.add(name_material_baked)
            name_material = name_material_baked.removesuffix("_baked")
            index_original_material = mesh.materials.find(name_material)
            face.material_index = index_original_material
        # eliminamos los materiales baked
        for material in materials_to_delete:
            index = mesh.materials.find(material)
            material_removed = mesh.materials.pop(index=index)
            bpy.data.materials.remove(material_removed)


    def bake_model(
        self,
        model: bpy.types.Object,
        bake_type: str,
        device: str,
        path: str,
        width: int,
        height: int,
        margin: int,
        margin_type: str,
        pass_filter: set[str],
        model_setting: ObjectInfo,
    ):

        valid: bool = True
        # creamos la imagen destino del baking
        image = AutomateBaking.get_image(
            f"{model.name}_{bake_type.lower()}_baked", path, width, height
        )

        # preparamos el objeto
        AutomateBaking.prepare_model(model, model_setting, image, bake_type)

        # configuramos el bake
        AutomateBaking.configure_bake(device)
        try:

            # ejecutamos bake
            self.execute_bake(model, bake_type, margin, margin_type, pass_filter)

            # guardamos bake
            AutomateBaking.save_image(image, path)

            # restauramos los materiales originales
            AutomateBaking.restore_materials(model)

            # creamos material bake
            material_baked_transformation: dict[int, int] = (
                AutomateBaking.create_bake_material(model, image, bake_type)
            )

            AutomateBaking.attach_material_to_polygons(
                model_setting, material_baked_transformation
            )

        except Exception:
            valid = False
            # restauramos los materiales originales
            AutomateBaking.restore_materials(model)

        return valid

    def bake_list(
        self,
        list_Models: list[bpy.types.Object],
        bake_type: str,
        device: str,
        path: str,
        width: int,
        height: int,
        margin: int,
        margin_type: str,
        pass_filter: set[str],
        switch_settings: bpy.types.CollectionProperty,
    ):
        for model in list_Models:
            model_setting = switch_settings.add()

            valid = self.bake_model(
                model,
                bake_type,
                device,
                path,
                width,
                height,
                margin,
                margin_type,
                pass_filter,
                model_setting,
            )

            if not valid:
                size = len(switch_settings)
                switch_settings.remove((size - 1))

    def execute(self, context):

        scene = context.scene
        scene.communication_data.baking_active = True
        object_name_list: bpy.types.Collection = scene.autobake_settings.objects
        object_list = []
        for object_name in object_name_list:
            object = scene.objects[object_name.object_name]
            object_list.append(object)

        bake_type: str = self.bake_type
        device: str = self.device
        path: str = self.path
        width: int = self.width
        height: int = self.height
        margin: int = self.margin
        margin_type: str = self.margin_type
        pass_filter: set[str] = self.pass_filter
        switch_structure = scene.switch_settings
        self.bake_list(
            object_list,
            bake_type,
            device,
            path,
            width,
            height,
            margin,
            margin_type,
            pass_filter,
            switch_structure,
        )
        scene.communication_data.baking_active = False
        return {"FINISHED"}
