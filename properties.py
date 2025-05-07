import bpy

class CHARANIM_PR_character_collection(bpy.types.PropertyGroup):
    type:               bpy.props.StringProperty(name='Type')
    collection:         bpy.props.PointerProperty(type=bpy.types.Collection, name="Collection")
    rig:                bpy.props.PointerProperty(type=bpy.types.Object, name="Rig")
    isolated:           bpy.props.BoolProperty(name="Isolated", default=False)


class CHARANIM_PR_props(bpy.types.PropertyGroup):
    available_characters:       bpy.props.CollectionProperty(type = CHARANIM_PR_character_collection, name="Characters")
    iso_collection:                    bpy.props.BoolProperty(name="Isolation Collection", default=False)
    iso_collection_count:              bpy.props.IntProperty(name="Isolation Collection Count", default=0)
    character_index:            bpy.props.IntProperty(
        name="Character Index",
        default=0,
        min=-1,
        update=char_index_callback,
        get=get_char_index,
        set=set_char_index,
    )
    prevent_update:             bpy.props.BoolProperty()
    show_char_details:          bpy.props.BoolProperty(name="Show Details")


### REGISTER ---

def register():
    bpy.utils.register_class(CHARANIM_PR_character_collection)
    bpy.utils.register_class(CHARANIM_PR_props)
    bpy.types.WindowManager.charanim_properties = \
        bpy.props.PointerProperty(type = CHARANIM_PR_props, name="Charanim Properties")
    bpy.types.Object.charanim_type = \
        bpy.props.StringProperty()

def unregister():
    bpy.utils.unregister_class(CHARANIM_PR_character_collection)
    bpy.utils.unregister_class(CHARANIM_PR_props)
    del bpy.types.WindowManager.charanim_properties
    del bpy.types.Object.charanim_type
