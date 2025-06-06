"""renpy

python early:
"""

class PressChange(renpy.Displayable):
    def __init__(self, press_image, unpress_image):
        super().__init__()
        self.press_image = renpy.displayable(press_image)  # 按下时的图片
        self.unpress_image = renpy.displayable(unpress_image)  # 鼠标常态图片 ( 不按下时 )
        self.is_pressing = False

    def event(self, ev, x, y, st):
        # 如果鼠标按钮按下或者抬起, 则进行一次检测
        if ev.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            # 储存上次的状态
            old_state = self.is_pressing

            # 如果存在按下的鼠标按钮, is_pressing 为 True
            self.is_pressing = True in pygame.mouse.get_pressed()

            # 如果状态发生变化, 重新绘制该可视化组件
            if old_state != self.is_pressing:
                renpy.redraw(self, 0)

    def render(self, width, height, st, at):
        # 根据不同的情况返回不同的 Render
        if self.is_pressing:
            return self.press_image.render(width, height, st, at)
        else:
            return self.unpress_image.render(width, height, st, at)


class HoverChange(renpy.Displayable):
    def __init__(self, hover_image, unhover_image, area=(100, 100)):
        super(HoverChange, self).__init__()
        self.hover_image = renpy.displayable(hover_image)
        self.unhover_image = renpy.displayable(unhover_image)
        self.area = area  # 定义检测区域
        self.hovering = False

    def event(self, ev, x, y, st):
        old_state = self.hovering

        # 判断状态
        self.hovering = 0 < x < self.area[0] and 0 < y < self.area[1]

        if self.hovering != old_state:
            renpy.redraw(self, 0)

    def render(self, width, height, st, at):
        if self.hovering:
            return self.hover_image.render(width, height, st, at)
        else:
            return self.unhover_image.render(width, height, st, at)


class PressHoverChange(renpy.Displayable):
    def __init__(self, active_image, negative_image, area=(100, 100)):
        super(PressHoverChange, self).__init__()
        self.active_image = renpy.displayable(active_image)
        self.negative_image = renpy.displayable(negative_image)
        self.area = area
        self.is_active = False

    def event(self, ev, x, y, st):
        old_state = self.is_active

        # 当鼠标在范围内按下时
        if ev.type == pygame.MOUSEBUTTONDOWN and (0 < x < self.area[0] and 0 < y < self.area[1]):  
            self.is_active = True

            # 因为 raise 的机制, 我们只能在 raise 前检测 state 是否发生变化
            if old_state != self.is_active:
                renpy.redraw(self, 0)

            # 阻止事件传输到其他可视化组件
            raise renpy.display.core.IgnoreEvent()

        # 当鼠标抬起并且控件处于按下状态时
        if ev.type == pygame.MOUSEBUTTONUP and self.is_active:
            self.is_active = True in pygame.mouse.get_pressed()

            if old_state != self.is_active:
                renpy.redraw(self, 0)

            # 阻止事件传输到其他可视化组件
            raise renpy.display.core.IgnoreEvent()


    def render(self, width, height, st, at):
        if self.is_active:
            return self.active_image.render(width, height, st, at)
        else:
            return self.negative_image.render(width, height, st, at)
