"""renpy

python early:
"""


from typing import Iterable


class EasyStellaText(renpy.Displayable):
    def __init__(self, text, font_size = 100, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 可视化组件
        self.text = Text(text, color="#fff", size=font_size)
        self.anti_text = Text(text, color="#aaa", size=font_size)


    def render(self, width, height, st, at):
        # 渲染处理
        rv = renpy.Render(width, height)
        text_render = self.text.render(width, height, st, at)
        anti_text_render = self.anti_text.render(width, height, st, at)  

        # 获取B组件覆盖A组件的宽度
        text_width = anti_text_render.get_size()[0]

        # 计算 B 组件显示的头和尾
        cut_time = st % 2
        head_pos = (cut_time - 1) * text_width if 0 < cut_time - 1 < 1 else 0
        end_pos = cut_time * text_width if 0 < cut_time < 1 else text_width

        # # 添加缓动曲线后的版本
        # head_pos = _warper.ease_quint(cut_time - 1) * text_width if 0 < cut_time - 1 < 1 else 0
        # end_pos = _warper.ease_quint(cut_time) * text_width if 0 < cut_time < 1 else text_width

        # 将此 Render 进行裁剪
        anti_text_render = anti_text_render.subsurface((head_pos, 0, end_pos, anti_text_render.get_size()[1]))

        # 先绘制 A 组件
        rv.blit(text_render, (0, 0))
        
        rv.canvas().rect((255, 255, 255), (head_pos, 0, end_pos-head_pos, anti_text_render.get_size()[1]))
        
        # 再绘制 B 组件
        rv.blit(anti_text_render, (head_pos, 0))

        renpy.redraw(self, 0)

        return rv



class BetterStellaText(renpy.Displayable):
    def __init__(self, text, font_size = 100, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = Text(text, color="#fff", size=font_size)
        self.anti_text = Text(text, color="#000", size=font_size)
        self.bg_boarder = [15, 1]
        self.bg_color = (255, 255, 255)

        self.last_st = None
        self.anima_ratio = 0.0
        self.complete_time = 0.5
        self.is_hover = None

        self.size = (font_size*len(text), font_size)

    def event(self, ev, x, y, st):
        if ev.type == pygame.MOUSEMOTION:
            self.is_hover = (0 < x < self.size[0] and 0 < y < self.size[1])

        if self.last_st is None:
            self.last_st = st

        if st != self.last_st:
            old_ratio = self.anima_ratio
            
            self.anima_ratio += (st - self.last_st) / self.complete_time * (bool(self.is_hover) - 0.5) * 2
            if 0.0 < self.anima_ratio < 1.0 or 0.0 < old_ratio < 1.0: 
                renpy.redraw(self, 0)
                renpy.timeout(0.015)
            
            if (0.0 < self.anima_ratio < 1.0) is False:
                self.anima_ratio = self.anima_ratio > 0
            
            self.last_st = st


    def render(self, width, height, st, at):
        rv = renpy.Render(width, height)
        text_render = self.text.render(width, height, st, at)
        
        if self.size != text_render.get_size():
            self.size = text_render.get_size()

        if self.anima_ratio == 0:
            rv.blit(text_render, (0, 0))
            return rv

        elif self.anima_ratio == 1:
            anti_text_render = self.anti_text.render(width, height, st, at)
            rv.canvas().rect(self.bg_color, (-self.bg_boarder[0], 0, anti_text_render.get_size()[0] + self.bg_boarder[0] * 2, anti_text_render.get_size()[1] + self.bg_boarder[1]))
            rv.blit(anti_text_render, (0, 0))
            return rv

        # 如果动画介于 0.0 ~ 1.0 里
        elif 0 < self.anima_ratio < 1:
            # 获取B组件覆盖A组件的宽度
            ratio = _warper.ease_quint(self.anima_ratio)
            mid = int(text_render.get_size()[0]*ratio)

            # 获取B组件完整的 Render
            anti_text_render = self.anti_text.render(width, height, st, at)
            # 将此 Render 进行裁剪
            anti_text_render = anti_text_render.subsurface((0, 0, mid, anti_text_render.get_size()[1]))

            # 先绘制 A 组件
            rv.blit(text_render, (0, 0))

            rv.canvas().rect(self.bg_color, (-self.bg_boarder[0]*ratio, 0, int(mid + self.bg_boarder[0] * 2 * ratio), anti_text_render.get_size()[1] + self.bg_boarder[1]))

            # 绘制 B 组件覆盖到 A 组件上
            rv.blit(anti_text_render, (0, 0))

            return rv

