import bpy

class AutomateBaking(bpy.types.Operator):
    
    bl_idname = "scene.autobake"
    bl_label = "AutomateBaking"
    #parameters
    bake_type: bpy.props.EnumProperty(
        items=[
            ("COMBINED", "Combined", "Combined Bake"),
            ("AO", "Ao", "Ambient Occlusion"),
            ("EMIT", "Emit", "Emit Bake"),
            ("ENVIRONMENT", "Environment", "Environment Bake"),
            ("DIFFUSE", "Diffuse", "Diffuse Bake"),
            ("GLOSSY", "Glossy", "Glossy Bake"),
        ],
        default="COMBINED"
    ) # type: ignore
    device: bpy.props.EnumProperty(
        items=[
            ("GPU", "Gpu", "GPU Device"),
            ("CPU", "Cpu", "Cpu Device"),
        ],
        default="CPU"
    ) # type: ignore
    width: bpy.props.IntProperty(min=1, default=1) # type: ignore

    height: bpy.props.IntProperty(min=1, default=1) # type: ignore
    
    margin: bpy.props.IntProperty(min=0, default=0) # type: ignore
    
    margin_type: bpy.props.EnumProperty(
        items=[
            ("ADJACENT_FACES", "Adjacent Faces", "Use pixels from adjacent faces across UV seams"),
            ("EXTEND", "Extend", "Extend border pixels outwards")
        ]
    ) # type: ignore

    pass_filter: bpy.props.EnumProperty(
        items=[
            ("DIRECT","Direct", "Direct light"),
            ("INDIRECT","Indirect", "Indirect light"),
            ("COLOR","Color", "Base Color"),
        ],
        options={'ENUM_FLAG'}
    ) # type: ignore

    path: bpy.props.StringProperty() # type: ignore
    
    @staticmethod
    def get_image(name: str, width: int, height: int):
        #creamos imagen
        image: bpy.types.Image = bpy.data.images.new(name,width,height)
        return image
    @staticmethod
    def get_model_material(model: bpy.types.Mesh, index):
        material = model.materials[index]
        return material

    @staticmethod
    def prepare_model(model:bpy.types.Object, image: bpy.types.Image):
        set_index_materials :set ={}
        #extraemos la mesh del modelo
        mesh: bpy.types.Mesh = model.data
        #nos recorremos cada uno de los poligonos para setearlos
        for face in mesh.polygons:
            #extraemos el indice del material
            material_index = face.material_index
            
            #extraemos el material
            material: bpy.types.Material = AutomateBaking.get_model_material(mesh,material_index)
            material_baked_name = f"{material.name}_baked"

            #comprobamos si el material ha sido ya previamente tratado
            material_baked_index : int = mesh.materials.find(material_baked_name)
            
            if material_baked_index == -1:
                #copiamos material para no afectar al original
                material_baked: bpy.types.Material = material.copy()
                material_baked.name = f"{material.name}_baked"

                #activamos el uso de nodos si no está ya activado
                if not material_baked.use_nodes:
                    material_baked.use_nodes = True
                
                #accedemos al arbol de nodos
                tree_node: bpy.types.NodeTree = material_baked.node_tree
                nodes: bpy.types.Nodes = tree_node.nodes
                
                #creamos nodo donde se alojará la imagen a hacer baking
                image_texture_node: bpy.types.ShaderNodeTexImage = nodes.new(type="ShaderNodeTexImage")
                #asignamos un nombre distintivo para poder posteriormente hacer busquedas

                image_texture_node.name = "node_for_baking"
                #asignamos la imagen al nodo
                image_texture_node.image = image

                # Ajustamos la posicion del nodo
                image_texture_node.location = (0, 0)
                
                #dejamos seleccionado el nodo que acabamos de crear
                image_texture_node.select = True

                #dejamos activo este nodo
                nodes.active = image_texture_node

                #cogemos y añadimos el material a la lista de materiales del objeto
                mesh.materials.append(material_baked)
                
                #extraemos el indice donde esta guardado el material creado
                index: int = mesh.materials.find(material_baked.name)
                face.material_index  = index

                #guardamos el material y su transformación en el diccionario
            else:
                face.material_index = material_baked_index

    @staticmethod
    def configure_bake(device: str):
        #para hacer bake seleccionamos un motor (de momento lo dejamos en cycles)
        bpy.context.scene.render.engine = 'CYCLES'

        #en el caso del motor gráfico de CYCLES se puede elegir si lo hace la CPU o GPU
        bpy.context.scene.cycles.device = device
        
    
    @staticmethod
    def execute_bake(model: bpy.types.Object,
                     bake_type: str,
                     margin: int,
                     margin_type: str,
                     pass_filter: set[str]
                     ):
        
        #ponemos el modelo como el objeto activo
        bpy.context.view_layer.objects.active = model
        bpy.ops.object.bake(
            type=bake_type,
            pass_filter=pass_filter,
            margin=margin,
            margin_type=margin_type,
            use_clear=True,
            save_mode="EXTERNAL"
        )

    @staticmethod
    def save_image(image: bpy.types.Image, path: str):
        image.filepath_raw = f"{path}\\{image.name}.png"
        image.file_format ="PNG"
        image.save()
    
    @staticmethod
    def restore_materials(model: bpy.types.Object):
        mesh: bpy.types.Mesh = model.data
        materials_to_delete: set[str] = set()
        #volvemos a poner en cada poligono su material original
        for face in mesh.polygons:
            index_material = face.material_index
            name_material_baked = mesh.materials[index_material].name
            materials_to_delete.add(name_material_baked)
            name_material = name_material_baked.split('_baked')[0]
            index_original_material = mesh.materials.find(name_material)
            face.material_index = index_original_material
        #eliminamos los materiales baked
        for material in materials_to_delete:
            index = mesh.materials.find(material)
            mesh.materials.pop(index=index)

        

    @staticmethod
    def bake_model(model: bpy.types.Object,
                   bake_type: str,
                   device: str,
                   path: str,
                   width: int,
                   height: int,
                   margin: int,
                   margin_type: str,
                   pass_filter: set[str]):
        
        
        #creamos la imagen destino del bakingç
        image = AutomateBaking.get_image(f"{model.name}_baked", width, height)
        
        #preparamos el objeto
        AutomateBaking.prepare_model(model, image)

        #configuramos el bake
        AutomateBaking.configure_bake(device)
        #ejecutamos bake
        AutomateBaking.execute_bake(model,
                                    bake_type,
                                    margin,
                                    margin_type,
                                    pass_filter)

        #guardamos bake
        AutomateBaking.save_image(image, path)
        #restauramos los materiales originales
        AutomateBaking.restore_materials(model)


    @staticmethod
    def bake_list(list_Models: list[bpy.types.Object],
                  bake_type: str,
                  device: str,
                  path: str,
                  width: int,
                  height: int,
                  margin: int,
                  margin_type: str,
                  pass_filter: set[str]
                  ):
        for model in list_Models:
            AutomateBaking.bake_model(model,
                                    bake_type,
                                    device,
                                    path,
                                    width,
                                    height,
                                    margin,
                                    margin_type,
                                    pass_filter
                                    )

    def execute(self, context):
        #faltaría seleccionar los elementos a hacer con baking
        #de momento podemos utilizar los elementos seleccionados
        scene = context.scene
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
        margin : int = self.margin
        margin_type: str = self.margin_type
        pass_filter: set[str] = self.pass_filter
        
        AutomateBaking.bake_list(object_list,
                                 bake_type,
                                 device,
                                 path,
                                 width,
                                 height,
                                 margin,
                                 margin_type,
                                 pass_filter)
        return {'FINISHED'}