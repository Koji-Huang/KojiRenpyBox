"""renpy

python early:
"""


# 此组件需要和 PressImageButton 一起使用 ( 也就是 press_button_ren )
class StellaButton(PressImageButton):
    def __init__(self, text, *args, **kwargs):
        super().__init__(Text(text, color="#000"), *args, **kwargs)
        self.text = Text(text, color="#000")
        self.anti_text = Text(text, color="#fff")
        self.anti_bg = renpy.displayable("#000")
        self.anima = 0.0
        self.last_st = 0.0
        self.background_state = 0  # 0: idle  1: hover  2: select
        self.bg_boarder = [10, 3]

    def render(self, width, height, st, at):
        anima_time = 0.2
        if self.background_state != 0:
            self.anima += (st - self.last_st) / anima_time
            if self.anima > 1.0: self.anima = 1.0
            renpy.redraw(self, 0)
        else:
            self.anima -= (st - self.last_st) / anima_time
            if self.anima < 0.0: self.anima = 0.0
            renpy.redraw(self, 0)

        self.last_st = st
        rv = renpy.Render(width, height)

        if self.anima == 0:
            return self.text.render(width, height, st, at)

        elif self.anima == 1:
            anti_text_render = self.anti_text.render(width, height, st, at)
            anti_bg_render = self.anti_bg.render(
                anti_text_render.get_size()[0] + self.bg_boarder[0] * 2, 
                anti_text_render.get_size()[1] + self.bg_boarder[1] * 2
                , st, at)

            rv.blit(anti_bg_render, (-self.bg_boarder[0], -self.bg_boarder[1]))
            rv.blit(anti_text_render, (0, 0))

            return rv

        elif 0 < self.anima < 1:
            fade = _warper.ease_quint(self.anima)
            
            text_render = self.text.render(width, height, st, at)

            height = text_render.get_size()[1]
            mid = int(text_render.get_size()[0]*fade)

            anti_text_render = self.anti_text.render(width, height, st, at).subsurface((0, 0, mid, height))
            anti_bg_render = self.anti_bg.render(
                anti_text_render.get_size()[0] + self.bg_boarder[0] * 2, 
                anti_text_render.get_size()[1] + self.bg_boarder[1] * 2, 
                st, at).subsurface((0, 0, mid + int(self.bg_boarder[0]*2*fade), height + self.bg_boarder[1]*2))

            rv.blit(text_render, (0, 0))
            rv.blit(anti_bg_render, (-self.bg_boarder[0], -self.bg_boarder[1]))
            rv.blit(anti_text_render, (0, 0))

            renpy.redraw(self, 0)

            return rv

