import enum

# https://github.com/KhronosGroup/glTF/tree/master/specification/1.0

# Uniform Semantics:
# LOCAL, MODEL, VIEW, PROJECTION, ...

class Uniform(enum.Enum):
    LOCAL      = "LOCAL"
    MODEL      = "MODEL"
    VIEW       = "VIEW"
    PROJECTION = "PROJECTION"

# Attribute Semantics:
# POSITION, NORMAL, TEXCOORD_0, TEXCOORD_1, COLOR, JOINT, WEIGHT

class Attribute(enum.Enum):
    POSITION   = "POSITION"
    NORMAL     = "NORMAL"
    TEXCOORD   = "TEXCOORD"
    TEXCOORD_0 = "TEXCOORD_0"
    TEXCOORD_1 = "TEXCOORD_1"
    COLOR      = "COLOR"
    JOINT      = "JOINT"
    WEIGHT     = "WEIGHT"

# Accessor Types:
# SCALAR, VEC2, VEC3, VEC4, MAT2, MAT3, MAT4

class AccessorType(enum.Enum):
    SCALAR = "SCALAR"
    VEC2   = "VEC2"
    VEC3   = "VEC3"
    VEC4   = "VEC4"
    MAT2   = "MAT2"
    MAT3   = "MAT3"
    MAT4   = "MAT4"

# Component Types:
# SCALAR, VEC2, VEC3, VEC4, MAT2, MAT3, MAT4

class ComponentType(enum.Enum):
    BYTE           = 5120
    UNSIGNED_BYTE  = 5121
    SHORT          = 5122
    UNSIGNED_SHORT = 5123
    FLOAT          = 5126

class BufferTarget(enum.Enum):
    ARRAY_BUFFER         = 34962
    ELEMENT_ARRAY_BUFFER = 34963

class PrimitiveMode(enum.Enum):
    POINTS         = 0
    LINES          = 1
    LINE_LOOP      = 2
    LINE_STRIP     = 3
    TRIANGLES      = 4
    TRIANGLE_STRIP = 5
    TRIANGLE_FAN   = 6

def askey(name):
    return name.replace(" ", "_").lower()


class Document(object):
    @classmethod
    def from_mesh(cls, mesh, material=None):
        node = Node("Default Node", meshes=[mesh])
        scene = Scene("Default Scene", nodes=[node])
        
        materials = {} if material is None else {material.key: material}
        meshes = {} if mesh is None else {mesh.key: mesh}
        nodes = {node.key: node}
        scenes = {scene.key: scene}
        
        return cls(materials=materials, meshes=meshes, nodes=nodes, scenes=scenes, scene=scene)
    
    @classmethod
    def from_meshes(cls, meshes, materials=None):
        meshes = [] if meshes is None else meshes
        materials = [] if materials is None else materials
        
        node = Node("Default Node", meshes=meshes)
        scene = Scene("Default Scene", nodes=[node])
        
        materials = {material.key: material for material in materials}
        meshes = {mesh.key: mesh for mesh in meshes}
        nodes = {node.key: node}
        scenes = {scene.key: scene}
        
        return cls(materials=materials, meshes=meshes, nodes=nodes, scenes=scenes, scene=scene)
    
    def __init__(self, *args, **kwargs):
        self.asset        = {"version": "1.0"}
        self.scene        = kwargs.get('scene', None)
        self.scenes       = kwargs.get('scenes', {})
        self.nodes        = kwargs.get('nodes', {})
        self.meshes       = kwargs.get('meshes', {})
        self.materials    = kwargs.get('materials', {})
        self.accessors    = kwargs.get('accessors', {})
        self.buffer_views = kwargs.get('buffer_views', {})
        self.buffers      = kwargs.get('buffers', {})
    
    def add_scene(self, value):
        self.scenes[value.key] = value
    def add_node(self, value):
        self.nodes[value.key] = value
    def add_mesh(self, value):
        self.meshes[value.key] = value
    def add_material(self, value):
        self.materials[value.key] = value
    def add_accessor(self, value):
        self.accessors[value.key] = value
    def add_buffer_view(self, value):
        self.buffer_views[value.key] = value
    def add_buffer(self, value):
        self.buffers[value.key] = value
    
    def togltf(self):
        return {
            "buffers":     {key: buffer.togltf()      for key, buffer      in self.buffers.items()},
            "bufferViews": {key: buffer_view.togltf() for key, buffer_view in self.buffer_views.items()},
            "accessors":   {key: accessor.togltf()    for key, accessor    in self.accessors.items()},
            "materials":   {key: material.togltf()    for key, material    in self.materials.items()},
            "meshes":      {key: mesh.togltf()        for key, mesh        in self.meshes.items()},
            "nodes":       {key: node.togltf()        for key, node        in self.nodes.items()},
            "scenes":      {key: scene.togltf()       for key, scene       in self.scenes.items()},
            "scene": self.scene.key,
            "asset": self.asset,
        }

class Scene(object):
    @property
    def key(self):
        return askey(self.name)
    def __init__(self, name, *args, **kwargs):
        self.name  = name
        self.nodes = kwargs.get('nodes', [])
    def togltf(self):
        return {
            "name": self.name,
            "nodes": [node.key for node in self.nodes],
        }

class Node(object):
    @property
    def key(self):
        return askey(self.name)
    def __init__(self, name, *args, **kwargs):
        self.name     = name
        self.matrix   = [
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        ],
        self.meshes   = kwargs.get('meshes', [])
        self.children = kwargs.get('children', [])
    def togltf(self):
        return {
            "name": self.name,
            "matrix": self.matrix,
            "meshes": [mesh.key for mesh in self.meshes],
            "children": [child.key for child in self.children],
        }

class Accessor(object):
    @property
    def key(self):
        return askey(self.name)
    def __init__(self, name, bufferView, byteOffset = 0, byteStride = 0, count = 0, type = AccessorType.SCALAR, componentType = ComponentType.FLOAT):
        self.name = name
        self.type = type
        self.componentType = componentType
        self.bufferView = bufferView
        self.byteOffset = byteOffset
        self.byteStride = byteStride
        self.count = count
        self.max = None
        self.min = None
    def togltf(self):
        return {
            #"name": self.name,
            "bufferView": self.bufferView.key,
            "byteOffset": self.byteOffset,
            "byteStride": self.byteStride,
            "componentType": self.componentType.value,
            "count": self.count,
            "type": self.type.value,
            #"max": self.max,
            #"min": self.min,
        }

class BufferView(object):
    @property
    def key(self):
        return askey(self.name)
    def __init__(self, name, buffer, byteOffset=0, byteLength=0, target=BufferTarget.ARRAY_BUFFER):
        self.name  = name
        self.buffer = buffer
        self.byteOffset = byteOffset
        self.byteLength = byteLength
        self.target = target
    def togltf(self):
        return {
            #"name": self.name,
            "buffer": self.buffer.key,
            "byteOffset": self.byteOffset,
            "byteLength": self.byteLength,
            "target": self.target.value,
        }

class Buffer(object):
    @property
    def key(self):
        return askey(self.name)
    def __init__(self, name, uri, byteLength=0, type="arraybuffer"):
        self.name  = name
        self.uri = uri
        self.byteLength = byteLength
        self.type = type
    def togltf(self):
        return {
            #"name": self.name,
            "uri": self.uri,
            "byteLength": self.byteLength,
            "type": self.type,
        }

class Primitive(object):
    def __init__(self, attributes, indices, material, mode=PrimitiveMode.TRIANGLES, targets=None):
        self.attributes = attributes
        self.indices = indices
        self.material = material
        self.mode = mode
        self.targets = targets
    def togltf(self):
        result = {
            "attributes": {key.value: attribute.key for key, attribute in self.attributes.items()},
        }
        if self.indices:
            result["indices"] = self.indices.key
        if self.material:
            result["material"] = self.material.key
        if self.mode:
            result["mode"] = self.mode.value
        #if self.targets:
        #    result["targets"] = self.targets
        return result

class Mesh(object):
    @property
    def key(self):
        return askey(self.name)
    def __init__(self, name, primitives = None):
        self.name = name
        self.primitives = [] if primitives is None else primitives 
    def togltf(self):
        return {
            "name": self.name,
            "primitives": [primitive.togltf() for primitive in self.primitives]
        }

class Material(object):
    @property
    def key(self):
        return askey(self.name)
    def __init__(self, name):
        self.name = name
        self.values = {
            "ambient": [0.0, 0.0, 0.0, 1],
            "diffuse": [0.0, 0.0, 0.0, 1],
            "specular": [0.0, 0.0, 0.0, 1],
            "emission": [0.0, 0.0, 0.0, 1],
            "shininess": 256
        }
    def __setitem__(self, key, item):
        self.values[key] = item
    def __getitem__(self, key):
        return self.values[key]
    def togltf(self):
        return  {
            "name": self.name,
            "values": self.values,
        }