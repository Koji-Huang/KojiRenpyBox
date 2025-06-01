'''

Copyright 2025.5.18 Koji-Huang(koji233@163.com)

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

init python:
"""

renpy.register_shader("cloud_node_point", 
    variables = """
        uniform vec4 u_color;
        attribute vec4 a_position;
        uniform vec2 u_model_size;
        varying vec2 v_uv;
    """,
    vertex_300="""
        v_uv = vec2(a_position.x / u_model_size.x, a_position.y / u_model_size.y);
    """,
    fragment_300="""
        gl_FragColor = u_color * (0.5 - length(v_uv-vec2(0.5, 0.5))) * 2;
    """
    )

renpy.register_shader("cloud_node_line", 
    variables = """
        uniform vec4 u_color;
        uniform float u_width;
        attribute vec4 a_position;
        uniform vec2 u_model_size;
        varying vec2 v_uv;
        uniform vec4 u_line;
    """,
    vertex_300="""
        v_uv = vec2(a_position.x / u_model_size.x, a_position.y / u_model_size.y);
    """,
    fragment_300="""

        vec4 line = u_line;
        vec2 uv = v_uv;
        float val = 0.0;
        float dis = abs(line[2] * uv.x - uv.y + line[3]) / sqrt(1 + pow(line[2], 2));
        if(dis < u_width) val = 1.0 - dis / u_width;
        gl_FragColor = u_color * val;
    """
    )




import random
from time import time
from math import sqrt
# import numpy

def TI_mul_2(a, b):
    return (a[0]*b, a[1]*b)
def TI_mul_4(a, b):
    return (a[0]*b, a[1]*b, a[2]*b, a[3]*b)

def TT_add_2(a, b):
    return (a[0]+b[0], a[1]+b[1])
def TT_sub_2(a, b):
    return (a[0]-b[0], a[1]-b[1])
def TT_mul_2(a, b):
    return (a[0]*b[0], a[1]*b[1])
def TT_div_2(a, b):
    return (a[0]/b[0], a[1]/b[1])
def TT_mix_2(a, b, k):
    return (a[0]*(1 - k) + b[0] * k, a[1] * (1 - k) + b[1] * k)
def TT_dis(vec):
    return sqrt(pow(vec[0], 2) + pow(vec[1], 2))

def int_limit(a, minx, manx):
    return minx if a < minx else manx if a > manx else a

def point_in_screen(node):
    return 0 < node.pos[0] < 1 and 0 < node.pos[1] < 1
def make_line(node_a, node_b, node_cost, w=1.0):
    k = node_cost[1] / node_cost[0]
    return node_a.pos[0], node_b.pos[0], k, node_a.pos[1] - node_a.pos[0] * k, w


# 点对象
class Node:
    def __init__(self, pos, st, vec=(0, 0), color=(255, 255, 255, 255)):
        self.pos = pos
        self.st = st
        self.vec = vec
        self.color = color
        self.w = 0.0


# 点生成更新, 线生成更新
class CloudNodeAlgorithms:
    def __init__(self):
        self.node = list()

        self.node_dead_time = 3.0
        self.link_length = 0.05
        self.mouse_r = 0.04
        self.mouse_R = 0.15
        self.mouse_w = 1.0
        self.mouse_k = 1.0
        self.mouse_f = 0.25

        self.line = tuple()
        self.triangle = tuple()

        self.last_st = None

    def add_node(self, st=0.0):
        self.node.append(
            Node(
                pos = (random.random(), random.random()),
                st  = st,
                vec = ((random.random()*2 - 1.0) / 20, (random.random()*2 - 1.0) / 20), )
            )

    def sort_node(self):
        self.node.sort(key=lambda each_node: each_node.pos[0])

    def clean_dead_node(self):
        self.node = [i for i in self.node if i.st < self.node_dead_time and (-self.link_length < i.pos[0] < 1.0+self.link_length and -self.link_length < i.pos[1] < 1.0+self.link_length)]

    def update_node(self, st, mouse_pos=None):
        self.clean_dead_node()

        if self.last_st is None: 
            self.last_st = st - 0.01

        cost_st = st - self.last_st
        self.last_st = st

        if self.mouse_w is not None:
            limit_w = int_limit(self.mouse_w, 0.0, 1.0)

        for node in self.node:
            vec = node.vec

            if mouse_pos is not None and self.mouse_w is not None:
                dis = TT_dis(TT_sub_2(mouse_pos, node.pos))
                if dis < self.mouse_R:
                    addin = TI_mul_2(TT_sub_2(node.pos, mouse_pos), -(dis - self.mouse_r) / dis * self.mouse_w * self.mouse_k)
                    vec = TT_add_2(vec, addin)
                    node.vec = TT_mix_2(node.vec, TI_mul_2(addin, self.mouse_k * (dis - self.mouse_r) * 50), self.mouse_f)

            node.pos = TT_add_2(node.pos, TI_mul_2(vec, cost_st))
            node.st += cost_st

            w = node.st / self.node_dead_time

            if w < 0.2: w = w * 5
            elif w > 0.8: w = (1.0 - w) * 5
            else: w = 1.0

            node.w = w

        self.sort_node()

    def update_line(self):
        line = list()
        
        for left in range(len(self.node)-2):
            for right in range(left+1, len(self.node)):
                cost = TT_sub_2(self.node[left].pos, self.node[right].pos)
                if abs(cost[0]) > self.link_length:
                    break
                dis = TT_dis(cost)
                if abs(cost[1]) < self.link_length and dis < self.link_length:
                    line.append(make_line(self.node[left], self.node[right], cost, min(self.node[left].w, self.node[right].w) * (1.0 - dis/self.link_length)))


        self.line = tuple(line)



# 渲染
class CloudNode(renpy.Displayable):
    def __init__(self, 
            color=(1.0, 1.0, 1.0, 0.0), 
            node_dead_time = 3.0,
            link_length = 0.05,
            line_width = 0.1,
            mouse_r = 0.04,
            mouse_R = 0.15,
            mouse_w = 1.0,
            mouse_k = 1.0,
            mouse_f  = 0.25,
            node_add_speed = 60.0,
            node_size = (5, 5)
            ):
        super().__init__()
        self.algo = CloudNodeAlgorithms()

        self.node_model = Model()
        self.node_model.shader("cloud_node_point")
        self.node_model.uniform("u_color", color)

        self.line_model = Model()
        self.line_model.shader("cloud_node_line")
        self.line_model.uniform("u_color", color)
        self.last_st = None
        self.last_pos = (0, 0)

        self.node_add_speed = node_add_speed
        self.node_addin_count = 0.0
        self.node_size = node_size
        self.line_width = line_width
        self.color = color
        self.node_dead_time = node_dead_time
        self.link_length = link_length
        self.mouse_r = mouse_r
        self.mouse_R = mouse_R
        self.mouse_w = mouse_w
        self.mouse_k = mouse_k
        self.mouse_f = mouse_f

    def render(self, w, h, st, at):
        self.algo.update_node(st, (self.last_pos[0] / w, self.last_pos[1] / h))
        self.algo.update_line()

        rv = renpy.Render(w, h)

        self.node_model.uniform("u_color", self._color)
        node_render = self.render_point(w, h, st, at)
        for node in self.algo.node:
            if node.w != 1.0:
                rv.blit(self.render_point(w, h, st, at, TI_mul_4(self.color, node.w)), (w * node.pos[0]-self.node_size[0]/2, h * node.pos[1]-self.node_size[1]/2))
            else:
                rv.blit(node_render, (w * node.pos[0]-self.node_size[0]/2, h * node.pos[1]-self.node_size[1]/2))

        for line in self.algo.line:
            rend = self.render_line(w, h, st, at, line)

            point = (line[0] * w, (line[0] * line[2] + line[3]) * h), (line[1] * w, (line[1] * line[2] + line[3]) * h)

            rv.blit(rend, (min(point[0][0], point[1][0]), min(point[0][1], point[1][1])), point)

        renpy.redraw(self, 0)
        return rv

    def render_point(self, w, h, st, at, color=None):
        if color is not None:
            self.node_model.uniform("u_color", color)
        return self.node_model.render(*self.node_size, st, at)

    def render_line(self, w, h, st, at, line, point=None):
        if point is None:
            point = (line[0] * w, (line[0] * line[2] + line[3]) * h), (line[1] * w, (line[1] * line[2] + line[3]) * h)
        k_bigger_1 = line[2] > 0
        self.line_model.uniform("u_line", (0, 1.0, (k_bigger_1 - 0.5) * 2, not k_bigger_1))
        self.line_model.uniform("u_width", self.line_width * line[4])
        return self.line_model.render(abs(point[0][0] - point[1][0]), abs(point[0][1] - point[1][1]), st, at)
    
    def event(self, ev, x, y, st):
        if self.last_st is None:
            self.last_st = st - 0.015
        
        self.last_pos = (x, y)

        if self.last_st != st:
            self.node_addin_count += (st - self.last_st) * self.node_add_speed
            while self.node_addin_count > 1:
                self.node_addin_count -= 1
                self.algo.add_node()

            self.last_st = st
            renpy.timeout(0.015)

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, val):
        self._color = val
        self.node_model.uniform("u_color", self._color)
        self.line_model.uniform("u_color", self._color)

    @property
    def node_dead_time(self):
        return self.algo.node_dead_time
    
    @node_dead_time.setter
    def node_dead_time(self, val):
        self.algo.node_dead_time = val

    @property
    def link_length(self):
        return self.algo.link_length
    
    @link_length.setter
    def link_length(self, val):
        self.algo.link_length = val

    @property
    def mouse_r(self):
        return self.algo.mouse_r
    
    @mouse_r.setter
    def mouse_r(self, val):
        self.algo.mouse_r = val

    @property
    def mouse_R(self):
        return self.algo.mouse_R
    
    @mouse_R.setter
    def mouse_R(self, val):
        self.algo.mouse_R = val

    @property
    def mouse_w(self):
        return self.algo.mouse_w
    
    @mouse_w.setter
    def mouse_w(self, val):
        self.algo.mouse_w = val

    @property
    def mouse_k(self):
        return self.algo.mouse_k
    
    @mouse_k.setter
    def mouse_k(self, val):
        self.algo.mouse_k = val

    @property
    def mouse_f(self):
        return self.algo.mouse_f
    
    @mouse_f.setter
    def mouse_f(self, val):
        self.algo.mouse_f = val
    

test_a = CloudNode()
test_a.color = (0.0, 0.6, 0.9, 0)