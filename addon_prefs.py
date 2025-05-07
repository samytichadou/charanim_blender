import bpy

class CHARANIM_PF_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    debug : bpy.props.BoolProperty(
        name='Debug',
        )

    def draw(self, context):
        layout = self.layout
        
        layout.prop(self, "debug")

        
# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(__package__)
    return getattr(addon, "preferences", None)


### REGISTER ---
def register():
    bpy.utils.register_class(CHARANIM_PF_addon_prefs)

def unregister():
    bpy.utils.unregister_class(CHARANIM_PF_addon_prefs)
