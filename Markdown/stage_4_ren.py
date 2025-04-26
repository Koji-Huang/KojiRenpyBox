"""renpy

python early:
"""


class EasyQuickMenu(renpy.Displayable):
    def __init__(self, *menu_items):
        super().__init__()
        self.items = tuple(renpy.displayable(i) for i in menu_items)  # 生成各个子控件
        self.item_spacing = 200  # 每个控件的间隔
        self.items_ypos = list(0 for _ in self.items)  # 每个控件的 y 坐标 ( 会更新 )
        self.items_xpos = tuple(i * self.item_spacing for i in range(len(self.items)))  # 每个控件的 x 坐标

    def event(self, ev, x, y, st):
        # 循环传入事件
        for i in range(len(self.items)):
            self.items[i].event(ev, x - self.items_xpos[i], y - self.items_ypos[i], st)

    def render(self, width, height, st, at):
        # 循环绘制所有子组件
        rv = renpy.Render(width, height)
        for i in range(len(self.items)):
            rv.blit(self.items[i].render(100, 100, st, at), (self.items_xpos[i], self.items_ypos[i]))
        return rv

    def set_spacing(self, args):
        self.item_spacing = args
        self.items_xpos = tuple(i * self.item_spacing for i in range(len(self.items)))  # 每个控件的 x 坐标


class NeatQuickMenu(renpy.Displayable):
    def __init__(self, *menu_items):
        super().__init__()
        self.items = tuple(renpy.displayable(i) for i in menu_items)  # 生成各个子控件
        self.item_spacing = 20
        self.items_ypos = list(0 for _ in self.items)  # 每个控件的 y 坐标 ( 会更新 )
        self.items_xpos = list()

    def event(self, ev, x, y, st):
        # 如果 xpos 并没有正确, 直接不接受此事件
        if len(self.items_xpos) != len(self.items):
            return
        
        for i in range(len(self.items)):
            self.items[i].event(ev, x - self.items_xpos[i], y - self.items_ypos[i], st)

    def render(self, width, height, st, at):
        rv = renpy.Render(width, height)
        
        # 清楚掉记录下来的 xpos
        self.items_xpos.clear()

        # 子组件所在的 xpos
        xpos = 0
        
        # 循环绘制所有子组件
        for i in range(len(self.items)):
            # 获取子组件的 render
            render = self.items[i].render(width, height, st, at)
            # 将此 render 绘制到 rv 上
            rv.blit(render, (xpos, self.items_ypos[i]))
            # 将此坐标加入到自己坐标记录里
            self.items_xpos.append(xpos)
            # 下一个组件的 xpos 就为此组件的 xpos + 固定的间距 + 当前子组件的宽
            xpos += self.item_spacing + render.get_size()[0]

        return rv


class RedrawableQuickMenu(renpy.Displayable):
    def __init__(self, *menu_items):
        super().__init__()
        self.items = tuple(renpy.displayable(i) for i in menu_items)
        self.item_spacing = 20
        self.items_ypos = list(0 for _ in self.items)
        self.items_xpos = list()

    def event(self, ev, x, y, st):
        for i in range(len(self.items)):
            self.items[i].event(ev, x - self.items_xpos[i], y - self.items_ypos[i], st)

    def render(self, width, height, st, at):
        rv = renpy.Render(width, height)

        self.items_xpos.clear()
        xpos = 0

        for i in range(len(self.items)):
            # 使用新的函数获取 render
            rend = renpy.render(self.items[i], 100, 100, st, at)
            rv.blit(rend, (self.items_xpos[i], self.items_ypos[i]))
            self.items_xpos.append(xpos)
            xpos += self.item_spacing + render.get_size()[0]

        return rv


class QuickerQuickMenu(renpy.Displayable):
    def __init__(self, *menu_index):
        super().__init__()
        self.items = menu_index
        self.item_spacing = 200
        self.items_ypos = list(0 for _ in self.items)
        self.items_xpos = tuple(i * self.item_spacing for i in range(len(self.items)))
        self.selected_index = -1
        self.hovered_index = -1

    def event(self, ev, x, y, st):
        # 当鼠标移动时
        if ev.type == pygame.MOUSEMOTION:

            # 记录旧索引, 重置新索引
            old_hover = self.hovered_index
            self.hovered_index = -1

            # 如果鼠标在次可视化组件内并选中了一个组件, 更新当前选中的索引
            if 0 <= y <= 100:
                self.hovered_index = int(x / self.item_spacing)
                if (0 <= self.hovered_index < len(self.items)) is False:
                    self.hovered_index = -1

            # 如果有当前覆盖和上次覆盖的对象不一样且上次确实覆盖了一个子对象
            if old_hover != self.hovered_index and old_hover != -1:
                self.items[old_hover].event(ev, x - self.items_xpos[old_hover], y - self.items_ypos[old_hover], st)
                renpy.redraw(self, 0)

            # 如果当前覆盖的对象不为空, 传入 event
            if self.hovered_index != -1: 
                self.items[self.hovered_index].event(ev, x - self.items_xpos[self.hovered_index], y - self.items_ypos[self.hovered_index], st)

        # 如果是鼠标按下事件
        if ev.type == pygame.MOUSEBUTTONDOWN and self.hovered_index != -1:
            self.selected_index = self.hovered_index
            renpy.redraw(self, 0)
            self.items[self.hovered_index].event(ev, x - self.items_xpos[self.hovered_index], y - self.items_ypos[self.hovered_index], st)
            raise renpy.display.core.IgnoreEvent()

        # 如果是鼠标抬起事件
        if ev.type == pygame.MOUSEBUTTONUP and self.selected_index != -1:
            self.selected_index= -1
            renpy.redraw(self, 0)
            return self.items[self.hovered_index].event(ev, x - self.items_xpos[self.hovered_index], y - self.items_ypos[self.hovered_index], st)
            raise renpy.display.core.IgnoreEvent()
        
    def render(self, width, height, st, at):
        rv = renpy.Render(width, height)
        for i in range(len(self.items)):
            rend = renpy.render(self.items[i], 100, 100, st, at)
            rv.blit(rend, (self.items_xpos[i], self.items_ypos[i]))
        return rv
