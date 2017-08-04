#this script is dedicated to the public domain under CC0 (https://creativecommons.org/publicdomain/zero/1.0/)
#do whatever you want with it! -Bram

#   TODO
#-precision mode for rotation
#-draw on screen handles that fit with Blender's transform tools

bl_info = {
    "name": "BRM UVTools",
    "category": "UV",
    "author": "Bram Eulaers",
    "description": "Edit selected faces'UVs directly inside the 3D Viewport. WIP. Check for updates @leukbaars",
    "version": (0, 6)
}

import bpy
from bpy.props import EnumProperty, BoolProperty

locals_list = locals()
if "BRM_UVTranslate" in locals_list:
    from importlib import reload
    reload(BRM_UVTranslate)
    reload(BRM_UVRotate)
    reload(BRM_UVScale)
else:
    from . import BRM_UVTranslate, BRM_UVRotate, BRM_UVScale


uvmenutype = [("SUBMENU", "Submenu", ""),
              ("INDIVIDUAL", "Individual Entries", "")]


class BRMUVToolsPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    adduvmenu = BoolProperty(name="Add BRM UVTools to UV Menu", default=True)
    individualorsubmenu = EnumProperty(name="Individual or Sub-Menu", items=uvmenutype, default="SUBMENU")

    def draw(self, context):
        layout=self.layout

        column = layout.column(align=True)

        row = column.row()
        row.prop(self, "adduvmenu")
        if self.adduvmenu:
            row.prop(self, "individualorsubmenu", expand=True)


class BRM_UVMenu(bpy.types.Menu):
    bl_label = "BRM UV Tools"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator("brm.uvtranslate", text="UVTranslate")
        col.operator("brm.uvrotate", text="UVRotate")
        col.operator("brm.uvscale", text="UVScale")


def uv_menu_func(self, context):
    if prefs().adduvmenu:
        if prefs().individualorsubmenu == "SUBMENU":
            self.layout.menu("BRM_UVMenu")
        else:
            layout = self.layout

            col = layout.column()
            col.operator_context = 'INVOKE_DEFAULT'
            col.operator("brm.uvtranslate", text="BRM UVTranslate")
            col.operator("brm.uvrotate", text="BRM UVRotate")
            col.operator("brm.uvscale", text="BRM UVScale")

        self.layout.separator()


def prefs():
    return bpy.context.user_preferences.addons[__name__].preferences


def register():
    bpy.utils.register_class(BRMUVToolsPreferences)
    bpy.utils.register_class(BRM_UVMenu)
    bpy.utils.register_class(BRM_UVPanel)
    bpy.utils.register_class(BRM_UVTranslate.UVTranslate)
    bpy.utils.register_class(BRM_UVRotate.UVRotate)
    bpy.utils.register_class(BRM_UVScale.UVScale)

    if prefs().adduvmenu:
        bpy.types.VIEW3D_MT_uv_map.prepend(uv_menu_func)


def unregister():
    bpy.utils.unregister_class(BRM_UVMenu)
    bpy.utils.unregister_class(BRM_UVPanel)
    bpy.utils.unregister_class(BRM_UVTranslate.UVTranslate)
    bpy.utils.unregister_class(BRM_UVRotate.UVRotate)
    bpy.utils.unregister_class(BRM_UVScale.UVScale)


if __name__ == "__main__":
    register()
