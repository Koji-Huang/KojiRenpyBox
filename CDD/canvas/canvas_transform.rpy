'''

Copyright 2025.6.7 Koji-Huang(koji233@163.com)

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


init python:
    default_texture_info = TextureInfo(Null(), color=(1, 1, 1, 0))
    default_line_info = LineInfo((0, 0), (100, 100), texture=default_texture_info)
    default_circle_info = CircleInfo((0, 0), texture=default_texture_info)
    default_rect_info = RectInfo((0, 0, 100, 100), texture=default_texture_info)
    import random



transform draw_texture(info=default_texture_info):
    Model().child(info.displayable)

    u_color info.color
    u_alpha info.alpha
    u_blend info.blend
    u_pow info.pow
    u_relat info.relative_coord


transform LineTransform(info=default_line_info):
    draw_texture(info.texture)
    shader 'draw_line_for_transform'
    u_start_pos info.start_pos
    u_end_pos info.end_pos
    u_width info.width
    u_round info.round


transform RectTransform(info=default_rect_info):
    draw_texture(info.texture)
    shader 'draw_rect_for_transform'
    u_pos info.rect_area[:2]
    u_size info.rect_area[2:]
    u_round info.round
    u_width info.width
    

transform CircleTransform(info=default_circle_info):
    draw_texture(info.texture)
    shader 'draw_circle_for_transform'
    u_pos info.pos
    u_r info.r
    u_width info.width
    u_offset info.degree[0]
    u_radius info.degree[1]
    u_round info.round

