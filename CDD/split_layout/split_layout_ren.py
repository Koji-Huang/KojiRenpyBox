'''

Copyright 2025.4.23 Koji-Huang(1447396418@qq.com)

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
from renpy.display.render import render
import pygame


class SplitLayout(renpy.display.layout.Container):
    def __init__(self, 
            horizontal_nor_vertical=True, 
            default_percent=0.5, 
            divider_idle=(144, 144, 144), 
            divider_hover=(100, 160, 210), 
            divider_select=(90, 180, 255),
            max_percent = 0.9,
            min_percent = 0.1,
            divider_width = 3,
            divider_border = 10,
            render_limit = True,
            event_limit = True,
            divider_draggable = True,
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)
        self.default_percent = default_percent
        self.divider_idle = divider_idle
        self.divider_hover = divider_hover
        self.divider_select = divider_select
        self.divider_width = divider_width
        self.divider_border = divider_border
        self.render_limit = render_limit
        self.event_limit = event_limit
        self.divider_draggable = divider_draggable
        self.min_percent = min_percent
        self.max_percent = max_percent
        self.direction = (horizontal_nor_vertical, not horizontal_nor_vertical)

        self.draggable = True
        
        self.divider_state = 0
        self.divider_pos = None
        self.render_size = (0, 0)

    def render(self, width, height, st, at):
        rv = renpy.Render(width, height)
        
        default_percent = tuple(i * self.default_percent for i in self.direction)

        self.offsets = self._list_type()
        self.render_size = (width, height)

        a_render_size = width * (default_percent[0] if self.direction[0] else 1.0), height * (default_percent[1] if self.direction[1] else 1.0)
        b_render_size = width * ((1 - default_percent[0]) if self.direction[0] else 1.0), height * ((1 - default_percent[1]) if self.direction[1] else 1.0)

        if len(self.children) >= 1:
            render_a = render(self.children[0], *a_render_size, st, at)

            # rv.blit(render_a, (0, 0))

            if self.render_limit:
                offset = self.children[0].place(rv, 0, 0, *a_render_size, render_a)
            else:
                offset = self.children[0].place(rv, 0, 0, width, height, render_a)
                
            self.offsets.append(offset)
            

        if len(self.children) >= 2:
            render_b = render(self.children[1], *b_render_size, st, at)
            b_pos = a_render_size[0] if self.direction[0] else 0.0, a_render_size[1] if self.direction[1] else 0.0

            # rv.blit(render_b, b_pos)

            if self.render_limit:
                offset = self.children[1].place(rv, *b_pos, *b_render_size, render_b)
            else:
                offset = self.children[1].place(rv, *b_pos, width, height, render_b)
                
            self.offsets.append(offset)

        self.divider_pos = (width * default_percent[0], height * default_percent[1])
        divider_end_pos = (width * default_percent[0] if self.direction[0] else width, height * default_percent[1] if self.direction[1] else height)
        
        color = self.divider_select if self.divider_state == 2 else self.divider_hover if self.divider_state == 1 else self.divider_idle

        rv.canvas().line(color = color, start_pos=self.divider_pos, end_pos=divider_end_pos, width=self.divider_width)

        return rv

    def event(self, ev, x, y, st):
        if self.divider_draggable:
            if ev.type == pygame.MOUSEMOTION and self.divider_pos is not None:
                if self.divider_state == 2:
                    self.default_percent = x / self.render_size[0] if self.direction[0] else y / self.render_size[1]
                    if self.default_percent < self.min_percent: self.default_percent = self.min_percent
                    if self.default_percent > self.max_percent: self.default_percent = self.max_percent
                    renpy.redraw(self, 0)
                    raise renpy.display.core.IgnoreEvent()
                else:

                    divider_hover_range = (
                        (-self.divider_border, +self.divider_border) if self.direction[0] > 0 else (0, 0+self.render_size[0]),
                        (-self.divider_border, +self.divider_border) if self.direction[1] > 0 else (0, 0+self.render_size[1]))
                    old_state = self.divider_state

                    self.divider_state = (divider_hover_range[0][0] < x - self.divider_pos[0] < divider_hover_range[0][1] and divider_hover_range[1][0] < y - self.divider_pos[1] < divider_hover_range[1][1] )
                    
                    if old_state != self.divider_state:
                        renpy.redraw(self, 0)

            if ev.type == pygame.MOUSEBUTTONDOWN and self.divider_state == 1 and ev.button == 1:
                self.divider_state = 2
                renpy.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()
            
            if ev.type == pygame.MOUSEBUTTONUP and self.divider_state == 2 and ev.button == 1:
                self.divider_state = 1
                renpy.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

        b_pos = (self.render_size[0] * self.default_percent if self.direction[0] else 0.0, self.render_size[1] * self.default_percent if self.direction[1] else 0.0)

        if (x > b_pos[0] and self.direction[0]) or (y > b_pos[1] and self.direction[1]):
            if len(self.children) >= 2:
                # print("B", self.children[1], st)
                self.children[1].event(ev, x - b_pos[0], y - b_pos[1], st)
            if len(self.children) >= 1 and self.event_limit is False:
                # print("A", self.children[0], st)
                self.children[0].event(ev, x, y, st)
        else:
            if len(self.children) >= 1:
                # print("A", self.children[0], st)
                self.children[0].event(ev, x, y, st)
            if len(self.children) >= 2 and self.event_limit is False:
                # print("B", self.children[1], st)
                self.children[1].event(ev, x - b_pos[0], y - b_pos[1], st)

    def add(self, child):
        if child is None or child in self.children:
            return
        
        if len(self.children) < 2:
            self.children.append(renpy.displayable(child))
        else:
            if child != self.children[0] and child != self.children[1]:
                raise Exception("Children is Out of Range\nNow Child: " + str(self.children[0]) + " - ", str(self.children[1]), "\nAdd in child:", str(child))


renpy.register_sl_displayable("split", SplitLayout, "", 2

    ).add_property("divider_width"  # 条渲染的宽度
    ).add_property("divider_border"  # 条判定的宽度
    ).add_property("divider_draggable"  # 条是否可拖动

    ).add_property("divider_idle"  # 条的 idle 颜色
    ).add_property("divider_hover"  # 条的 hover 颜色
    ).add_property("divider_select"  # 条的 select 颜色

    ).add_property("max_percent"  # 最大的百分度
    ).add_property("min_percent"  # 最小的百分度
    ).add_property("default_percent"  # 默认的百分度

    ).add_property("render_limit"  # 是否按照分割后的大小渲染子组件 (不然就以 SplitLayout 的大小进行渲染)
    ).add_property("event_limit"  # 是否只把 event 传入一个子组件 (不然同一个 event 能被两个子组件接收)
    ).add_property("horizontal_nor_vertical"  # 纵或横向布局
    )

