bl_info = {
    "name": "All Shapekeys Transfer",
    "author": "gogo",
    "version": (0, 0, 1),
    "blender": (2, 83, 0),
    "description": "Transfer all shapekeys from source to target.",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "https://github.com/3str6/all_shapekeys_transfer",
    "category": "3D View"
}

import bpy
from bpy.types import (
    Panel,
)
from bpy.props import (
    PointerProperty,
)

def insane_input(obj_1, obj_2):
    if len(obj_1.data.vertices) == len(obj_2.data.vertices):
        return False
    return True

def insane_source(obj):
    if obj.data.shape_keys:
        return False
    return True


def get_mesh_callback(scene, object):
    return object.type == 'MESH'


class SPKTRNSF_OT_transfer(bpy.types.Operator):
    bl_idname = "spktrnsf.transfer"
    bl_label = "Transfer"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Transfer all shape keys from source to target"

    @classmethod
    def poll(cls, context):
        props = context.scene.spktrnsf
        return props.obj_target and props.obj_source

    def execute(self, context):
        props = context.scene.spktrnsf
        target_object = props.obj_target
        source_object = props.obj_source

        if insane_input(target_object, source_object):
            self.report({'ERROR_INVALID_INPUT'}, "Topology is diffrent")
            return {'CANCELLED'}

        if insane_source(props.obj_source):
            self.report({'ERROR_INVALID_INPUT'}, "There is no shapekeys in Source Object")
            return {'CANCELLED'}
        
        bpy.ops.object.select_all(action='DESELECT')
        source_object.select_set(True)
        target_object.select_set(True)
        context.view_layer.objects.active = target_object

        for i in range(1, len(source_object.data.shape_keys.key_blocks)):
            source_object.active_shape_key_index = i
            bpy.ops.object.shape_key_transfer()

        return {'FINISHED'}


class SPKTRNSF_PT_main(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "For VRoid"
    bl_label = "All Shapekeys Transfer"
    bl_idname = "SPKTRNSF_PT_main"
    bl_context = 'objectmode'
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.spktrnsf
        layout.prop(props, property="obj_target", text="Target")
        layout.prop(props, property="obj_source", text="Source")
        layout.operator(SPKTRNSF_OT_transfer.bl_idname, text=bpy.app.translations.pgettext("Transfer Shapekeys"))


class SPKTRNSF_props(bpy.types.PropertyGroup):
    obj_target: PointerProperty(
        name="Target Object",
        description="Target Object",
        type=bpy.types.Object,
        poll=get_mesh_callback,
    )
    obj_source: PointerProperty(
        name="Source Object",
        description="Source Object",
        type=bpy.types.Object,
        poll=get_mesh_callback,
    )


classes = (
    SPKTRNSF_OT_transfer,
    SPKTRNSF_PT_main,
    SPKTRNSF_props,
)


translation_dict = {
    "en_US": {
        ("*", "Target"): "Target",
        ("*", "Source"): "Source",
        ("*", "Transfer Shapekeys"): "Transfer Shapekeys",
        ("*", "Topology is diffrent"): "Topology is diffrent",
        ("*", "There is no shapekeys in Source Object"): "There is no shapekeys in Source Object",
        ("*", "Transfer all shape keys from source to target"): "Transfer all shape keys from source to target",
    },
    "ja_JP": {
        ("*", "Target"): "ターゲット",
        ("*", "Source"): "ソース",
        ("*", "Transfer Shapekeys"): "シェイプキーの転送",
        ("*", "Topology is diffrent"): "トポロジーが異なっています",
        ("*", "There is no shapekeys in Source Object"): "ソースオブジェクトにシェイプキーが存在しません",
        ("*", "Transfer all shape keys from source to target"): "すべてのシェイプキーをソースからターゲットへ転送します",
    }
}


def register():
    for i in classes:
        bpy.utils.register_class(i)
    
    bpy.types.Scene.spktrnsf = PointerProperty(type=SPKTRNSF_props)
    bpy.app.translations.register(__name__, translation_dict)

def unregister():
    bpy.app.translations.unregister(__name__)
    del bpy.types.Scene.spktrnsf
    for i in classes:
        bpy.utils.unregister_class(i)


if __name__ == "__main__":
    register()
