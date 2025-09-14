# 注: circle_menu 是可以正常使用 xalign, yalign 之类的
# 这里用 pos 来确定中心是因为 canvas 组件的缺陷

default circle_texture = TextureInfo(color=(1.0, 1.0, 1.0, 0.0), alpha=1.0, blend=0.1, val_pow=0.01)

default bg_circle = CircleInfo((0, 0), texture=circle_texture.__copy__())
default choice_circle = CircleInfo((0, 0), round=10, texture=circle_texture.__copy__())
default follow_circle = CircleInfo((0, 0), round=20, texture=circle_texture.__copy__())


init python:
    def change_focus_area(self, selected, last, index):
        # 改变选中区域的
        if index is None:
            choice_circle.texture.blend = 0.0
            return
        choice_circle.texture.blend=0.1
        size = len(self.children)
        index = (int(size/2)-index) % size - ((size+1) % 2) / 2.0
        choice_circle.degree = ( pi*2/size * index, pi*2/size,)

    def change_follow_area(self, ev, x, y, rad):
        follow_circle.degree = ( pi-rad, pi*2/len(self.children),)

    def redraw_circle(*args):
        for i in args:
            renpy.redraw(i, 0)


# 这个界面大概是可以直接调用的
screen circle_menu_with_circle(mouse_check_r=(160, 300), ring_r=230, center_point=(int(1920/2), int(1080/2))):
    python:
        bg_circle.pos = center_point
        bg_circle.r = mouse_check_r[1]/2 + mouse_check_r[0]/2
        bg_circle.width = mouse_check_r[1] - mouse_check_r[0]

        choice_circle.pos = center_point
        choice_circle.r = mouse_check_r[1]/2 + mouse_check_r[0]/2
        choice_circle.width = mouse_check_r[1] - mouse_check_r[0]

        follow_circle.pos = center_point
        follow_circle.r =  mouse_check_r[1]+10
        follow_circle.width = 50

    circle bg_circle
    circle choice_circle as cho
    circle follow_circle as fol

    timer 0.015 action Function(redraw_circle, cho, fol, _update_screens=False) repeat True

    circle_menu:
        mouse_check_r mouse_check_r
        r ring_r
        callbacks {
            "motion": change_follow_area,
            "apply_focus": change_focus_area,
            }
        textbutton "开始游戏" action Start()
        textbutton "读取游戏" action ShowMenu("load")
        textbutton "设置" action ShowMenu("preferences")
        textbutton "关于" action ShowMenu("about")
        textbutton "帮助" action ShowMenu("help")
        textbutton "退出" action Quit(confirm=not main_menu)
        pos (center_point[0] - ring_r, center_point[1] - ring_r)
        as target
    