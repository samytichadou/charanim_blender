import bpy

from . import character_selection as char_select

class CHARANIM_PR_character_collection(bpy.types.PropertyGroup):
    collection          : bpy.props.PointerProperty(type=bpy.types.Collection, name="Collection")
    rig                 : bpy.props.PointerProperty(type=bpy.types.Object, name="Rig")
    isolated            : bpy.props.BoolProperty(name="Isolated", default=False)
    type                : bpy.props.StringProperty(name="Type")


class CHARANIM_PR_props(bpy.types.PropertyGroup):
    available_characters : bpy.props.CollectionProperty(
        type = CHARANIM_PR_character_collection,
        name="Characters",
    )
    character_index : bpy.props.IntProperty(
        name="Character Index",
        default=-1,
        min=-1,
        update=char_select.char_index_callback,
        get=char_select.get_char_index,
        set=char_select.set_char_index,
        description="Select character\n"\
            "Shift to add to/remove from current selection",
    )

    isocoll                     : bpy.props.BoolProperty(name="Isolation Collection", default=False)
    isocoll_count               : bpy.props.IntProperty(name="Isolation Collection Count", default=0)
    previous_scene              : bpy.props.PointerProperty(type=bpy.types.Scene, name="Previous Scene")
    prevent_update              : bpy.props.BoolProperty()
    show_char_details           : bpy.props.BoolProperty(name="Show Details")


### REGISTER ---
def register():
    bpy.utils.register_class(CHARANIM_PR_character_collection)
    bpy.utils.register_class(CHARANIM_PR_props)
    bpy.types.WindowManager.charanim_properties = \
        bpy.props.PointerProperty(type = CHARANIM_PR_props, name="Charanim Properties")
    bpy.types.Object.charanim_collection = \
        bpy.props.PointerProperty(type = bpy.types.Collection, name="Character Collection")

def unregister():
    bpy.utils.unregister_class(CHARANIM_PR_character_collection)
    bpy.utils.unregister_class(CHARANIM_PR_props)
    del bpy.types.WindowManager.charanim_properties
    del bpy.types.Object.charanim_collection
