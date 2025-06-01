init python:
    import pygame

    class CanvasRectButton(DrawRect):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.info = self.info.__copy__()
            self.state = 0
            self.size = None
            self.last_st = None
            self.anima = 0.0
        
        def event(self, ev, x, y, st):
            if self.size is None:
                return
            
            in_range = 0 < x < self.size[0] and 0 < y < self.size[1]

            if self.state - in_range and self.state != 2:
                self.state = in_range
                self.last_st = None
                renpy.redraw(self, 0)

            elif ev.type == pygame.MOUSEBUTTONDOWN and in_range:
                self.state += (1.5 - self.state) * 2
                self.last_st = None
                renpy.redraw(self, 0)

        
        def render(self, w, h, st, at):
            if self.last_st is None:
                self.last_st = st - 0.001

            cost = st - self.last_st
            self.last_st = st
            cmp = (self.state > self.anima)
            self.anima += cost * (cmp * 2 - 1) * 4
            
            if (self.state > self.anima) > cmp: self.anima = self.state 
            
            if self.anima < 0: self.anima = 0
            if self.anima > 2: self.anima = 2

            anima = self.anima
            if anima > 1: anima = 1.0 + _warper.ease_expo(anima-1)
            else: anima = _warper.ease_expo(anima)

            # 鼠标遮住下
            if 0 <= anima < 1:
                # round: 100~50
                self.info.round = 80 - anima * 30
                # blend: 0.1~0.3
                self.info.texture.blend = 0.1 + anima * 0.1

            # 鼠标按下时
            if 1 <= anima <= 2:
                # round: 50~30
                self.info.round = 50 - (anima - 1) * 30
                # alpha: 0.0~0.5
                self.info.texture.alpha = (anima - 1) * 0.3
                # blend: 0.1~0.3
                self.info.texture.blend = 0.2 + (anima - 1) * 0.3

            if self.anima != self.state:
                renpy.redraw(self, 0)

            rv = super().render(w, h, st, at)
            self.size = rv.get_size()
            return rv 


screen canvas_menu:
    default button_bg = RectInfo((0, 0, 100, 100), round = 100, texture=canvas_texture.__copy__(alpha=0.0, blend=0.1, color=(1.0,1.0,1.0,0.3)))
    default menu_bg = RectInfo((0, 0, 1600, 150), round = 60, texture=canvas_texture.__copy__())

    rect:
        info menu_bg 
        yalign 0.5
        xalign 0.5 
        # xpos 90 
        xysize(1600, 150)

    hbox:
        yalign 0.5
        xalign 0.5
        spacing 20
        add CanvasRectButton(button_bg) yalign 0.5 xysize(100, 100)
        add CanvasRectButton(button_bg) yalign 0.5 xysize(100, 100)
        add CanvasRectButton(button_bg) yalign 0.5 xysize(100, 100)
        add CanvasRectButton(button_bg) yalign 0.5 xysize(100, 100)
        add CanvasRectButton(button_bg) yalign 0.5 xysize(100, 100)
        add CanvasRectButton(button_bg) yalign 0.5 xysize(100, 100)
        add CanvasRectButton(button_bg) yalign 0.5 xysize(100, 100)
        add CanvasRectButton(button_bg) yalign 0.5 xysize(100, 100)
        add CanvasRectButton(button_bg) yalign 0.5 xysize(100, 100)
        add CanvasRectButton(button_bg) yalign 0.5 xysize(100, 100)
        add CanvasRectButton(button_bg) yalign 0.5 xysize(100, 100)
        add CanvasRectButton(button_bg) yalign 0.5 xysize(100, 100)
        add CanvasRectButton(button_bg) yalign 0.5 xysize(100, 100)
