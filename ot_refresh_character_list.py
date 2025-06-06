import bpy

from bpy.app.handlers import persistent

from .addon_prefs import get_addon_preferences

def get_characters():
    context = bpy.context
    winman = context.window_manager
    props = winman.charanim_properties

    # Clear collection
    props.available_characters.clear()

    all_armatures = get_addon_preferences().all_armatures

    # Get available rigs
    # for ob in bpy.data.objects:
    for ob in context.scene.objects:

        if ob.users == 0:
            continue

        if ob.library:
            continue

        if ob.charanim_collection\
        or (ob.type == "ARMATURE" and all_armatures):

            new = props.available_characters.add()
            new.name = ob.name
            new.rig = ob

            if ob.type == "ARMATURE":
                new.type = "ARMATURE"
            else:
                new.type = "OBJECT"

            if ob.charanim_collection:
                try:
                    coll = bpy.data.collections[ob.charanim_collection.name]
                except KeyError:
                    coll = ob.charanim_collection
                new.collection = coll
                continue

            # Get parent collection
            coll = None

            for c in context.scene.collection.children_recursive:
                if not c.library:
                    for obj in c.objects:
                        if obj == ob:
                            coll = c
                            break
            if coll is None:
                for c in bpy.data.collections:
                    if not c.library:
                        for obj in c.objects:
                            if obj == ob:
                                coll = c
                                break

            new.collection = coll


@persistent
def character_list_handler(scene):
    print("CHARANIM --- Updating character list")
    get_characters()


class CHARANIM_OT_refresh_character_list(bpy.types.Operator):
    bl_idname = "charanim.refresh_character_list"
    bl_label = "Refresh Character List"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        get_characters()
        self.report({'INFO'}, "Character list refreshed")
        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(CHARANIM_OT_refresh_character_list)
    bpy.app.handlers.load_post.append(character_list_handler)

def unregister():
    bpy.utils.unregister_class(CHARANIM_OT_refresh_character_list)
    bpy.app.handlers.load_post.remove(character_list_handler)
