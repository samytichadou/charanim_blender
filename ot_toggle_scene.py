import bpy

from . import variables as var

def _link_camera(general_scn, anim_scn):
    if general_scn.camera:
        anim_scn.camera = general_scn.camera
        anim_scn.collection.objects.link(general_scn.camera)

# Deal with not only sound strips # TODO

def _remove_all_sound_strips(scene):
    if scene.sequence_editor:
        for strip in scene.sequence_editor.sequences_all:
            if strip.type=='SOUND':
                scene.sequence_editor.sequences.remove(strip)

def _copy_sound_strips(scene_from, scene_to):
    # Copy sound strips
    if not scene_from.sequence_editor:
        return
    scene_to.sequence_editor_create()
    for strip in scene_from.sequence_editor.sequences_all:
        if strip.type=='SOUND':
            sound = strip.sound
            # Create new strip
            new = scene_to.sequence_editor.sequences.new_sound(
                strip.name,
                sound.filepath,
                strip.channel,
                int(strip.frame_start),
                )
            # Remove newly created sound data
            bpy.data.sounds.remove(new.sound)
            # Assign sound
            new.sound = strip.sound
            # get properties
            props = strip.bl_rna.properties
            for p in props:
                try:
                    setattr(new, p.identifier, getattr(strip, p.identifier))
                except AttributeError:
                    pass

def _link_sound(scene_from, scene_to, remove_existing=True):
    # Remove sound strips from scene_to
    if remove_existing:
        _remove_all_sound_strips(scene_to)
    # Copy sound strips
    _copy_sound_strips(scene_from, scene_to)

def _copy_scene_settings(from_scn, to_scn):
    # frame_range
    to_scn.frame_start                  = from_scn.frame_start
    to_scn.frame_end                    = from_scn.frame_end
    # fps
    to_scn.frame_step                   = from_scn.frame_step
    to_scn.render.fps                   = from_scn.render.fps
    to_scn.render.fps_base              = from_scn.render.fps_base
    # output
    to_scn.render.resolution_x          = from_scn.render.resolution_x
    to_scn.render.resolution_y          = from_scn.render.resolution_y
    to_scn.render.resolution_percentage = from_scn.render.resolution_percentage

def _copy_anim_settings(from_scn, to_scn):
    # preview frame_range
    to_scn.use_preview_range            = from_scn.use_preview_range
    to_scn.frame_preview_start          = from_scn.frame_preview_start
    to_scn.frame_preview_end            = from_scn.frame_preview_end
    # anim
    to_scn.tool_settings.use_keyframe_insert_auto = from_scn.tool_settings.use_keyframe_insert_auto
    to_scn.tool_settings.keyframe_type  = from_scn.tool_settings.keyframe_type
    to_scn.keying_sets.active           = from_scn.keying_sets.active
    to_scn.sync_mode                    = from_scn.sync_mode
    to_scn.use_audio_scrub              = from_scn.use_audio_scrub
    to_scn.use_audio                    = from_scn.use_audio
    to_scn.frame_current                = from_scn.frame_current

def _create_scene(scn_name):
    scn = bpy.data.scenes.new()
    scn.name = scn_name
    return scn

def _get_scenes():

    context = bpy.context

    general_scn = _get_general_scene(context)

    if general_scn is None:
        return None, None, False

    datas = bpy.data
    created = False

    try:
        anim_scn = datas.scenes[var.anim_scn_name]
        _copy_scene_settings(general_scn, anim_scn)

    except KeyError:
        # Create scene
        anim_scn = datas.scenes.new(name=var.anim_scn_name)
        _copy_scene_settings(general_scn, anim_scn)
        _copy_anim_settings(general_scn, anim_scn)
        # Set current frame
        anim_scn.frame_current = general_scn.frame_current

        _link_camera(general_scn, anim_scn)
        _link_sound(general_scn, anim_scn)
        created = True

    return anim_scn, general_scn, created

def _switch_to_scene(scn):
    try:
        bpy.context.window.scene = scn
    except KeyError:
        print(f'CHARANIM --- Unable to find Scene named "{scene_name}"')

def _get_general_scene(context):
    props = context.window_manager.charanim_properties

    general_scn = None
    if context.scene.name != var.anim_scn_name:
        return context.scene
    elif props.previous_scene:
        return props.previous_scene
    else:
        for scn in bpy.data.scenes:
            if scn.name != var.anim_scn_name:
                return scn


class CHARANIM_OT_toggle_scene(bpy.types.Operator):
    bl_idname = "charanim.toggle_scene"
    bl_label = "Toggle Scene"
    bl_description = "Toggle between Current and Animation temp scene"
    bl_options = {"UNDO", "INTERNAL"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        # Prevent missing scene
        if len(bpy.data.scenes) == 1\
        and bpy.data.scenes[0].name == var.anim_scn_name:
            self.report({'WARNING'}, "Missing scene")
            return {"CANCELLED"}

        props = context.window_manager.charanim_properties

        # Get scenes

        anim_scn, general_scn, created = _get_scenes()

        # Prevent missing scene
        if general_scn is None:
            self.report({'WARNING'}, "Missing scene")
            return {"CANCELLED"}

        if not created:
            _link_sound(general_scn, anim_scn)

        if context.scene != anim_scn:
            props.previous_scene = context.scene
            _copy_anim_settings(general_scn, anim_scn)
            _switch_to_scene(anim_scn)

        else:
            _copy_anim_settings(anim_scn, general_scn)
            _switch_to_scene(general_scn)
            props.previous_scene = None

        return {'FINISHED'}


def register():
    bpy.utils.register_class(CHARANIM_OT_toggle_scene)

def unregister():
    bpy.utils.unregister_class(CHARANIM_OT_toggle_scene)
