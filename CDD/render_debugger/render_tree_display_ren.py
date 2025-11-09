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

"""renpy

python early:
"""

import pygame

DebuggerHideObject = list()


renpy.register_shader("debugger_frame",
    variables="""
    uniform vec4 u_col;
    """,
    fragment_300="""
    gl_FragColor = mix(u_col, vec4(gl_FragColor.rgb, u_col.a), gl_FragColor.a);
    """)

renpy.register_shader("debugger_reverse",
    variables="""
    uniform vec4 u_col;
    """,
    fragment_300="""
    // vec4 reverse = vec4(1.0 - u_col.g * 0.5 + u_col.b, 1.0 - u_col.r * 0.5 + u_col.b, 1.0 - u_col.g * 0.5 + u_col.r, 1.0);
    vec4 reverse = vec4(1.0 - u_col.r, 1.0 - u_col.g, 1.0 - u_col.b, 1.0);
    gl_FragColor = mix(u_col, reverse, gl_FragColor.a);

    """)

renpy.register_shader("debugger_background",
    variables="""
    uniform vec2 u_virtual_size;
    uniform vec2 u_model_size;
    uniform vec4 u_col_1;
    uniform vec4 u_col_2;
    uniform float u_scale;
    varying vec2 v_position;
    """,
    vertex_300 = """
    v_position = u_virtual_size * vec2(gl_Position.x * .5 + .5, -gl_Position.y * .5 + .5);
""",
    fragment_300="""
    bool can = step(fract(v_position.x/u_model_size.x*u_scale), 0.5) == step(fract(v_position.y/u_model_size.y*u_scale), 0.5);
    if(can) gl_FragColor = u_col_1;
    else gl_FragColor = u_col_2;
    """)


def clean_text_tag(text):
    return text.replace("{", "{{")


def render_tree_extract(render, dis=None, depth=0, offset=(0, 0)):
    tree = dict()

    if dis is None:
        dis = dict()
    
    for i in render.children:

        if isinstance(i[0], renpy.gl2.gl2model.GL2Model):
            continue
        if bool(i[0].render_of) is False:
            continue

        if ('children' in i[0].__dir__() and bool(i[0].children)):
            get_child = render_tree_extract(i[0], dis, depth+1, (i[1]+offset[0], i[2]+offset[1]))[0]
            tree[i[0]] = get_child if len(get_child) else None
        else:
            tree[i[0]] = None

        dis[i[0]] = ((i[1]+offset[0], i[2]+offset[1], *i[0].get_size()), i[0].render_of, depth)
        
    return tree, dis


def sort_render_tree(tree, dis, ret=None):
    if ret is None:
        ret = dict()
    for i in tree.keys():
        ret[i] = dis[i]
        if tree[i]:
            sort_render_tree(tree[i], dis, ret)
    return ret


def apply_blend(col):
    return (
        col[0] * col[3],
        col[1] * col[3],
        col[2] * col[3],
        col[4],
    )


def float_color_hex(col):
    blended = apply_blend(col)
    nornaml = tuple(int(i*255) for i in blended)
    return Color(nornaml).hexcode


def set_layer_index(index=0):
    DebuggerConfig["target_index"] = index
    DebuggerConfig["displaying_head_index"] = 0
    renpy.restart_interaction()


def preview_debugger_background(st, at):
    return Transform(
        Solid("#fff", xysize=(600, 50)),
        shader="debugger_background",
        u_col_1=apply_blend(DebuggerConfig['mark_color_1']),
        u_col_2=apply_blend(DebuggerConfig['mark_color_2']),
        u_scale=1.0,
    ), 0.1


def preview_debugger_notice(st, at):
    return Transform(
        Text("Hello World"),
        shader="debugger_reverse",
        u_col=apply_blend(DebuggerConfig["mark_notice"])
    ), 0.1


def displayable_is_hiden(obj):
    for i in range(len(DebuggerHideObject)):
        if obj == DebuggerHideObject[i]:
            return i
    return False


class RenderTreePreview(renpy.Displayable):
    def __init__(self):
        super().__init__()

        # To Render Text
        self.text = Text('', size=DebuggerConfig["text_size"], color=DebuggerConfig["text_color"])
        self.mark_text = Text('', size=DebuggerConfig["text_size"])

        self.head_index = DebuggerConfig['displaying_head_index']
        self.is_rendering = False

        self.hovering_index = None
        self.hovering_cover = None

        self.displaying_obj = []  # x, y, w, h, displayable, index
        self.hide_index = []

    def get_target_displayable(self):
        if len(renpy.display.scenelists.scene_lists().layers[DebuggerConfig["target_screen"]]) <= DebuggerConfig["target_index"]:
            DebuggerConfig["target_index"] = 0
            DebuggerConfig["target_screen"] = 'screens'
            
        return renpy.display.scenelists.scene_lists().layers[DebuggerConfig["target_screen"]][int(DebuggerConfig["target_index"])].displayable
    
    def event(self, ev, x, y, st):
        if ev.type == pygame.MOUSEBUTTONUP:
            # Hide Displayable
            if ev.button == 3 and self.hovering_cover is not None:
                displayable = tuple(self.displaying_obj[self.hovering_cover][4])
                index = displayable_is_hiden(displayable)
                if index is False:
                    DebuggerHideObject.append(displayable)
                else:
                    DebuggerHideObject.pop(index)
                renpy.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            # Roll Up
            if ev.button == 4:
                fold = self.reverse_fold_hide_index()
                head = self.head_index-DebuggerConfig['step_line'] if self.head_index-DebuggerConfig['step_line'] > 0 else 0
                end = self.head_index
                last_sum = 0
                while True:
                    cound = sum(fold[head:end])
                    if cound != last_sum:
                        head -= cound - last_sum
                        last_sum = cound
                    else:
                        break

                self.head_index = head
                renpy.redraw(self, 0)
            
            # Roll Down
            if ev.button == 5:
                fold = self.fold_hide_index()
                head = self.head_index
                end = self.head_index+DebuggerConfig['step_line'] if self.head_index+DebuggerConfig['step_line'] < len(fold) else len(fold)
                last_sum = 0
                while True:
                    cound = sum(fold[head:end])
                    if cound != last_sum:
                        end += cound - last_sum
                        last_sum = cound
                    else:
                        break

                self.head_index = end
                renpy.redraw(self, 0)
    
        if ev.type == pygame.KEYUP and ev.key == pygame.K_PAGEUP:
            self.head_index -= len(self.displaying_obj)
            renpy.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()
    
        if ev.type == pygame.KEYUP and ev.key == pygame.K_PAGEDOWN:
            self.head_index += len(self.displaying_obj)
            renpy.redraw(self, 0)

        if ev.type == pygame.MOUSEMOTION:
            select = None
            for i, area in enumerate(self.displaying_obj):
                if 0 < y-area[1] < area[3] and 0 < x-area[0] < area[2]:
                    select = area[5]
                    self.hovering_cover = i
                    break

            if self.hovering_index != select:
                renpy.redraw(self, 0)

            self.hovering_index = select

    def render(self, width, height, st, at):
        rv = renpy.Render(width, height)

        if self.is_rendering == True:
            return rv


        self.is_rendering = True
        self.text = Text('', size=DebuggerConfig["text_size"], color=float_color_hex(DebuggerConfig["text_color"]), bold=True)
        self.displaying_obj = []
        self.hide_index = []
        
        # Extract Render Tree
        tree, dis = render_tree_extract(
            renpy.display.render.render_screen(
                self.get_target_displayable(), 
                config.screen_width, 
                config.screen_height)
                )
        index = sort_render_tree(tree, dis)  # { render: ((x, y, w, h), displayable, depth) }
        if self.head_index >= len(index):
            self.head_index = len(index) - 1 - ( self.hide_index[-1] if self.hide_index else 0 )
        if self.head_index < 0:
            self.head_index = 0
        DebuggerConfig['displaying_head_index'] = self.head_index

        spacing = (DebuggerConfig['spacing_x'], DebuggerConfig['spacing_y'])
        previewing_render = None
        previewing_tip = None
        yoffset = 0
        hide_limit = None
        hiden_obj = 0


        for i, key in enumerate(index.keys()):

            if yoffset > height:
                break

            render_of = tuple(key.render_of)

            if hide_limit:
                if index[key][2] <= hide_limit:
                    self.hide_index.append(hiden_obj)
                    hide_limit = None
                else:
                    hiden_obj += 1
                    continue
            else:
                self.hide_index.append(0)

            if displayable_is_hiden(render_of):
                hide_limit = index[key][2]
                hiden_obj = 0

            if i < self.head_index:
                continue
        
            tip = self.render_tip(index[key], width - index[key][2]*spacing[0], height, st, at)

            if i == self.hovering_index:
                previewing_tip = (tip, (index[key][2]*spacing[0], yoffset))

                # Marked Render's Background
                marked_bg = renpy.displayable("#fff").render(*key.get_size(), st, at)
                marked_bg.add_shader("debugger_background")
                marked_bg.add_uniform("u_col_1", apply_blend(DebuggerConfig["mark_color_1"]))
                marked_bg.add_uniform("u_col_2", apply_blend(DebuggerConfig["mark_color_2"]))
                marked_bg.add_uniform("u_scale", DebuggerConfig["preview_background_scale"])

                # When Previewing Render
                # Draw a Background on Full Screen
                previewing_bg = renpy.displayable("#fff").render(width, height, st, at)
                previewing_bg.add_shader("debugger_background")
                previewing_bg.add_uniform("u_col_1", apply_blend(DebuggerConfig["mark_background_color_1"]))
                previewing_bg.add_uniform("u_col_2", apply_blend(DebuggerConfig["mark_background_color_2"]))
                previewing_bg.add_uniform("u_scale", DebuggerConfig["preview_background_scale"])
                
                # Marked Render's Tip
                marked_tip = self.render_marked_tip(index[key], width - index[key][2] * spacing[0], height, st, at)
                marked_tip.add_shader("debugger_reverse")
                marked_tip.add_uniform("u_col", apply_blend(DebuggerConfig["mark_notice"]))

                # Align to Render's Left Top
                marked_tip_x = index[key][0][0] if index[key][0][0] + marked_tip.get_size()[0] < width else width - marked_tip.get_size()[0]
                if marked_tip_x < 0: marked_tip_x = 0
                marked_tip_y = index[key][0][1] - marked_tip.get_size()[1]
                marked_tip_y = marked_tip_y if marked_tip_y < height else height - marked_tip.get_size()[1]
                if marked_tip_y <= 0:
                    if index[key][0][1] + index[key][0][3] + marked_tip.get_size()[1] < height:
                        marked_tip_y = index[key][0][1] + index[key][0][3]
                    else:
                        marked_tip_y = 0

                previewing_render = renpy.Render(*key.get_size())
                previewing_render.blit(marked_bg, (index[key][0][0], index[key][0][1]))
                previewing_render.blit(key, (index[key][0][0], index[key][0][1]))
                previewing_render.blit(marked_tip, (marked_tip_x, marked_tip_y if marked_tip_y > 0 else 0))

                # Double Render tip to Focus
                rv.blit(tip, (index[key][2]*spacing[0], yoffset-1))

            else:
                tip.add_shader("debugger_frame")
                tip.add_uniform("u_col", apply_blend(DebuggerConfig['text_background_color']))

            rv.blit(tip, (index[key][2]*spacing[0], yoffset))
            self.displaying_obj.append((index[key][2]*spacing[0], yoffset, tip.get_size()[0], tip.get_size()[1] + spacing[1]+5, key.render_of, i))

            if self.hide_index[-1]:
                hide_info = self.render_hide(self.hide_index[-1], width, height, st, at)
                rv.blit(hide_info, (0, yoffset-hide_info.get_size()[1]-spacing[1]))

            yoffset += tip.get_size()[1] + DebuggerConfig["spacing_y"]


        if hide_limit:
            self.hide_index.append(hiden_obj)
        else:
            self.hide_index.append(0)
        if self.hide_index[-1]:
            hide_info = self.render_hide(self.hide_index[-1], width, height, st, at)
            rv.blit(hide_info, (0, yoffset-hide_info.get_size()[1]-spacing[1]))
        self.hide_index = self.hide_index[1:]

        if previewing_render is not None:
            if DebuggerConfig["top_preiview"]:
                rv.blit(previewing_bg, (0, 0))
                rv.blit(previewing_render, (0, 0))
            else:
                bg_rv = renpy.Render(width, height)
                bg_rv.blit(previewing_bg, (0, 0))
                bg_rv.blit(previewing_render, (0, 0))
                bg_rv.blit(rv, (0, 0))
                rv = bg_rv
        
        if DebuggerConfig["top_tip"] and previewing_tip is not None:
            rv.blit(*previewing_tip)

        self.is_rendering = False

        return rv

    def render_tip(self, info, w, h, st, at):
        self.text.set_text(clean_text_tag(f"{info[1]} - {info[0]}"))
        return self.text.render(w, h, st, at)
    
    def render_marked_tip(self, info, w, h, st, at):
        self.mark_text.set_text(clean_text_tag(f"pos:{info[0][:2]} size:{info[0][2:4]} - {info[1]}"))
        return self.mark_text.render(w, h, st, at)
    
    def render_hide(self, hide_num, w, h, st, at):
        self.text.set_text(clean_text_tag(f"[{hide_num}] ->"))
        return self.text.render(w, h, st, at)
    
    def fold_hide_index(self):
        fold = list()
        for i in self.hide_index:
            fold.append(i)
            for k in range(i):
                fold.append(0)
        return fold

    def reverse_fold_hide_index(self):
        fold = self.fold_hide_index()
        reverse = [0 for i in fold]
        for i, v in enumerate(fold):
            if v:
                reverse[i+v] += v
        return reverse


class DisableEvent(renpy.Displayable):
    def __init__(self):
        super().__init__()
        self.is_rendering = False
        self.focusable = True

    def event(self, ev, x, y, st):
        if ev.type in (pygame.KEYUP, pygame.KEYDOWN) and ev.key in (DebuggerConfig["quit_pygame"], DebuggerConfig['wake_pygame']):
            pass
        else:
            raise renpy.display.core.IgnoreEvent()
    
    def render(self, w, h, st, at):
        return renpy.Render(w, h)
    
    def focus(self):
        pass