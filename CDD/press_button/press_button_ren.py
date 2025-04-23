'''

Copyright 2024.10.30 Koji-Huang(1447396418@qq.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''


"""renpy

python early:
"""


import pygame


class PressImageButton(renpy.display.behavior.ImageButton):
    def __init__(self, 
                idle = None,
                hover = None,
                insensitive = None,
                activate = None,
                press = None, 
                idle_image = None,
                hover_image = None,
                insensitive_image = None,   
                activate_image = None,
                press_image = None, 
                selected_idle = None,
                selected_hover = None,
                selected_insensitive = None,
                selected_activate = None,
                selected_press = None,
                selected_idle_image = None,
                selected_hover_image = None,
                selected_insensitive_image = None,
                selected_activate_image = None,
                selected_press_image = None, 
                press_sound = None,
                press_sound_channel = 'audio',
                auto = None,
                *args, **kwargs):


        # COPY from "renpy/ui.py" -> "def _imagebutton" -> "def __init__"
        def choice(a, b, name, required=False, auto = None):
            if a:
                return a

            if b:
                return b

            if auto is not None:
                rv = renpy.config.imagemap_auto_function(auto, name)
                if rv is not None:
                    return rv

            if required:
                if auto:
                    raise Exception("Imagebutton does not have a %s image. (auto=%r)." % (name, auto))
                else:
                    raise Exception("Imagebutton does not have a %s image." % (name,))

            return None
        

        idle = choice(idle, idle_image, "idle", required=True, auto=auto)
        hover = choice(hover, hover_image, "hover", auto=auto)
        insensitive = choice(insensitive, insensitive_image, "insensitive", auto=auto)
        selected_idle = choice(selected_idle, selected_idle_image, "selected_idle", auto=auto)
        selected_hover = choice(selected_hover, selected_hover_image, "selected_hover", auto=auto)
        selected_insensitive = choice(selected_insensitive, selected_insensitive_image, "selected_insensitive", auto=auto)

        super(PressImageButton, self).__init__(idle, hover, insensitive, selected_idle, selected_hover, selected_insensitive, *args, **kwargs)

        press_image = press_image if press_image is not None else press
        selected_press_image = selected_press_image if press_image is not None else selected_press

        self.background_state = 0  # 0: idle  1: hover  2: select

        self.state_children['press_'] = renpy.easy.displayable(press_image) if press_image is not None else self.state_children['idle_']
        self.state_children['selected_press_'] = renpy.easy.displayable(selected_press_image) if selected_press_image is not None else self.state_children['selected_idle_']

        self.press_sound = press_sound
        self.press_sound_channel = press_sound_channel


    def event(self, ev, x, y, st):
        is_in_range = int(self.is_hovered(x, y))
        background_state_last = self.background_state

        if self.background_state - is_in_range and self.background_state != 2:
            self.background_state = is_in_range
            renpy.redraw(self, 0)

        elif ev.type == pygame.MOUSEBUTTONDOWN and is_in_range:
            print(ev.__dict__)
            
            if self.press_sound is not None:
                renpy.music.play(self.press_sound, channel=self.press_sound_channel)

            self.background_state = 2
            renpy.redraw(self, 0)

        elif ev.type == pygame.MOUSEBUTTONUP and self.background_state == 2:
            self.background_state = is_in_range
            renpy.redraw(self, 0)

        return super(PressImageButton, self).event(ev, x, y, st)


    # def render(self, w, h, st, at):
    #     renpy.redraw(self, 0)
    #     print(st, at)
    #     return super().render(w, h, st, at)


    def get_child(self):
        # COPY from "renpy/display/behavior.py" -> "class ImageButton" -> "def get_child" to fix

        raw_child = self.style.child or self.state_children[self.style.prefix]

        # it's strange that renpy.is_sensitive(None) will return True...
        if self.action is not None and renpy.is_sensitive(self.action):
            if self.background_state == 2:
                raw_child = self.state_children['selected_press_' if self.is_selected() else "press_"] 

        if raw_child is not self.imagebutton_raw_child:
            self.imagebutton_raw_child = raw_child

            if raw_child._duplicatable:
                self.imagebutton_child = raw_child._duplicate(None)
                self.imagebutton_child._unique()
            else:
                self.imagebutton_child = raw_child

            self.imagebutton_child.per_interact()

        return self.imagebutton_child

    @property
    def displaying_size(self):
        """
        Because the child weight's size is not a const. so I have to use such a ugly way to get the size of child weight.
        Actually, I think window_size can also be used, but not every weight is the son class of window, it doesn't work perfectly. So I give up the try. 
        If child widget's size have been changed, it can't update it. If you found the code didn't work as predict, just try another way to get child's size.
        """
        child = self.get_child()
        if 'displaying_size' not in child.__dir__():
            child.displaying_size = child.render(1920, 1080, 0, 0).get_size()
        return child.displaying_size

    def is_hovered(self, x, y):
        return 0 < x < self.displaying_size[0] and 0 < y < self.displaying_size[1]


renpy.register_sl_displayable("pressbutton", PressImageButton, "", 1
    ).add_property("press"
    ).add_property("hover"
    ).add_property("idle"
    ).add_property("insensitive"
    ).add_property("activate"
    ).add_property("press_image"
    ).add_property("hover_image"
    ).add_property("idle_image"
    ).add_property("insensitive_image"
    ).add_property("activate_image"
    ).add_property("selected_idle"
    ).add_property("selected_hover"
    ).add_property("selected_insensitive"
    ).add_property("selected_activate"
    ).add_property("selected_press"
    ).add_property("selected_idle_image"
    ).add_property("selected_hover_image"
    ).add_property("selected_insensitive_image"
    ).add_property("selected_activate_image"
    ).add_property("selected_press_image"
    ).add_property("style"
    ).add_property("clicked"
    ).add_property("hovered"
    ).add_property("press_sound_channel"
    ).add_property("press_sound"
    ).add_property_group("button")
