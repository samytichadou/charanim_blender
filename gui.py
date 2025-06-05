import bpy
import types

from . import variables as var


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

        if item.type == "ARMATURE":
            icon = "ARMATURE_DATA"
        else:
            icon = "OBJECT_DATAMODE"

        row.label(
            text = item.name,
            icon = icon,
            )
        sub = row.row()
        sub.alignment = 'RIGHT'

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
                icon = var.iso_icon
            else:
                icon = var.no_iso_icon
            op = col1.operator("charanim.isolate_character", text="", icon=icon, emboss=False)
            op.char_name = item.name

            #row.separator()
            col2.prop(item.collection, "hide_select", text="", emboss=False)
            col3.prop(item.collection, "hide_viewport", text="", emboss=False)
            col4.prop(item.collection, "hide_render", text="", emboss=False)

            # op = col4.operator("charanim.rig_add_char_keyframes", text="", icon="DECORATE_KEYFRAME", emboss=False) # TODO
            # op.char_index = index # TODO


def draw_scene_switcher(scene, container):
    sub=container.row()
    if scene.name==var.anim_scn_name:
        sub.alert = True
        icon = var.iso_icon
    else:
        icon = var.no_iso_icon
    sub.operator("charanim.toggle_scene", text="", icon=icon, emboss=False)


def draw_rig_selector_header(context, layout):
    row = layout.row(align=True)
    row.label(text="Characters")
    row.separator()
    row.operator("charanim.refresh_character_list", icon='FILE_REFRESH', text="", emboss=False)
    draw_scene_switcher(context.scene, row)


def draw_rig_selector(context, layout):
    scn = context.scene
    props = context.window_manager.charanim_properties

    big_col = layout.column(align=True)

    # Isolated collection
    anim_scn = scn.name != var.anim_scn_name

    box = big_col.box()
    row=box.row(align=True)
    sub0 = row.row(align=True)
    sub0.alignment="LEFT"
    sub0.operator(
        "charanim.select_isocoll_objects",
        text=f"{str(props.isocoll_count)} - IsoColl",
        emboss=False,
        icon="OUTLINER_COLLECTION",
        )

    sub1=row.row(align=True)
    # sub0.scale_x=0.8
    sub1.alignment="CENTER"
    sub1b=sub1.row(align=True)
    sub1b.enabled=anim_scn
    sub1b.operator("charanim.manage_isolate_collection", text="", icon="ADD").behavior="ADD"
    sub1.operator("charanim.manage_isolate_collection", text="", icon="REMOVE").behavior="REMOVE"
    sub1.operator("charanim.manage_isolate_collection", text="", icon="X").behavior="DELETE"

    sub2=row.row(align=True)
    sub2.alignment="RIGHT"

    if props.isocoll:
        icon = var.iso_icon
    else:
        icon = var.no_iso_icon
    sub2.operator("charanim.manage_isolate_collection", text="", icon=icon, emboss=False).behavior="LINK"
    try:
        coll = bpy.data.collections['_anim_temp']
    except KeyError:
        coll = None
    if coll is not None:
        sub2.prop(coll, "hide_select", text="", emboss=False)
        sub2.prop(coll, "hide_viewport", text="", emboss=False)

    big_col.template_list(
        "CHARANIM_UL_character_selector",
        "",
        props,
        "available_characters",
        props,
        "character_index",
        rows = 3,
        )


def copy_func(f, name=None):
    fn = types.FunctionType(f.__code__, f.__globals__, name or f.__name__,
        f.__defaults__, f.__closure__)
    # in case f was given attrs (note this dict is a shallow copy):
    fn.__dict__.update(f.__dict__)
    return fn


draw_xform_copy = copy_func(bpy.types.VIEW3D_HT_header.draw_xform_template)


def charanim_override_xform(layout, context):
    draw_xform_copy(layout, context)
    layout.popover(panel="CHARANIM_PT_rig_selector_popover", text="", icon="MESH_MONKEY")


class CHARANIM_PT_rig_selector_popover(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_label = "Characters"
    bl_ui_units_x = 12

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        draw_rig_selector_header(context, self.layout)
        draw_rig_selector(context, self.layout)


class CHARANIM_PT_object_properties(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_label = "Charanim"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        self.layout.prop(context.active_object, "charanim_collection", text="")


# anim topbar
def scene_rig_topbar(self, context):
    if context.region.alignment == 'RIGHT':
        layout=self.layout
        draw_scene_switcher(context.scene, layout)


### REGISTER ---
def register():
    bpy.utils.register_class(CHARANIM_UL_character_selector)
    bpy.utils.register_class(CHARANIM_PT_rig_selector_popover)
    bpy.utils.register_class(CHARANIM_PT_object_properties)

    bpy.types.VIEW3D_HT_header.draw_xform_template = charanim_override_xform
    bpy.types.TOPBAR_HT_upper_bar.prepend(scene_rig_topbar)

def unregister():
    bpy.utils.unregister_class(CHARANIM_UL_character_selector)
    bpy.utils.unregister_class(CHARANIM_PT_rig_selector_popover)
    bpy.utils.unregister_class(CHARANIM_PT_object_properties)

    # bpy.types.VIEW3D_HT_header.draw_xform_template = charanim_override_xform
    bpy.types.TOPBAR_HT_upper_bar.remove(scene_rig_topbar)
