import bpy

class CHARANIM_get_event(bpy.types.Operator):
    bl_idname  = "charanim.get_event"
    bl_label   = ""
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        global _shift_event
        _shift_event = event.shift
        return {'FINISHED'}

def check_rig_in_scene(context, rig_object):
    try:
        context.scene.objects[rig_object.name]
        return True
    except (KeyError, AttributeError):
        print(f"CHARANIM --- {rig_object.name} : No Rig available")
        return False

def select_single_object(context, rig_object):
    for obj in context.selected_objects:
        obj.select_set(False)
    context.view_layer.objects.active = rig_object
    rig_object.select_set(True)

def add_object_to_selection(context, rig_object):
    context.view_layer.objects.active = rig_object
    rig_object.select_set(True)

def remove_object_from_selection(context, rig_object):
    rig_object.select_set(False)
    if context.view_layer.objects.active == rig_object:
        if context.selected_objects:
            context.view_layer.objects.active = context.selected_objects[0]
        else:
            context.view_layer.objects.active = None

def get_out_of_pose_mode(context):
    if context.mode == "POSE":
        bpy.ops.object.posemode_toggle()
        return True
    return False

def get_back_to_pose_mode(context):
    if context.view_layer.objects.active is not None:
        if context.view_layer.objects.active.type=="ARMATURE":
            bpy.ops.object.posemode_toggle()
            return True
    return False

_shift_event = False

def get_char_index(self):
    return self.get("character_index", 0)

def set_char_index(self, value):
    # Refresh shift event
    bpy.ops.charanim.get_event("INVOKE_DEFAULT")

    # Get rig object
    context = bpy.context
    rig_object = self.available_characters[value].rig

    if not check_rig_in_scene(bpy.context, rig_object):
        self.prevent_update = True
        return

    # Get if object has to be deselected
    if _shift_event and rig_object.select_get():

        # Out of pose mode
        pose_chk = get_out_of_pose_mode(context)

        # Deselect
        remove_object_from_selection(context, rig_object)

        # Back in pose mode
        if pose_chk:
            get_back_to_pose_mode(context)

        print(f"CHARANIM --- {rig_object.name} selected/deselected")

        # Prevent callback
        self.prevent_update = True

        # If click on already active, change index
        if value == self.character_index:
            # Try to get active rig
            active = context.active_object
            if active:
                n=0
                for char in self.available_characters:
                    if char.rig==active:
                        self["character_index"] = n
                        return
                    n+=1
            self["character_index"] = -1
        return

    self["character_index"] = value

def char_index_callback(self, context):
    # Check if callback needed
    if self.prevent_update:
        self.prevent_update = False
        return
    if self.character_index < 0\
        or self.character_index >= len(self.available_characters):
        return

    # Shift event already refreshed at set

    # Out of pose mode
    pose_chk = get_out_of_pose_mode(context)

    # Get rig object
    rig_object = self.available_characters[self.character_index].rig
    if not check_rig_in_scene(context, rig_object):
        return

    # Select object
    # Single selection
    if not _shift_event:
        select_single_object(context, rig_object)
    # Multiple selection
    else:
        # Add to selection, set func ensure not selected
        add_object_to_selection(context, rig_object)

    # Back in pose mode
    if pose_chk:
        get_back_to_pose_mode(context)

    print(f"CHARANIM --- {rig_object.name} selected/deselected")


### REGISTER ---
def register():
    bpy.utils.register_class(CHARANIM_get_event)

def unregister():
    bpy.utils.unregister_class(CHARANIM_get_event)
