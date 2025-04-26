"""renpy

python early:
"""

# 定义一个可视化组件
class ShowColor(renpy.Displayable):
    def __init__(self, color, pos=(0, 0), size=(100, 100)):
        # 此组件必须传入一个 color 参数, pos 和 size 均有默认值
        super().__init__()
        self.image = renpy.displayable(color)
        self.size = size
        self.pos = pos

    def render(self, w, h, st, at):
        rv = renpy.Render(*self.size)
        rv.blit(self.image.render(*self.size, st, at), self.pos)
        return rv

# 将 'show_color' 关键字定义为 ShowColor 组件, 此组件接收0个子组件
renpy.register_sl_displayable("show_color", ShowColor, 0
    ).add_positional("color"  # 此组件有一个名为 color 的固定入参
    ).add_property("size"  # 此组件有一个 size 特性
    ).add_property("pos")  # 此组件有一个 pos 特性




class ShakeText(renpy.text.text.Text):
    def __init__(self, text, shake_range=(10, 5), *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.shake_range = shake_range
    
    def render(self, w, h, st, at):

        obj = super().render(w, h, st, at)

        rand = 1.0*randint(0, 628)/100

        rv = renpy.Render(*obj.get_size())

        rv.blit(obj, (sin(rand)*self.shake_range[0], cos(rand)*self.shake_range[1]))

        renpy.redraw(self, 0)

        return rv

renpy.register_sl_displayable("shake_text", ShakeText, "", 0
    ).add_positional("text"  # 固定参数
    ).add_property("shake_range"  # 额外参数
    ).add_property_group('text')  # text 参数组



class ShakeLayout(renpy.Displayable):
    def __init__(self, shake_range=(10, 5), *args, **kwargs):
        super().__init__()
        self.shake_range = shake_range
        self.children = list()
        self.offset = list()
    
    def render(self, w, h, st, at):
        rv = renpy.Render(w, h)
        self.offset.clear()

        rand = 1.0*randint(0, 628)/100

        for i in self.children:
            son_rv = renpy.render(i, w, h, st, at)
            pos = i.place(rv, sin(rand)*self.shake_range[0], cos(rand)*self.shake_range[1], w, h, son_rv)
            self.offset.append(pos)

        renpy.redraw(self, 0)

        return rv
    
    def event(self, ev, x, y, st):
        if len(self.children) != len(self.offset):
            return

        for i in range(len(self.children)):
            self.children[i].event(ev, x - self.offset[i][0], y - self.offset[i][1], st)

    def add(self, d):
        self.children.append(d)

    def remove(self, d):
        self.children.remove(d)


renpy.register_sl_displayable("shake", ShakeLayout, "", 2
    ).add_property("shake_range")


# 以下内容请放到某个 rpy 文件里使用捏
# """renpy

# screen show_color_test:
#     hbox:
#         spacing 20

#         show_color "#fff"   # 调用 ShowColor 组件, color 为 "#fff"

#         show_color "#ddd"   # 调用 ShowColor 组件, color 为 "#ddd"

#         show_color "#aaa":   # 调用 ShowColor 组件, color 为 "#aaa"
#             size (200, 100)   # 此组件的 size 为 200, 100

#         show_color "#888":  # 调用 ShowColor 组件, color 为 "#888"
#             pos (0, -20)   # 此组件的 pos 为 200, 100

    
# screen shake_text_test:
#     hbox:
#         shake_text "一个抖动的字体"
#         shake_text "一个很大的抖动字体" text_size 50
#         shake_text "一个很粗很抖的抖动字体" shake_range (50, 50) bold True


# screen shake_layout_test:
#     shake:
#         text "你干嘛~"
#         text "干什么!" xpos 100
#         textbutton "什么功能都没有噢" action NullAction()
    
#     shake:
#         shake_range (50, 50)
#         text "这边晃得更厉害了!"
#         text "头好晕啊啊啊啊"
# """