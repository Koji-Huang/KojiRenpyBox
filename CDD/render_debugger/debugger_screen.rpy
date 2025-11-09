'''

Copyright 2025.11.9 Koji-Huang(koji233@163.com)

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


default DebuggerConfig = {
    "text_size": 15,
    "spacing_x": 40,
    "spacing_y": 5,
    "target_screen": "screens",
    "target_index": 0,
    "displaying_head_index": 0,
    "preview_background_scale": 1.0,
    "step_line": 1,
    "top_preiview": True,
    "top_tip": True,
    "wake": "K_BACKQUOTE",
    "wake_pygame": pygame.K_BACKQUOTE,
    "quit": "K_ESCAPE",
    "quit_pygame": pygame.K_ESCAPE,
    "background_color": [1.0, 1.0, 1.0, 0.5, 0.5],
    "text_color": [0, 1.0, 1.0, 1.0, 1.0],
    "text_background_color": [0.0, 0.0, 0.0, 0.5, 0.5],
    "mark_color_1": [0.0, 0.0, 0.0, 1.0, 1.0],
    "mark_color_2": [0.0, 0.0, 0.0, 1.0, 1.0],
    "mark_background_color_1": [0.0, 0.0, 0.0, 0.5, 0.5],
    "mark_background_color_2": [0.0, 0.0, 0.0, 0.5, 0.5],
    "mark_notice": [0.0, 1.0, 1.0, 1.0, 1.0],
    "menu_background_color": [0.0, 1.0, 1.0, 0.2, 0.7],
}


python early:
    DebuggerColor = dict()
    DebuggerThemePack = dict()
    DebuggerColorInited = False

    def get_setted_col(name, r=None, g=None, b=None, a=None, blend=None):
        return [get if replace is None else replace for get, replace in zip(DebuggerColor[name], (r, g, b, a, blend))]

    def load_color_pack(data):
        DebuggerColor.update(data['Color'])

        for name, color in data['Theme'].items():
            theme = dict()

            for key, match in color.items():
                if isinstance(match, str):
                    get_color = get_setted_col(match)
                elif isinstance(match, Mapping):
                    get_color = get_setted_col(**match)
                elif isinstance(match, Iterable):
                    get_color = list(match)
                else:
                    get_color = get_setted_col("Clear")
                theme[key] = get_color

            DebuggerThemePack[name] = theme

    def init_debugger_color(debugger_config):
        import json
        import os

        debugger_color_json_path = None

        for root, dirname, files in os.walk(config.gamedir):
            if "debugger_color.json" in files:
                debugger_color_json_path = os.path.join(root, "debugger_color.json")
                print(debugger_color_json_path)
        else:
            if debugger_color_json_path is None:
                DebuggerColor.update(
                    {
                    "Dark":  [0.0, 0.0, 0.0, 1.0, 0.5],
                    "Light": [1.0, 1.0, 1.0, 1.0, 0.5],
                    "Clear": [0.0, 0.0, 0.0, 0.0, 0.0],
                    "Black": [0.0, 0.0, 0.0, 1.0, 1.0],
                    "White": [1.0, 1.0, 1.0, 1.0, 1.0],
                    "Cyan":  [0.0, 1.0, 1.0, 1.0, 1.0],
                    "Green": [0.0, 1.0, 0.0, 1.0, 1.0],
                    "Blue":  [0.2, 0.6, 0.9, 1.0, 1.0],
                    "Gray":  [0.5, 0.5, 0.5, 1.0, 1.0]
                    }
                )
            else:
                with open(debugger_color_json_path, "r", encoding="utf-8") as f:
                    color_json = json.load(f)
                load_color_pack(color_json)
                set_debugger_theme(debugger_config)

    def set_debugger_theme(debugger_config, name="Default"):
        if name not in DebuggerThemePack:
            raise Exception("Theme not Found")

        for key, color in DebuggerThemePack[name].items():
            debugger_config[key] = color[:]



init python:
    config.always_shown_screens.append("debugger_screen")

    def SetDebuggerConfig(key, value):
        return SetDict(DebuggerConfig, key, value)


screen hbox_color_set(set_name, target_key):
    hbox:
        xpos 50
        for i in set_name:
            textbutton i action SetDict(DebuggerConfig, target_key, get_setted_col(i))


screen vbox_color_adjust(target_key, disable_blend=False):
    vbox:
        xpos 50
        hbox:
            text "R "
            bar value DictValue(DebuggerConfig[target_key], 0, 1.0)
            text "%d" % (DebuggerConfig[target_key][0]*255)
        hbox:
            text "G "
            bar value DictValue(DebuggerConfig[target_key], 1, 1.0)
            text "%d" % (DebuggerConfig[target_key][1]*255)
        hbox:
            text "B "
            bar value DictValue(DebuggerConfig[target_key], 2, 1.0)
            text "%d" % (DebuggerConfig[target_key][2]*255)
        hbox:
            text "Alpha "
            bar value DictValue(DebuggerConfig[target_key], 3, 1.0)
            text "%.1f%%" % (DebuggerConfig[target_key][3]*100)
        if disable_blend == False:
            hbox:
                text "Blend "
                bar value DictValue(DebuggerConfig[target_key], 4, 1.0)
                text "%.1f%%" % (DebuggerConfig[target_key][4]*100)


screen debugger_menu:
    default Page = "Screen"

    fixed:
        xsize 800
        xalign 1.0

        # add DisableEvent() xsize 800 xalign 1.0
        add Solid(float_color_hex(DebuggerConfig["menu_background_color"]))
   
        hbox:
            textbutton "{size=50}Screen" action SetScreenVariable("Page", "Screen")
            textbutton "{size=50}Debugger" action SetScreenVariable("Page", "Debugger")
            textbutton "{size=50}Color" action SetScreenVariable("Page", "Color")

        viewport:
            mousewheel True
            ysize config.screen_height - 100
            yalign 1.0
            xpos 25

            vbox:
                xsize 600

                if Page == "Screen":
                    text "Layer"
                    vbox:
                        xpos 50
                        for i in renpy.display.scenelists.scene_lists().layers.keys():
                            textbutton str(i): 
                                action [SetDict(DebuggerConfig, "target_screen", i), Function(set_layer_index)]
                                sensitive renpy.display.scenelists.scene_lists().layers[i].__len__()

                    add Null(height=30)

                    text f"SLE"
                    vbox:
                        xpos 50
                        for i, o in enumerate(renpy.display.scenelists.scene_lists().layers[DebuggerConfig['target_screen']]):
                            textbutton str(o.tag) action [Function(set_layer_index, i), SetDict(DebuggerConfig, "target_index", i)]

                if Page == "Debugger":

                    add Null(height=20)
                    text f"Show Preview on Top"
                    hbox:
                        xpos 50
                        textbutton "True" action SetDebuggerConfig("top_preiview", True)
                        textbutton "False" action SetDebuggerConfig("top_preiview", False)

                    add Null(height=20)
                    text f"Show Selected Tip on Top"
                    hbox:
                        xpos 50
                        textbutton "True" action SetDebuggerConfig("top_tip", True)
                        textbutton "False" action SetDebuggerConfig("top_tip", False)

                    add Null(height=20)
                    text f"Mouse Scroll Line"
                    hbox:
                        xpos 50
                        bar value DictValue(DebuggerConfig, "step_line", range=80)
                        text f"{DebuggerConfig['step_line']}"


                    add Null(height=30)
                    text f"Debugger Text Size"
                    hbox:
                        xpos 50
                        bar value DictValue(DebuggerConfig, "text_size", range=60)
                        text f"{DebuggerConfig['text_size']}"

                    add Null(height=20)

                    text f"Indent Width"
                    hbox:
                        xpos 50
                        bar value DictValue(DebuggerConfig, "spacing_x", range=80)
                        text f"{DebuggerConfig['spacing_x']}"
                        

                    add Null(height=20)

                    text f"Line Spacing"
                    hbox:
                        xpos 50
                        bar value DictValue(DebuggerConfig, "spacing_y", range=80)
                        text f"{DebuggerConfig['spacing_y']}"

                if Page == "Color":
                    text "{size=50}Theme"
                    vbox:
                        xpos 50
                        for name in DebuggerThemePack:
                            textbutton name action Function(set_debugger_theme, DebuggerConfig, name)

                    add Null(height=20)

                    text "{size=50}Color Set"
                    vbox:
                        xpos 50
                        text "Debugger Background Color"
                        use hbox_color_set(("Dark", "Light", "Clear", "Black"), "background_color")

                        text "Debugger Text Color"
                        use hbox_color_set(("Cyan", "White", "Green", "Blue"), "text_color")

                        text "Debugger Text Background Color"
                        use hbox_color_set(("Dark", "Light", "Cyan", "Clear"), "text_background_color")

                        text "Mark Object Color Set"
                        add DynamicDisplayable(preview_debugger_background) xpos 50
                        hbox:
                            xpos 50
                            text "Blend: "
                            textbutton "Dark"  action [SetDebuggerConfig("mark_color_1", get_setted_col("Black", blend=0.0)), SetDebuggerConfig("mark_color_2", get_setted_col("Gray",  blend=0.0))] selected False
                            textbutton "Light" action [SetDebuggerConfig("mark_color_1", get_setted_col("White", blend=0.0)), SetDebuggerConfig("mark_color_2", get_setted_col("Gray",  blend=0.0))] selected False
                            textbutton "White" action [SetDebuggerConfig("mark_color_1", get_setted_col("White", blend=0.0)), SetDebuggerConfig("mark_color_2", get_setted_col("White", blend=0.0))] selected False
                            textbutton "Clear" action [SetDebuggerConfig("mark_color_1", get_setted_col("Black", a=0.0, blend=0.0)), SetDebuggerConfig("mark_color_2",  get_setted_col("Black", a=0.0, blend=0.0))] selected False

                        hbox:
                            xpos 50
                            text "Trans: "
                            textbutton "Dark"  action [SetDebuggerConfig("mark_color_1", get_setted_col("Dark")), SetDebuggerConfig("mark_color_2", get_setted_col("Gray", a=0.5, blend=0.5))] selected False
                            textbutton "Light" action [SetDebuggerConfig("mark_color_1", get_setted_col("Light")), SetDebuggerConfig("mark_color_2", get_setted_col("Gray", a=0.5, blend=0.5))] selected False
                            textbutton "Black" action [SetDebuggerConfig("mark_color_1", get_setted_col("Dark")), SetDebuggerConfig("mark_color_2", get_setted_col("Dark"))] selected False
                            textbutton "White" action [SetDebuggerConfig("mark_color_1", get_setted_col("Light")), SetDebuggerConfig("mark_color_2", get_setted_col("Light"))] selected False

                        hbox:
                            xpos 50
                            text "Solid: "
                            textbutton "Dark"  action [SetDebuggerConfig("mark_color_1", get_setted_col("Black", blend=1.0)), SetDebuggerConfig("mark_color_2", get_setted_col("Gray",  blend=1.0))] selected False
                            textbutton "Light" action [SetDebuggerConfig("mark_color_1", get_setted_col("White", blend=1.0)), SetDebuggerConfig("mark_color_2", get_setted_col("Gray",  blend=1.0))] selected False
                            textbutton "Black" action [SetDebuggerConfig("mark_color_1", get_setted_col("Black", blend=1.0)), SetDebuggerConfig("mark_color_2", get_setted_col("Black", blend=1.0))] selected False
                            textbutton "White" action [SetDebuggerConfig("mark_color_1", get_setted_col("White", blend=1.0)), SetDebuggerConfig("mark_color_2", get_setted_col("White", blend=1.0))] selected False



                    add Null(height=20)

                    text "{size=50}Detail"

                    add Null(height=20)

                    text "Debugger"

                    add Null(height=20)

                    vbox:
                        xpos 30
                        text "Debugger Background Color"
                        use vbox_color_adjust("background_color")

                        add Null(height=20)
                        text "Debugger Text Color"
                        use vbox_color_adjust("text_color")

                        add Null(height=20)
                        text "Debugger Text Background Color"
                        use vbox_color_adjust("text_background_color")
                            
                    add Null(height=20)
                    add Null(height=20)

                    text "Mark"

                    add Null(height=20)

                    vbox:
                        xpos 30

                        add Null(height=20)
                        text "Mark Notice Color"
                        add DynamicDisplayable(preview_debugger_notice) xpos 50
                        use vbox_color_adjust("mark_notice")

                        add Null(height=20)
                        add DynamicDisplayable(preview_debugger_background) xpos 50

                        add Null(height=20)
                        text "Mark Object Color #1"
                        use vbox_color_adjust("mark_color_1")
                            
                        add Null(height=20)
                        text "Mark Object Color #2"
                        use vbox_color_adjust("mark_color_2")

                        add Null(height=20)
                        text "Mark Background Color #1"
                        use vbox_color_adjust("mark_background_color_1")
                            
                        add Null(height=20)
                        text "Mark Background Color #2"
                        use vbox_color_adjust("mark_background_color_2")

                    add Null(height=20)

                    text "Menu"

                    vbox:
                        add Null(height=20)
                        text "Menu Background Color"
                        use vbox_color_adjust("menu_background_color")


screen debugger_screen:
    default Enable = False
    default OpenDebuggerMenu = False

    timer 1.0 repeat True action Function(print, "Still Displayaing", _update_screens=False)

    if Enable:
        if DebuggerColorInited is False:
            $ init_debugger_color(DebuggerConfig)
            $ DebuggerColorInited = True
        key DebuggerConfig["wake"] action [SetScreenVariable("OpenDebuggerMenu", not OpenDebuggerMenu)]
        key DebuggerConfig["quit"] action [SetScreenVariable("Enable", False)]

    else:
        key DebuggerConfig["wake"] action [SetScreenVariable("Enable", True)]
    
    layer "top"

    if Enable:
        add DisableEvent()

        add Solid(float_color_hex(DebuggerConfig["background_color"]))

        text "{size=20}%s to Open Menu\n%s to Quit\n{size=15}{b}DisplayableDebugger{/b} by Koji" % (DebuggerConfig["wake"], DebuggerConfig["quit"]) yalign 1.0

        add RenderTreePreview() as debugger
        
        if OpenDebuggerMenu:
            add DisableEvent()
            imagebutton: 
                idle Solid(float_color_hex(DebuggerConfig["background_color"]))
                action [SetScreenVariable("OpenDebuggerMenu", False), Function(print, "Hideeeee")]
                xysize (1920, 1080)
            use debugger_menu
