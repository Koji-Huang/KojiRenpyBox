init python:
    def TT_mix_2(a, b, k):
        return (a[0]*(1 - k) + b[0] * k, a[1] * (1 - k) + b[1] * k)

    class CircleLoadingAnima(DrawCircle):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.info.degree = (0, 0)

        def render(self, w, h, st, at):
            head = st * 3.14 * 2 + _warper.ease_back(sin(st) * 0.5 + 0.5)
            end = (cos(st) + 1.2) * (3.14 - 0.5)
            self.info.degree = (head, end)
            renpy.redraw(self, 0)
            return super().render(w, h, st, at)

    class LineLoadingAnima(DrawLine):
        def __init__(self, *args, later=0, **kwargs):
            super().__init__(*args, **kwargs)
            self.primer = (self.info.start_pos, self.info.end_pos)
            self.later=later

        def render(self, w, h, st, at):
            head = TT_mix_2(*self.primer, _warper.ease_expo((sin(st+self.later)) * 0.5 + 0.5))
            end = TT_mix_2(*self.primer, _warper.ease_expo((cos(st+self.later)) * 0.5 + 0.5))
            self.info.start_pos = head
            self.info.end_pos = end
            renpy.redraw(self, 0)
            return super().render(w, h, st, at)


screen canvas_loading:
    add CircleLoadingAnima((1920/3, 1080/2), width=30, r=100, round=15, texture=canvas_texture)
    add LineLoadingAnima((1920/6+1920/2, 1080/2), (1920-1920/6, 1080/2), width=40, round=20, texture=canvas_texture.__copy__(blend=1.0, alpha=0.0))
    add LineLoadingAnima((1920/6+1920/2, 1080/2), (1920-1920/6, 1080/2), width=40, round=20, later=3.14*2/3, texture=canvas_texture.__copy__(blend=1.0, alpha=0.0))
    add LineLoadingAnima((1920/6+1920/2, 1080/2), (1920-1920/6, 1080/2), width=40, round=20, later=3.14*4/3, texture=canvas_texture.__copy__(blend=1.0, alpha=0.0))