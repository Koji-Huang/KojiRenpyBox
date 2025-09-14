"""renpy

python early:
"""
from math import atan2, sin, cos, pi


class DrawEasy(renpy.Displayable):
    def __init__(self, render_callback=None, event_callback=None, info=None, **kwargs):
        super().__init__(**kwargs)
        # print("#########", info)
        self.model = Model()
        self.info = info
        self.render_callback = render_callback
        self.event_callback = event_callback
    
    def render(self, w, h, st, at):
        if self.render_callback is not None:
            if isinstance(self.render_callback, Iterable) is False:
                self.render_callback = (self.render_callback, )
            for callback in self.render_callback:
                callback(self, w, h, st, at)
        self.info.apply_uniform(self.model)
        return self.model.render(w, h, st, at)
    
    def event(self, ev, x, y, st):
        if self.event_callback is not None:
            if isinstance(self.event_callback, Iterable) is False:
                self.event_callback = (self.event_callback, )
            for callback in self.event_callback:
                callback(self, ev, x, y, st)
        return self.model.event(ev, x, y, st)


class DrawLine(DrawEasy):
    def __init__(self, start_pos=(0, 0), end_pos=(0, 0), width=5, round=0.0, texture=None, **kwargs):
        if isinstance(start_pos, LineInfo):
            kwargs['info'] = start_pos

        super().__init__(**kwargs)

        if self.info is None:
            self.info = LineInfo(start_pos, end_pos, width, round, texture)

        self.model.shader("draw_line")
        self.info.init_model(self.model)


class DrawRect(DrawEasy):
    def __init__(self, rect_area=(0, 0, 100, 100), round=0.0, width=0.0, texture=None, **kwargs):
        if isinstance(rect_area, RectInfo):
            kwargs['info'] = rect_area

        super().__init__(**kwargs)

        if self.info is None:
            self.info = RectInfo(rect_area, round, width, texture)
        
        self.model.shader("draw_rect")
        self.info.init_model(self.model)


class DrawCircle(DrawEasy):
    def __init__(self, pos=(0, 0), r=30, width=0, degree=(0, pi*2), round=30, texture=None, **kwargs):
        if isinstance(pos, CircleInfo):
            kwargs['info'] = pos
        print(pos)

        super().__init__(**kwargs)

        if self.info is None:
            self.info = CircleInfo(pos, r, width, degree, round, texture)
        
        self.model.shader("draw_circle")
        self.info.init_model(self.model)


renpy.register_sl_displayable("line", DrawLine, "", 0
    ).add_property("render_callback"
    ).add_property("event_callback"
    ).add_property("info"
    ).add_property("start_pos"
    ).add_property("end_pos"
    ).add_property("width"
    ).add_property("texture"
    ).add_property("round"
    )

renpy.register_sl_displayable("rect", DrawRect, "", 0
    ).add_property("render_callback"
    ).add_property("event_callback"
    ).add_property("info"
    ).add_property("rect_area"
    ).add_property("round"
    ).add_property("width"
    ).add_property("texture"
    )

renpy.register_sl_displayable("circle", DrawCircle, "", 0
    ).add_property("render_callback"
    ).add_property("event_callback"
    ).add_property("info"
    ).add_positional("pos"
    ).add_property("r"
    ).add_property("width"
    ).add_property("degree"
    ).add_property("round"
    ).add_property("texture"
    )
