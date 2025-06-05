import bpy

from . import ot_toggle_scene as toggle
from . import variables as var


def _get_isolation_collection():

    datas = bpy.data
    try:
        coll = datas.collections[var.iso_coll_name]
    except KeyError:
        coll = datas.collections.new(var.iso_coll_name)

    return coll


class CHARANIM_OT_manage_isolate_collection(bpy.types.Operator):
    bl_idname = "charanim.manage_isolate_collection"
    bl_label = "Organise Isolation Collection"
    bl_description = "Add/Remove objects, Delete collection or Link it in Animation temp scene"
    bl_options = {"UNDO", "INTERNAL"}

    behavior: bpy.props.EnumProperty(
        items = [
            ("ADD", "Add", ""),
            ("REMOVE", "Remove", ""),
            ("DELETE", "Delete collection", ""),
            ("LINK", "Link/Unlink to scene", ""),
            ]
        )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        datas = bpy.data

        anim_scn, general_scn, created = toggle._get_scenes()

        # Prevent missing scene
        if general_scn is None:
            self.report({'WARNING'}, "Missing scene")
            return {"CANCELLED"}

        props = context.window_manager.charanim_properties

        # Delete collection
        if self.behavior=="DELETE":
            try:
                datas.collections.remove(datas.collections[var.iso_coll_name])
                props.isocoll=props.isocoll_count=0
                self.report({'INFO'}, "Isolation Collection Deleted")
            except KeyError:
                self.report({'WARNING'}, "No Isolation Collection to clear")
            return {'FINISHED'}

        iso_coll = _get_isolation_collection()

        # Link or Unlink objects to collection
        if self.behavior in {"ADD", "REMOVE"}:

            if self.behavior=="ADD":
                for ob in context.selected_objects:
                    try:
                        iso_coll.objects.link(ob)
                        props.isocoll_count+=1
                    except RuntimeError:
                        print(f"CHARANIM --- {ob.name} already in collection")
                # Link coll to anim scene
                try:
                    anim_scn.collection.children.link(iso_coll)
                except RuntimeError:
                    print(f"CHARANIM --- Isolation collection already in anim scene")

                props.isocoll=True
                self.report({'INFO'}, "Objects linked in Isolation Collection")

            elif self.behavior=="REMOVE":
                for ob in context.selected_objects:
                    try:
                        iso_coll.objects.unlink(ob)
                        props.isocoll_count-=1
                    except RuntimeError:
                        print(f"CHARANIM --- {ob.name} not in collection")

                self.report({'INFO'}, "Objects unlinked from Isolation Collection")

        # Link or unlink coll to scene
        elif self.behavior=="LINK":

            # Link/Unlink Character collection
            try:
                anim_scn.collection.children.link(iso_coll)
                props.isocoll=True

                self.report({'INFO'}, "Isolation Collection linked")

            except RuntimeError:
                anim_scn.collection.children.unlink(iso_coll)
                props.isocoll=False

                self.report({'INFO'}, "Isolation Collection unlinked")

        return {'FINISHED'}


class CHARANIM_OT_select_isocoll_objects(bpy.types.Operator):
    bl_idname = "charanim.select_isocoll_objects"
    bl_label = "Select Objects"
    bl_description = "Select Isolation Collection objects\n"\
        "Shift to add it to current selection"
    bl_options = {"UNDO", "INTERNAL"}

    shift = False

    @classmethod
    def poll(cls, context):
        try:
            return bpy.data.collections[var.iso_coll_name].objects
        except KeyError:
            return False

    def invoke(self, context, event):
        if event.shift:
            self.shift=True
        return self.execute(context)

    def execute(self, context):
        coll = bpy.data.collections[var.iso_coll_name]

        # Deselect all if needed
        if not self.shift:
            for obj in context.selected_objects:
                obj.select_set(False)
            context.view_layer.objects.active = coll.objects[0]

        for ob in coll.objects:
            ob.select_set(True)

        self.report({'INFO'}, "Objects selected")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(CHARANIM_OT_manage_isolate_collection)
    bpy.utils.register_class(CHARANIM_OT_select_isocoll_objects)

def unregister():
    bpy.utils.unregister_class(CHARANIM_OT_manage_isolate_collection)
    bpy.utils.unregister_class(CHARANIM_OT_select_isocoll_objects)
