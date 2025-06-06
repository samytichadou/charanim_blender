import bpy


def set_active_object(context, object):
    old = context.view_layer.objects.active
    context.view_layer.objects.active = object
    return old

class CHARANIM_OT_keyframe_character(bpy.types.Operator):
    bl_idname = "charanim.keyframe_character"
    bl_label = "Keyframe Character"
    bl_description = "Add keyframe for whole character"
    bl_options = {"INTERNAL", "UNDO"}

    char_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        chars = context.window_manager.charanim_properties.available_characters
        char_entry = chars[self.char_name]
        object = char_entry.rig

        pose_check = False

        rig = object.type == "ARMATURE"

        if rig:
            # out from pose mode
            if context.mode == "POSE":
                pose_check = True
                bpy.ops.object.posemode_toggle()

        # toggle active
        old_active = None
        if not context.active_object == object:
            old_active = set_active_object(context, object)

        # Deselect all
        old_selection = context.selected_objects
        for ob in context.selected_objects:
            ob.select_set(False)

        # select object to keyframe
        object.select_set(True)

        if rig:
            bpy.ops.object.posemode_toggle()
            bpy.ops.anim.keyframe_insert(type='WholeCharacter')

            bpy.ops.object.posemode_toggle()

        else:
            bpy.ops.anim.keyframe_insert()

        # Restore selection
        object.select_set(False)
        for ob in old_selection:
            ob.select_set(True)

        # Restore active object
        if old_active is not None:
            set_active_object(context, old_active)

        if pose_check:
            bpy.ops.object.posemode_toggle()

        self.report({'INFO'}, f"{char_entry.name} keyframed")

        return {'FINISHED'}


def register():
    bpy.utils.register_class(CHARANIM_OT_keyframe_character)

def unregister():
    bpy.utils.unregister_class(CHARANIM_OT_keyframe_character)
