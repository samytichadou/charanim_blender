'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou (tonton)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


# register
##################################

from . import (
    addon_prefs,
    properties,
    gui,
    character_selection,
    ot_refresh_character_list,
    ot_toggle_scene,
    ot_isolate_character,
    ot_isolation_collection,
    ot_keyframe_character,
)

def register():
    addon_prefs.register()
    properties.register()
    gui.register()
    character_selection.register()
    ot_refresh_character_list.register()
    ot_toggle_scene.register()
    ot_isolate_character.register()
    ot_isolation_collection.register()
    ot_keyframe_character.register()

def unregister():
    addon_prefs.unregister()
    properties.unregister()
    gui.unregister()
    character_selection.unregister()
    ot_refresh_character_list.unregister()
    ot_toggle_scene.unregister()
    ot_isolate_character.unregister()
    ot_isolation_collection.unregister()
    ot_keyframe_character.unregister()
