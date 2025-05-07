import bpy

class CHARANIM_UL_character_selector(bpy.types.UIList):

    use_filter_scene : bpy.props.BoolProperty(
        name = "Filter by Current Scene",
        description="Show only characters from current scene",
        )

    use_filter_sort_reverse: bpy.props.BoolProperty(
        name="Reverse",
        default=False,
        #options=set(),
        description="Reverse the order of shown items",
    )
    use_filter_sort_alpha: bpy.props.BoolProperty(
        name="Filter by Name",
        default=False,
        #options=set(),
        description="Sort groups by their name",
    )
    filter_name: bpy.props.StringProperty(
        name="Filter by Name",
        default = "",
        description="Filter items by name",
        options = {"TEXTEDIT_UPDATE"},
    )
    use_filter_invert: bpy.props.BoolProperty(
        name="Invert",
        default = False,
        #options=set(),
        description="Invert Filtering"
    )

    def filter_items(self, context, data, property):

        items = getattr(data, property)
        if not len(items):
            return [], []

        # https://docs.blender.org/api/current/bpy.types.UI_UL_list.html
        # helper functions for handling UIList objects.
        if self.filter_name:
            flt_flags = bpy.types.UI_UL_list.filter_items_by_name(
                    self.filter_name,
                    self.bitflag_filter_item,
                    items,
                    propname="name",
                    reverse=self.use_filter_invert)
        else:
            flt_flags = [self.bitflag_filter_item] * len(items)

        if self.use_filter_scene:
            for i, item in enumerate(items):
                if item.collection not in context.scene.collection.children_recursive:
                    flt_flags[i] &= ~self.bitflag_filter_item

        # https://docs.blender.org/api/current/bpy.types.UI_UL_list.html
        # helper functions for handling UIList objects.
        flt_neworder = []

        # if self.use_filter_sort_alpha:
        #     flt_neworder = bpy.types.UI_UL_list.sort_items_by_name(items, "name")

        if self.use_filter_sort_reverse:
            flt_neworder = [i for i, item in enumerate(items)]
            flt_neworder.reverse()

        return flt_flags, flt_neworder

    def draw_filter(self, context, layout):

        row = layout.row(align=True)
        row.prop(self, "use_filter_scene", text="", icon="SCENE_DATA")
        row.prop(self, "filter_name", text="")
        row.prop(self, "use_filter_invert", text="", icon="ARROW_LEFTRIGHT")
        row.separator()
        #row.prop(self, "use_filter_sort_alpha", text="", icon="SORTALPHA")
        icon = 'SORT_DESC' if self.use_filter_sort_reverse else 'SORT_ASC'
        row.prop(self, "use_filter_sort_reverse", text="", icon=icon)

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # We could write some code to decide which icon to use here... custom_icon = 'OBJECT_DATAMODE'
        # Make sure your code supports all 3 layout types

        ob = item.rig

        # row = layout.row(align=True)
        # row.alignment = 'LEFT'
        split = layout.split(factor=0.7)
        bcol0 = split.column()
        bcol1 = split.column()

        row = bcol0.row(align=True)
        #row.alignment = 'LEFT'
        if ob.select_get():
            if context.view_layer.objects.active==ob:
                icon="PROP_CON"
            else:
                icon="RADIOBUT_ON"
        else:
            icon="RADIOBUT_OFF"
        row.label(text="", icon=icon)
        if ob.type=="ARMATURE":
            icon="ARMATURE_DATA"
        else:
            icon="OBJECT_DATAMODE"
        row.label(
            text=item.name,
            icon=icon,
            )
        sub = row.row()
        sub.alignment = 'RIGHT'
        sub.label(text=item.type.upper())

        # row = layout.row(align=True)
        # row.alignment = 'RIGHT'
        split = bcol1.split()
        col1 = split.column()
        col2 = split.column()
        col3 = split.column()
        col4 = split.column()


        if item.collection:
            #row.separator()
            # Isolate
            if item.isolated:
                icon = "PINNED"
            else:
                icon = "UNPINNED"
            op = col1.operator("charanim.isolate_character", text="", icon=icon, emboss=False)
            op.char_index = index

            #row.separator()
            col2.prop(item.collection, "hide_select", text="", emboss=False)
            col3.prop(item.collection, "hide_viewport", text="", emboss=False)
            #row.prop(item.collection, "hide_render", text="", emboss=False)

            op = col4.operator("charanim.rig_add_char_keyframes", text="", icon="DECORATE_KEYFRAME", emboss=False)
            op.char_index = index


def draw_scene_switcher(scene, container):
    sub=container.row()
    if scene.name=="_anim_temp":
        sub.alert = True
        icon = "PINNED"
    else:
        icon = "UNPINNED"
    sub.operator("charanim.change_scene", text="", icon=icon, emboss=False)

def draw_rig_selector(context, layout):
    scn = context.scene
    rig_props = context.window_manager.woolly_rig_properties
    chars = rig_props.available_characters

    big_col = layout.column(align=True)

    # Isolated collection
    anim_scn = scn.name!="_anim_temp"
    box = big_col.box()
    row=box.row(align=True)
    split = row.split(factor=0.7)
    #split = row.split(factor=0.3)
    bcol0 = split.column()
    bcol1 = split.column()
    row = bcol0.row(align=True)
    sub = row.row(align=True)
    sub.alignment="LEFT"
    sub.operator(
        "woolly.select_isocoll",
        text=f"{str(rig_props.isocoll_count)} - IsoColl",
        emboss=False,
        icon="OUTLINER_COLLECTION",
        )

    sub0=row.row(align=True)
    sub0.scale_x=0.8
    sub0.alignment="RIGHT"
    sub=sub0.row(align=True)
    sub.enabled=anim_scn
    sub.operator("woolly.manage_isolate_collection", text="", icon="ADD").behavior="ADD"
    sub0.operator("woolly.manage_isolate_collection", text="", icon="REMOVE").behavior="REMOVE"
    sub0.operator("woolly.manage_isolate_collection", text="", icon="X").behavior="DELETE"

    split = bcol1.split()
    col1 = split.column()
    col2 = split.column()
    col3 = split.column()
    col4 = split.column()

    # row.separator()
    if rig_props.isocoll:
        icon = "PINNED"
    else:
        icon = "UNPINNED"
    col1.operator("woolly.manage_isolate_collection", text="", icon=icon, emboss=False).behavior="LINK"
    try:
        coll = bpy.data.collections['_anim_temp']
    except KeyError:
        coll = None
    if coll is not None:
        # row.separator()
        col2.prop(coll, "hide_select", text="", emboss=False)
        col3.prop(coll, "hide_viewport", text="", emboss=False)
        #row.label(text="", icon="BLANK1")

    big_col.template_list(
        "WOOLLY_UL_character_selector",
        "",
        rig_props,
        "available_characters",
        rig_props,
        "character_index",
        rows = 3,
        )

def draw_rig_selector_header(context, layout):
    row = layout.row(align=True)
    row.label(text="Personnages")
    row.separator()
    row.operator("woolly.available_character_update", icon='FILE_REFRESH', text="", emboss=False)
    draw_scene_switcher(context.scene, row)
    op=row.operator("woolly.character_list_select", text="", icon="RESTRICT_SELECT_OFF", emboss=False)
    op.char_index=-1

class WOOLLY_PT_rig_selector_viewport_panel(class_c.WOOLLY_anim_panels):
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return get_addon_preferences().character_list_panel=="VIEWPORT"

    def draw_header(self, context):
        draw_rig_selector_header(context, self.layout)

    def draw(self, context):
        draw_rig_selector(context, self.layout)

class WOOLLY_PT_rig_selector_properties_panel(class_c.WOOLLY_anim_properties_panels):
    bl_label = ""

    @classmethod
    def poll(cls, context):
        if not context.area.spaces[0].search_filter:
            return get_addon_preferences().character_list_panel=="PROPERTIES"

    def draw_header(self, context):
        draw_rig_selector_header(context, self.layout)

    def draw(self, context):
        draw_rig_selector(context, self.layout)

class WOOLLY_PT_rig_selector_popover(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_label = "Personnages"
    bl_ui_units_x = 12

    @classmethod
    def poll(cls, context):
        return get_addon_preferences().character_list_panel=="POPOVER"

    def draw(self, context):
        draw_rig_selector_header(context, self.layout)
        draw_rig_selector(context, self.layout)

def copy_func(f, name=None):
    fn = types.FunctionType(f.__code__, f.__globals__, name or f.__name__,
        f.__defaults__, f.__closure__)
    # in case f was given attrs (note this dict is a shallow copy):
    fn.__dict__.update(f.__dict__)
    return fn

draw_xform_copy = copy_func(bpy.types.VIEW3D_HT_header.draw_xform_template)

def ww_override_xform(layout, context):
    draw_xform_copy(layout, context)
    prefs = get_addon_preferences()
    if prefs.animation_panel=="POPOVER":
        layout.popover(panel="WOOLLY_PT_animation_utils_popover", text="", icon="ACTION")
    if prefs.character_list_panel=="POPOVER":
        layout.popover(panel="WOOLLY_PT_rig_selector_popover", text="", icon="MESH_MONKEY")

# anim topbar
def ww_rig_topbar(self, context):
    if context.region.alignment == 'RIGHT':
        layout=self.layout
        #layout.prop(context.window_manager.woolly_rig_properties, "profile_process", text="", icon='MONKEY')
        draw_scene_switcher(context.scene, layout)

class WOOLLY_OT_lock_rig_panel(bpy.types.Operator):
    bl_idname = "woolly.lock_rig_panel"
    bl_label = "Verouiller UI"
    bl_description = "Verouiller UI du rig"
    bl_options = {"INTERNAL"}

    char_name : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.area.type=="PROPERTIES"

    def execute(self, context):
        if not self.char_name:
            self.report({'WARNING'}, "Unavailable rig panel")
            return {'CANCELLED'}

        space = context.area.spaces[0]
        if space.search_filter == self.char_name:
            space.search_filter = ""
            space.use_pin_id = False
            msg = 'Panel unlocked'
        else:
            space.search_filter = self.char_name
            space.use_pin_id = True
            msg = f'{self.char_name} panel locked'

        self.report({'INFO'}, msg)
        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(WOOLLY_UL_character_selector)
    bpy.utils.register_class(WOOLLY_PT_rig_selector_viewport_panel)
    bpy.utils.register_class(WOOLLY_PT_rig_selector_properties_panel)
    bpy.utils.register_class(WOOLLY_PT_rig_selector_popover)
    bpy.types.VIEW3D_HT_header.draw_xform_template = ww_override_xform
    bpy.types.TOPBAR_HT_upper_bar.prepend(ww_rig_topbar)
    bpy.utils.register_class(WOOLLY_OT_lock_rig_panel)

def unregister():
    bpy.utils.unregister_class(WOOLLY_UL_character_selector)
    bpy.utils.unregister_class(WOOLLY_PT_rig_selector_viewport_panel)
    bpy.utils.unregister_class(WOOLLY_PT_rig_selector_properties_panel)
    bpy.utils.unregister_class(WOOLLY_PT_rig_selector_popover)
    bpy.types.VIEW3D_HT_header.draw_xform_template = ww_override_xform
    bpy.types.TOPBAR_HT_upper_bar.remove(ww_rig_topbar)
    bpy.utils.unregister_class(WOOLLY_OT_lock_rig_panel)
