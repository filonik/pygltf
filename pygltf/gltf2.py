import enum

import collections

# https://github.com/KhronosGroup/glTF/tree/master/specification/2.0

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
    BINORMAL   = "BINORMAL"
    TANGENT    = "TANGENT"
    TEXCOORD   = "TEXCOORD"
    TEXCOORD_0 = "TEXCOORD_0"
    TEXCOORD_1 = "TEXCOORD_1"
    COLOR      = "COLOR"
    COLOR_0    = "COLOR_0"
    COLOR_1    = "COLOR_1"
    JOINTS_0   = "JOINTS_0"
    WEIGHTS_0  = "WEIGHTS_0"
    @staticmethod
    def custom(value):
        return collections.namedtuple("Attribute", "value")(value)

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
    #INT            = 5124
    UNSIGNED_INT   = 5125
    FLOAT          = 5126
    @staticmethod
    def custom(value):
        return collections.namedtuple("ComponentType", "value")(value)

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

class AlphaMode(enum.Enum):
    OPAQUE = "OPAQUE"
    MASK   = "MASK" 
    BLEND  = "BLEND"
    
class Interpolation(enum.Enum):
    LINEAR      = "LINEAR"
    STEP        = "STEP"
    CUBICSPLINE = "CUBICSPLINE"

class Filter(enum.Enum):
    NEAREST = 9728 
    LINEAR = 9729
    NEAREST_MIPMAP_NEAREST = 9984
    LINEAR_MIPMAP_NEAREST = 9985
    NEAREST_MIPMAP_LINEAR = 9986
    LINEAR_MIPMAP_LINEAR = 9987

class Wrap(enum.Enum):
    CLAMP_TO_EDGE = 33071
    MIRRORED_REPEAT = 33648 
    REPEAT = 10497


def askey(name):
    return name.replace(" ", "_").lower()


class Object(object):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name")
        self.extensions = kwargs.get("extensions")
        self.extras = kwargs.get("extras")
    def togltf(self):
        result = {}
        if self.name:
            result["name"] = self.name
        if self.extensions:
            result["extensions"] = self.extensions
        if self.extras:
            result["extras"] = self.extras
        return result


class Document(object):
    @classmethod
    def from_mesh(cls, mesh, material=None):
        materials = [] if material is None else [material]
        meshes = [] if mesh is None else [mesh]
        
        nodes = [Node(name="Default Node", mesh=mesh) for mesh in meshes]
        scene = Scene(name="Default Scene", nodes=nodes)
        scenes = [scene]
        
        return cls(materials=materials, meshes=meshes, nodes=nodes, scenes=scenes, scene=scene)
    
    @classmethod
    def from_meshes(cls, meshes, materials=None):
        meshes = [] if meshes is None else meshes
        materials = [] if materials is None else materials
        
        nodes = [Node(name="Default Node", mesh=mesh) for mesh in meshes]
        scene = Scene(name="Default Scene", nodes=nodes)
        scenes = [scene]
        
        return cls(materials=materials, meshes=meshes, nodes=nodes, scenes=scenes, scene=scene)
    
    def __init__(self, *args, **kwargs):
        self.asset        = {"version": "2.0"}
        self.accessors    = []
        self.animations   = []
        self.buffers      = []
        self.bufferViews  = []
        self.cameras      = []
        self.images       = []
        self.materials    = []
        self.meshes       = []
        self.nodes        = []
        self.samplers     = []
        self.scenes       = []
        self.skins        = []
        self.textures     = []
        self.scene        = kwargs.get('scene', None)
        
        self.add_accessors(kwargs.get('accessors', []))
        self.add_animations(kwargs.get('animations', []))
        self.add_buffers(kwargs.get('buffers', []))
        self.add_buffer_views(kwargs.get('bufferViews', []))
        self.add_cameras(kwargs.get('cameras', []))
        self.add_images(kwargs.get('images', []))
        self.add_materials(kwargs.get('materials', []))
        self.add_meshes(kwargs.get('meshes', []))
        self.add_nodes(kwargs.get('nodes', []))
        self.add_samplers(kwargs.get('samplers', []))
        self.add_scenes(kwargs.get('scenes', []))
        self.add_skins(kwargs.get('skins', []))
        self.add_textures(kwargs.get('textures', []))
    
    def add_accessor(self, value):
        value.key = len(self.accessors)
        self.accessors.insert(value.key, value)
    def add_animation(self, value):
        value.key = len(self.animations)
        self.animations.insert(value.key, value)
    def add_buffer(self, value):
        value.key = len(self.buffers)
        self.buffers.insert(value.key, value)
    def add_buffer_view(self, value):
        value.key = len(self.bufferViews)
        self.bufferViews.insert(value.key, value)
    def add_camera(self, value):
        value.key = len(self.cameras)
        self.cameras.insert(value.key, value)
    def add_image(self, value):
        value.key = len(self.images)
        self.images.insert(value.key, value)
    def add_material(self, value):
        value.key = len(self.materials)
        self.materials.insert(value.key, value)
    def add_mesh(self, value):
        value.key = len(self.meshes)
        self.meshes.insert(value.key, value)
    def add_node(self, value):
        value.key = len(self.nodes)
        self.nodes.insert(value.key, value)
    def add_sampler(self, value):
        value.key = len(self.samplers)
        self.samplers.insert(value.key, value)
    def add_scene(self, value):
        value.key = len(self.scenes)
        self.scenes.insert(value.key, value)
    def add_skin(self, value):
        value.key = len(self.skins)
        self.skins.insert(value.key, value)
    def add_texture(self, value):
        value.key = len(self.textures)
        self.textures.insert(value.key, value)
    
    def add_accessors(self, values):
        for value in values:
            self.add_accessor(value)
    def add_animations(self, values):
        for value in values:
            self.add_animation(value)
    def add_buffers(self, values):
        for value in values:
            self.add_buffer(value)
    def add_buffer_views(self, values):
        for value in values:
            self.add_buffer_view(value)
    def add_cameras(self, values):
        for value in values:
            self.add_camera(value)
    def add_images(self, values):
        for value in values:
            self.add_image(value)
    def add_materials(self, values):
        for value in values:
            self.add_material(value)
    def add_meshes(self, values):
        for value in values:
            self.add_mesh(value)
    def add_nodes(self, values):
        for value in values:
            self.add_node(value)
    def add_samplers(self, values):
        for value in values:
            self.add_sampler(value)
    def add_scenes(self, values):
        for value in values:
            self.add_scene(value)
    def add_skins(self, values):
        for value in values:
            self.add_skin(value)
    def add_textures(self, values):
        for value in values:
            self.add_texture(value)
    
    def togltf(self):
        result = {}
        result["asset"] = self.asset
        if self.buffers:
            result["buffers"]     = [buffer.togltf()      for buffer      in self.buffers]
        if self.bufferViews:
            result["bufferViews"] = [bufferView.togltf()  for bufferView  in self.bufferViews]
        if self.accessors:
            result["accessors"]   = [accessor.togltf()    for accessor    in self.accessors]
        if self.animations:
            result["animations"]  = [animation.togltf()   for animation   in self.animations]
        if self.cameras:
            result["cameras"]     = [camera.togltf()      for camera      in self.cameras]
        if self.images:
            result["images"]      = [image.togltf()       for image       in self.images]
        if self.materials:
            result["materials"]   = [material.togltf()    for material    in self.materials]
        if self.meshes:
            result["meshes"]      = [mesh.togltf()        for mesh        in self.meshes]
        if self.nodes:
            result["nodes"]       = [node.togltf()        for node        in self.nodes]
        if self.samplers:
            result["samplers"]    = [sampler.togltf()     for sampler     in self.samplers]
        if self.scenes:
            result["scenes"]      = [scene.togltf()       for scene       in self.scenes]
        if self.skins:
            result["skins"]       = [skin.togltf()        for skin        in self.skins]
        if self.textures:
            result["textures"]    = [texture.togltf()     for texture     in self.textures]
        if self.scene:
            result["scene"] = self.scene.key
        return result

glTF = Document


class Accessor(Object):
    def __init__(self, bufferView, byteOffset=None, count=0, type=AccessorType.SCALAR, componentType=ComponentType.FLOAT, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key  = -1
        self.bufferView = bufferView
        self.byteOffset = byteOffset
        self.componentType = componentType
        self.normalized = False
        self.count = count
        self.type = type
        self.max = kwargs.get("max")
        self.min = kwargs.get("min")
        self.sparse = kwargs.get("sparse")
    def togltf(self):
        result = super().togltf()
        result["bufferView"] = self.bufferView.key
        result["componentType"] = self.componentType.value
        result["count"] = self.count
        result["type"] = self.type.value
        if self.byteOffset is not None:
            result["byteOffset"] = self.byteOffset
        if self.max:
            result["max"] = self.max
        if self.min:
            result["min"] = self.min
        if self.sparse:
            result["sparse"] = self.sparse.togltf()
        return result


class AccessorSparse(object):
    def __init__(self, count, indices, values, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.count = count
        self.indices = indices
        self.values = values
    def togltf(self):
        result = {}
        result["count"] = self.count
        result["indices"] = self.indices.togltf()
        result["values"] = self.values.togltf()
        return result

Accessor.Sparse = AccessorSparse


class AccessorSparseIndices(object):
    def __init__(self, bufferView, byteOffset=None, componentType=ComponentType.UNSIGNED_BYTE, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.bufferView = bufferView
        self.byteOffset = byteOffset
        self.componentType = componentType
    def togltf(self):
        result = {}
        result["bufferView"] = self.bufferView.key
        result["componentType"] = self.componentType.value
        if self.byteOffset is not None:
            result["byteOffset"] = self.byteOffset
        return result

Accessor.Sparse.Indices = AccessorSparseIndices


class AccessorSparseValues(object):
    def __init__(self, bufferView, byteOffset=None, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.bufferView = bufferView
        self.byteOffset = byteOffset
    def togltf(self):
        result = {}
        result["bufferView"] = self.bufferView.key
        if self.byteOffset is not None:
            result["byteOffset"] = self.byteOffset
        return result
        
Accessor.Sparse.Values = AccessorSparseValues


class Animation(Object):
    def __init__(self, channels, samplers, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.key   = -1
        self.channels = channels
        self.samplers = samplers
    def togltf(self):
        result = super().togltf()
        result["channels"] = [channel.togltf() for channel in self.channels]
        result["samplers"] = [sampler.togltf() for sampler in self.samplers]
        return result


class AnimationChannel(object):
    def __init__(self, sampler, target, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.sampler = sampler
        self.target = target
    def togltf(self):
        result = {}
        result["sampler"] = self.sampler
        result["target"] = self.target.key
        return result
    
Animation.Channel = AnimationChannel


class AnimationSampler(Object):
    def __init__(self, input, output, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.input = input
        self.output = output
        self.interpolation = kwargs.get("interpolation")
    def togltf(self):
        result = {}
        result["input"] = self.input.key
        result["output"] = self.output.key
        result["interpolation"] = self.interpolation.value
        return result

Animation.Sampler = AnimationSampler


class Buffer(Object):
    def __init__(self, byteLength=0, uri=None, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.key   = -1
        self.byteLength = byteLength
        self.uri = uri
    def togltf(self):
        result = super().togltf()
        result["byteLength"] = self.byteLength
        if self.uri:
            result["uri"] =  self.uri
        return result


class BufferView(Object):
    def __init__(self, buffer, byteOffset=None, byteLength=0, byteStride=None, target=BufferTarget.ARRAY_BUFFER, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key    = -1
        self.buffer = buffer
        self.byteOffset = byteOffset
        self.byteLength = byteLength
        self.byteStride = byteStride
        self.target = target
    def togltf(self):
        result = super().togltf()
        result["buffer"] = self.buffer.key
        result["byteLength"] = self.byteLength
        if self.byteOffset is not None:
            result["byteOffset"] = self.byteOffset
        if self.byteStride is not None:
            result["byteStride"] = self.byteStride
        if self.target:
            result["target"] = self.target.value
        return result


class Camera(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.orthographic = kwargs.get("orthographic")
        self.perspective = kwargs.get("perspective")
        self.type = kwargs.get("type")
    def togltf(self):
        result = super().togltf()
        if self.orthographic:
            result["orthographic"] = self.orthographic.togltf()
        if self.perspective:
            result["perspective"] = self.perspective.togltf()
        if self.type:
            result["type"] = self.type
        return result


class CameraOrthographic(Object):
    def __init__(self, xmag, ymag, zfar, znear, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.xmag = xmag
        self.ymag = ymag
        self.zfar = zfar
        self.znear = znear
    def togltf(self):
        result = super().togltf()
        result["xmag"] = self.xmag
        result["ymag"] = self.ymag
        result["zfar"] = self.zfar
        result["znear"] = self.znear
        return result

Camera.Orthographic = CameraOrthographic


class CameraPerspective(Object):
    def __init__(self, yfov, znear, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.aspectRatio = kwargs.get("aspectRatio")
        self.yfov = yfov
        self.zfar = kwargs.get("zfar")
        self.znear = znear
    def togltf(self):
        result = super().togltf()
        if self.aspectRatio:
            result["aspectRatio"] = self.aspectRatio
        result["yfov"] = self.yfov
        if self.zfar:
            result["zfar"] = self.zfar
        result["znear"] = self.znear
        return result

Camera.Perspective = CameraPerspective


class Image(Object):
    def __init__(self, uri=None, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.key  = -1
        self.uri = uri
        self.mimeType = kwargs.get("mimeType")
        self.bufferView = kwargs.get("bufferView")
    def togltf(self):
        result = super().togltf()
        if self.uri:
            result["uri"] = self.uri
        if self.mimeType:
            result["mimeType"] = self.mimeType
        if self.bufferView:
            result["bufferView"] = self.bufferView.key
        return result


class Material(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.key  = -1
        self.pbrMetallicRoughness = kwargs.get("pbrMetallicRoughness")
        self.normalTexture = kwargs.get("normalTexture")
        self.occlusionTexture = kwargs.get("occlusionTexture")
        self.emissiveTexture = kwargs.get("emissiveTexture")
        self.emissiveFactor = kwargs.get("emissiveFactor")
        self.alphaMode = kwargs.get("alphaMode")
        self.alphaCutoff = kwargs.get("alphaCutoff")
        self.doubleSided = kwargs.get("doubleSided")
    def togltf(self):
        result = super().togltf()
        if self.pbrMetallicRoughness:
            result["pbrMetallicRoughness"] = self.pbrMetallicRoughness.togltf()
        if self.normalTexture:
            result["normalTexture"] = self.normalTexture.togltf()
        if self.occlusionTexture:
            result["occlusionTexture"] = self.occlusionTexture.togltf()
        if self.emissiveTexture:
            result["emissiveTexture"] = self.emissiveTexture.togltf()
        if self.alphaMode:
            result["alphaMode"] = self.alphaMode.value
        if self.alphaCutoff:
            result["alphaCutoff"] = self.alphaCutoff
        if self.doubleSided:
            result["doubleSided"] = self.doubleSided
        return result


class PBRMetallicRoughness(object):
    def __init__(self, *args, **kwargs):
        self.baseColorFactor = kwargs.get("baseColorFactor")
        self.baseColorTexture = kwargs.get("baseColorTexture")
        self.metallicFactor = kwargs.get("metallicFactor")
        self.roughnessFactor = kwargs.get("roughnessFactor")
        self.metallicRoughnessTexture = kwargs.get("metallicRoughnessTexture")
        self.extensions = kwargs.get("extensions")
        self.extras = kwargs.get("extras")
    def togltf(self):
        result = {}
        if self.baseColorFactor:
            result["baseColorFactor"] = self.baseColorFactor
        if self.baseColorTexture:
            result["baseColorTexture"] = self.baseColorTexture.togltf()
        if self.metallicFactor:
            result["metallicFactor"] = self.metallicFactor
        if self.roughnessFactor:
            result["roughnessFactor"] = self.roughnessFactor
        if self.metallicRoughnessTexture:
            result["metallicRoughnessTexture"] = self.metallicRoughnessTexture.togltf()
        if self.extensions:
            result["extensions"] = self.extensions
        if self.extras:
            result["extras"] = self.extras
        return result

Material.PBRMetallicRoughness = PBRMetallicRoughness

class Mesh(Object):
    def __init__(self, primitives, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.key  = -1
        self.primitives = [] if primitives is None else primitives
        self.weights = kwargs.get('weights')
    def togltf(self):
        result = super().togltf()
        result["primitives"] = [primitive.togltf() for primitive in self.primitives]
        if self.weights:
            result["weights"] =  self.weights
        return result


class Primitive(object):
    def __init__(self, attributes, indices, material, mode=PrimitiveMode.TRIANGLES, **kwargs):
        self.attributes = attributes
        self.indices = indices
        self.material = material
        self.mode = mode
        self.targets = kwargs.get("targets")
        self.extensions = kwargs.get("extensions")
        self.extras = kwargs.get("extras")
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
        if self.targets:
            result["targets"] = self.targets
        if self.extensions:
            result["extensions"] = self.extensions
        if self.extras:
            result["extras"] = self.extras
        return result

Mesh.Primitive = Primitive


class Node(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.key         = -1
        self.camera      = kwargs.get('camera')
        self.children    = kwargs.get('children', [])
        self.skin        = kwargs.get('skin')
        self.matrix      = kwargs.get('matrix')
        self.mesh        = kwargs.get('mesh')
        self.rotation    = kwargs.get('rotation')
        self.scale       = kwargs.get('scale')
        self.translation = kwargs.get('translation')
        self.weights     = kwargs.get('weights')
    def togltf(self):
        result = super().togltf()
        if self.children:
            result["children"] = [child.key for child in self.children]
        if self.camera:
            result["camera"] = self.camera.key
        if self.skin:
            result["skin"] = self.skin.key
        if self.mesh:
            result["mesh"] = self.mesh.key
        if self.matrix:
            result["matrix"] = self.matrix
        if self.rotation:
            result["rotation"] = self.rotation
        if self.scale:
            result["scale"] = self.scale
        if self.translation:
            result["translation"] = self.translation
        if self.weights:
            result["weights"] = self.weights
        return result


class Sampler(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.key   = -1
        self.magFilter = kwargs.get('magFilter')
        self.minFilter = kwargs.get('minFilter')
        self.wrapS = kwargs.get('wrapS')
        self.wrapT = kwargs.get('wrapT')
    def togltf(self):
        result = super().togltf()
        if self.magFilter:
            result["magFilter"] = self.magFilter.value
        if self.minFilter:
            result["minFilter"] = self.minFilter.value
        if self.wrapS:
            result["wrapS"] = self.wrapS.value
        if self.wrapT:
            result["wrapT"] = self.wrapT.value
        return result


class Scene(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.key   = -1
        self.nodes = kwargs.get('nodes', [])
    def togltf(self):
        result = super().togltf()
        result["nodes"] = [node.key for node in self.nodes]
        return result


class Skin(Object):
    def __init__(self, joints, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.key   = -1
        self.inverseBindMatrices = kwargs.get('inverseBindMatrices')
        self.joints = joints
        self.skeleton = kwargs.get('skeleton')
    def togltf(self):
        result = super().togltf()
        if self.inverseBindMatrices:
            result["inverseBindMatrices"] = self.inverseBindMatrices.key
        if self.joints:
            result["joints"] = [joint.key for joint in self.joints]
        if self.skeleton:
            result["skeleton"] = self.skeleton.key
        return result


class Texture(Object):
    def __init__(self, sampler=None, source=None, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.sampler = sampler
        self.source = source
    def togltf(self):
        result = super().togltf()
        if self.sampler:
            result["sampler"] = self.sampler.key
        if self.source:
            result["source"] = self.source.key
        return result


class TextureInfo(Object):
    def __init__(self, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = index
        self.texCoord = kwargs.get("texCoord")
    def togltf(self):
        result = super().togltf()
        result["index"] = self.index.key
        if self.texCoord:
            result["texCoord"] = self.texCoord
        return result
