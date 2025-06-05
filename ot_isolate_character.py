import bpy

from . import ot_toggle_scene as toggle


class CHARANIM_OT_isolate_character(bpy.types.Operator):
    bl_idname = "charanim.isolate_character"
    bl_label = "Isolate Character"
    bl_description = "Isolate Character in Animation temp Scene"
    bl_options = {"UNDO", "INTERNAL"}

    char_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        datas = bpy.data
        props = context.window_manager.charanim_properties
        chars = props.available_characters

        # Get rig object
        try:
            char_entry = chars[self.char_name]
            char_object = char_entry.rig
        except KeyError:
            self.report({'WARNING'}, f"{self.char_name} : no base object available")
            return {'CANCELLED'}

        # Get rig collection
        if not char_entry.collection:
            self.report({'WARNING'}, f"{self.char_name} : no collection available")
            return {'CANCELLED'}

        char_coll = char_entry.collection

        # Get scenes
        anim_scn, general_scn, created = toggle._get_scenes()

        # Prevent missing scene
        if general_scn is None:
            self.report({'WARNING'}, "Missing scene")
            return {"CANCELLED"}

        # Check if coll exists
        chk_exist = False
        for coll in anim_scn.collection.children_recursive:
            if coll==char_coll:
                chk_exist = True
                break

        # Link/Unlink Character collection
        if chk_exist:
            anim_scn.collection.children.unlink(char_coll)
            char_entry.isolated = False
            msg = f'{char_coll.name} unlinked to Animation Scene'

        else:
            anim_scn.collection.children.link(char_coll)
            char_entry.isolated = True
            msg = f'{char_coll.name} linked to Animation Scene'

        self.report({'INFO'}, msg)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(CHARANIM_OT_isolate_character)

def unregister():
    bpy.utils.unregister_class(CHARANIM_OT_isolate_character)
