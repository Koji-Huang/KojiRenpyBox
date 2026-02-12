'''

Copyright 2025.9.14 Koji-Huang(1447396418@qq.com)

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


from builtins import list as _list_type
from math import pi, sin, cos, atan2, sqrt
from typing import Iterable
import pygame


# 圆盘菜单默认回调函数 (以及注释)
default_callback = {
    # 渲染函数回调
    # 传参: self, rv, w, h, st, at
    "render": None,

    # 事件函数回调
    # 传参: self, ev, x, y, st
    "event": None,

    # 鼠标移动回调
    # 传参: self, ev, x, y, st, rad (鼠标所在弧度)
    "motion": None,

    # 用于判断当前事件是否激活了选项
    # 传参: self, ev, x, y, st
    "is_active": None,

    # 事件激活回调
    # 传参: 
    #     self: CircleMenu (菜单对象)
    #     obj: Displayable (选中项), 
    #     index: int (选中项下表), 
    "active": None,

    # 处理当前选择的子对象的下标
    # 传参: self: CircleMenu (菜单对象), st: int (时间轴)
    "solve_select": None,

    # 将 focus 应用到对象时的回调, 仅在 focus 改变时调用
    # 传参:
    #     self: CircleMenu (菜单对象)
    #     selected: Displayable ( 当前 focus )
    #     last: Displayable ( 上一个 focus )
    #     index: tuple[int, int] ( 当前/上一个 focus 的下标 )
    "apply_focus": None
}


# 圆盘菜单默认配置 (以及注释)
default_config = {
    "mouse_motion": True,    # 启用鼠标移动选择选项
    "mouse_wheel": True,     # 启用鼠标滚轮选择选项
    "keyboard": True,        # 启用键盘选择选项
    "mouse_active": True,    # 启用鼠标左键确认选项
    "keyboard_active": True, # 启用键盘按键确认选项
    "clean_focus": True,     # 清除掉原本按钮的 focus, 关掉的话键盘的上下左右可以按照标准 renpy 布局的方法来进行选择
    "limit_event": False,    # 限制事件只能在 mouse_check_r 的外半径内被处理
}


# 圆盘菜单默认选项切换键
default_key = {
    
    # 键盘下一个按钮的按键映射
    "next": (pygame.K_RIGHT, pygame.K_DOWN, pygame.K_d, pygame.K_s, pygame.K_KP_2, pygame.K_KP_6),
    
    # 键盘上一个按钮的按键映射
    "last": (pygame.K_LEFT, pygame.K_UP, pygame.K_a, pygame.K_w, pygame.K_4, pygame.K_8),
    
    # 激活选项的键盘按键
    "active": (pygame.K_KP_ENTER, pygame.K_SPACE)
}


def do_callback(key, dic, *args, **kwargs):
    callback = dic.get(key, None)
    if callback is None:
        return None
    if isinstance(callback, Iterable):
        ret = None
        for i in callback:
            tmp = i(*args, **kwargs)
            if tmp is not None:
                ret = tmp
        return ret
    else:
        return callback(*args, **kwargs)


# 圆盘布局
class CircleLayout(renpy.display.layout.Container):
    def __init__(self, offsets_angle = 0.0, r=200,*args, **kwargs):
        """
        :param offset_angle: 偏转角
        :param r: 选项所在的半径
        """
        super().__init__(*args, **kwargs)

        self.offsets_angle = offsets_angle
        self.r = r

    def render(self, w, h, st, at):
        rv = renpy.Render(w, h)
        
        self.offsets.clear()
        l = len(self.children) / pi / 2.0
        begin = -pi / 2.0 + self.offsets_angle

        for i, c in enumerate(self.children):
            cr = renpy.render(c, w, h, st, at)
            primer_offset = (cos(i / l + begin)*self.r, sin(i / l + begin)*self.r)
            size = cr.get_size()
            offset = (int(primer_offset[0]-size[0]*0.5), int(primer_offset[1]-size[1]*0.5))
            count_offset = c.place(rv, *offset, w, h, cr)
            self.offsets.append(count_offset)

        return rv


# 圆盘菜单
class CircleMenu(CircleLayout):
    def __init__(
            self, 
            offsets_angle: float = 0.0, 
            r: int = 230, 
            mouse_check_r: tuple[int, int] = (160, 300), 
            callbacks: dict={}, 
            config: dict={}, 
            key: dict={},
            *args, **kwargs):
        """
        :param mouse_check_r: 鼠标移动事件生效的半径
        :param callbacks: 回调函数的字典   
        :param config: 配置项的字典
        """
        super().__init__(offsets_angle, r, *args, **kwargs)

        self.mouse_check_r = mouse_check_r

        self.callbacks = default_callback.copy()
        self.callbacks.update(callbacks)

        self.config = default_config.copy()
        self.config.update(config)

        self.key = default_key.copy()
        self.key.update(key)


        # 当前选中的项的下标, 为 None 时则为不选中
        self.selected = None

        # 是否触发 [换到上一个/换到下一个]
        self.select_state = _list_type()
        self.select_state.append(False)
        self.select_state.append(False)

        # 上一次按键触发选项切换的时间
        self.select_state_st = None

    def render(self, w, h, st, at):
        rv = renpy.Render(self.r*2, self.r*2)
        
        self.offsets.clear()
        l = len(self.children) / pi / 2.0
        begin = -pi / 2.0 + self.offsets_angle

        for i, c in enumerate(self.children):
            cr = renpy.render(c, w, h, st, at)
            primer_offset = (cos(i / l + begin)*self.r, sin(i / l + begin)*self.r)
            size = cr.get_size()
            offset = (int(primer_offset[0]-size[0]*0.5)+self.r, int(primer_offset[1]-size[1]*0.5)+self.r)
            count_offset = c.place(rv, *offset, w, h, cr)
            self.offsets.append(count_offset)

            if self.config['clean_focus']:
                cr.focuses.clear()
        
        do_callback('render', self.callbacks, self, rv, w, h, st, at)

        return rv

    def event(self, ev, x, y, st):
        if self.config['limit_event'] is True and sqrt(pow(x-self.r, 2) + pow(y-self.r, 2)) > self.mouse_check_r[1]:
            last = self.selected
            self.selected = None
            self.apply_focus(self.selected)
            return

        last = self.selected
        last_state = self.select_state[:]

        self.mouse_focus(ev, x, y)
        self.keyboard_focus()

        self.solve_select(st, last_state)
        self.apply_focus(last)

        for i in range(len(self.children)):
            self.children[i].event(ev, x-self.offsets[i][0], y-self.offsets[i][1], st)
        
        do_callback('event', self.callbacks, self, ev, x, y, st)
        
        if self.is_active(ev, x, y, st):
            self.active()

    def mouse_focus(self, ev, x, y):
        if ev.type not in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
            return

        x -= self.r
        y -= self.r

        if ev.type == pygame.MOUSEMOTION and self.config['mouse_motion']: 
            if (self.mouse_check_r[0] < sqrt(x*x + y*y) < self.mouse_check_r[1]) is False:
                self.selected = None
                return
            n = len(self.children)
            rad_spacing = 2 * pi / n
            start_rad = pi - rad_spacing / 2
            rad = (-atan2(x, y) - start_rad - self.offsets_angle) % (2 * pi)
            self.selected = int(rad / rad_spacing)
            self.selected = n - 1 if rad < 0 else self.selected

            do_callback("motion", self.callbacks, self, ev, x, y, rad)

        if ev.type == pygame.MOUSEBUTTONUP and self.config['mouse_wheel']:
            if ev.button == 4:
                self.last_select()
            if ev.button == 5:
                self.next_select()
    
    def keyboard_focus(self):
        if self.config['keyboard'] is False:
            return
        
        keymap = pygame.key.get_pressed()
        self.select_state[0] = False
        self.select_state[1] = False

        for i in self.key['last']:
            if keymap[i]:
                self.select_state[0] = True
                break

        for i in self.key['next']:
            if keymap[i]:
                self.select_state[1] = True
                break

    def is_active(self, ev, x, y, st):
        if self.selected is None:
            return False
        if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and self.config['mouse_active']:
            return True
        if ev.type == pygame.KEYUP and ev.key in self.key['active'] and self.config['keyboard_active']:
            return True
        callback_result = do_callback('is_active', self.callbacks, self, ev, x, y, st)
        return callback_result if callback_result is not None else False

    def active(self):
        selected = self.get_select_child()
        do_callback('active', self.callbacks, self, selected, self.selected)
        if isinstance(selected, renpy.display.behavior.Button):
            renpy.run(selected.clicked)

    def solve_select(self, st, last_state):
        if True not in self.select_state:
            self.select_state_st = None
        

        if any(self.select_state):
            delay = 0.0

            if self.select_state_st is None or last_state != self.select_state:
                self.select_state_st = st
                delay = 0.3
            elif st - self.select_state_st > 0:
                delay += 0.04

            if st - self.select_state_st >= 0:
                if self.select_state[1]:
                    self.next_select()
                else:
                    self.last_select()

            self.select_state_st += delay
            renpy.timeout(0.0)

        do_callback('solve_select', self.callbacks, self, st)
    
    def apply_focus(self, last):
        if last != self.selected:
            if self.selected is not None:
                self.children[self.selected].focus()
            if last is not None:
                self.children[last].unfocus()

            do_callback(
                'apply_focus', 
                self.callbacks, 
                self,
                self.children[self.selected] if self.selected is not None else None,
                self.children[last] if last is not None else None,
                self.selected
                )
            
            renpy.redraw(self, 0)

    def next_select(self):
        if self.selected is None:
            self.selected = 0
        else:
            self.selected = (self.selected + 1) % len(self.children)

    def last_select(self):
        if self.selected is None:
            self.selected = 0
        else:
            self.selected = (self.selected - 1) % len(self.children)

    def get_select_child(self):
        return self.children[self.selected] if self.selected is not None else None



renpy.register_sl_displayable("circle_layout", CircleLayout, "", 2
    ).add_property("offsets_angle"
    ).add_property("r")

renpy.register_sl_displayable("circle_menu", CircleMenu, "", 2
    ).add_property("offsets_angle"
    ).add_property("r"
    ).add_property("mouse_check_r"
    ).add_property("callbacks"
    ).add_property("config")


# 顺带一提, 我很久没写了, 有点梦到什么写什么的感觉了 ( )