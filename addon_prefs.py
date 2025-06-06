import bpy

class CHARANIM_PF_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    all_armatures : bpy.props.BoolProperty(
        name='All Armatures',
        description='Retrieve all available Armatures, not just the setup ones',
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "all_armatures")

        
# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(__package__)
    return getattr(addon, "preferences", None)


### REGISTER ---
def register():
    bpy.utils.register_class(CHARANIM_PF_addon_prefs)

def unregister():
    bpy.utils.unregister_class(CHARANIM_PF_addon_prefs)
