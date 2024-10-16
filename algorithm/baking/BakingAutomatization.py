import bpy

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "op.simple_operator"
    bl_label = "Simple Object Operator"
    
    @classmethod
    def get_image(name, width, height):
        #creamos imagen
        image: bpy.types.Image = bpy.data.images.new(name,width,height)
        return image
    @classmethod
    def get_face_material(model: bpy.types.Mesh, index):
        material = model.materials[index]
        return material
    @classmethod
    def bake_model(model: bpy.types.Object):
        
        
        #creamos la imagen destino del bakingç
        image = SimpleOperator.get_image(f"{model.name}_baked")
        
        #extraemos la mesh del modelo
        mesh: bpy.types.Mesh = model.data
        mesh.mat
        #nos recorremos cada uno de los poligonos para setearlos
        for face in mesh.polygons:
            #extraemos el indice del material
            material_index = face.material_index
            
            #extraemos el material
            material: bpy.types.Material = SimpleOperator.get_face_material(mesh,material_index)
            material_baked_name = f"{material.name}_baked"

            #comprobamos si el material ha sido ya previamente tratado
            material_baked : int = mesh.materials.find(material_baked_name)
            
            if material_baked == -1:
                #copiamos material para no afectar al original
                material_baked: bpy.types.Material = material.copy()
                material_baked.name = f"{material.name}_baked"

                #activamos el uso de nodos si no está ya activado
                if not material_baked.use_nodes:
                    material_baked.use_nodes = True

                #accedemos al arbol de nodos
                tree_node: bpy.types.ShaderNodeTree = material.node_tree
                nodes: bpy.types.Nodes = tree_node.nodes
                
                #creamos nodo donde se alojará la imagen a hacer baking
                image_texture_node: bpy.types.ShaderNodeTexImage = nodes.new(type="ShaderNodeTexImage")
                
                #asignamos la imagen al nodo
                image_texture_node.image = image

                # Ajustamos la posicion del nodo
                image_texture_node.location = (0, 0)
                
                #dejamos seleccionado el nodo que acabamos de crear
                image_texture_node.select = True

                #dejamos activo este nodo (ver si este es necesario)
                nodes.active = image_texture_node

                #cogemos y añadimos el material a la lista de materiales del objeto
                mesh.materials.append(material_baked)
                
                #extraemos el indice donde esta guardado el material creado
                index: int = mesh.materials.find(material_baked.name)
                face.material_index  = index

                #guardamos el material y su transformación en el diccionario
            else:
                #si ya existe, únicamente hay que poner ese material como el activo de la cara
                face.material_index = index

                





    @classmethod
    def bake_list(list_Models: [bpy.types.Object]):
        for model in list_Models:
            SimpleOperator.bake_model(model)

    def execute(self, context):
        return {'FINISHED'}