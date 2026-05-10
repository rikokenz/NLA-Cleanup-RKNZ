bl_info = {
    "name": "NLA Empty Track Cleanup RKNZ",
    "author": "Rikokenz",
    "version": (1, 2, 0),
    "blender": (4, 2, 0),
    "location": "NLA Editor > Sidebar > RKNZ",
    "description": "Quickly remove all empty NLA tracks (tracks with no strips) from your scene with one click.",
    "category": "Animation",
}

import bpy
from bpy.props import IntProperty

TAB = "RKNZ"


class NLA_OT_rknz_delete_empty_tracks(bpy.types.Operator):
    bl_idname = "nla.rknz_delete_empty_tracks"
    bl_label = "Delete Empty NLA Tracks"
    bl_description = "Remove all NLA tracks that contain no strips"
    bl_options = {'UNDO'}

    empty_count: IntProperty(default=0)

    def count_empty_tracks(self):
        count = 0
        for obj in bpy.data.objects:
            ad = obj.animation_data
            if not ad:
                continue
            count += sum(1 for t in ad.nla_tracks if not t.strips)
        return count

    def invoke(self, context, event):
        self.empty_count = self.count_empty_tracks()
        if self.empty_count == 0:
            self.report({'INFO'}, "No empty NLA tracks found")
            return {'CANCELLED'}
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        removed = 0
        for obj in bpy.data.objects:
            ad = obj.animation_data
            if not ad:
                continue
            empty_tracks = [t for t in ad.nla_tracks if not t.strips]
            for track in empty_tracks:
                ad.nla_tracks.remove(track)
                removed += 1
        self.report({'INFO'}, f"Removed {removed} empty NLA tracks")
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text=f"This will delete {self.empty_count} empty NLA track(s).")
        layout.label(text="This action cannot be undone.")


class NLA_PT_rknz_cleanup(bpy.types.Panel):
    bl_label = "NLA Cleanup"
    bl_idname = "NLA_PT_rknz_cleanup"
    bl_space_type = 'NLA_EDITOR'
    bl_region_type = 'UI'
    bl_category = TAB

    def draw(self, context):
        layout = self.layout
        layout.operator("nla.rknz_delete_empty_tracks", icon='TRASH')


classes = (
    NLA_OT_rknz_delete_empty_tracks,
    NLA_PT_rknz_cleanup,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
