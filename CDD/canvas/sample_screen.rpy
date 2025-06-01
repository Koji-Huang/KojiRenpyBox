
init python:
    # 物体旋转 callback  ( render_callback )
    def sping_circle(obj, w, h, st, at):
        obj.info.degree = obj.info.degree[0] + 0.0001 * obj.info.r, obj.info.degree[1]
        renpy.redraw(obj, 0)

    # 鼠标跟踪 callback ( event_callback )
    def mouse_follow(obj, ev, x, y, st):
        if "_pos" not in obj.info.__dir__():
            obj.info._pos = obj.info.pos
        obj.info.pos = obj.info._pos[0] + x / 1920 * 30, obj.info._pos[1] + y / 1080 * 30
    
    def hight_light(obj, ev, x, y, st):
        if ev.type == pygame.MOUSEMOTION:
            x -= 900/2
            y -= 100/2
            dis = sqrt(x*x + y*y)
            val = dis / 300
            val = val if val < 0.5 else 0.5
            obj.info.texture.alpha = val
            renpy.redraw(obj, 0.0)



screen canvas_screen:
    # 左侧圆圈特效的 info
    default circle_info = CircleInfo((400, 1080/2), r=100, round=10, width=30, degree=(0, 6), texture=canvas_texture.__copy__(), )
    # 右侧按钮的 info
    default rect_info = RectInfo((0, 0, 900, 100), round = 40, texture=canvas_texture.__copy__(blend=0.8, alpha=0.5))

    # 背景
    rect:
        rect_area (0, 0, 1920, 1080)
        texture canvas_texture.__copy__(color=(0.0, 0.0, 0.0, 0.5), blend=0.5)

    # 左侧旋转
    circle:
        info circle_info.__copy__(degree=(0, 7), width=0)
        render_callback sping_circle
        event_callback mouse_follow

    circle:
        info circle_info.__copy__(r=200)
        render_callback sping_circle 
        event_callback mouse_follow
    
    circle:
        info circle_info.__copy__(r=300)
        render_callback sping_circle 
        event_callback mouse_follow
    
    circle:
        info circle_info.__copy__(r=400, degree=(0, 7), width=50)
        render_callback sping_circle 
        event_callback mouse_follow

    # 右侧组件
    rect:
        rect_area (700, 100, 1170, 880)
        round 100
        texture canvas_texture.__copy__(color=(0.0, 0.0, 0.0, 0.5), blend=0.2, alpha=0.0)

    line:
        start_pos (1920-120, 180)
        end_pos (1920-120, 1080-180)
        width 30
        round 15
        texture canvas_texture.__copy__(blend=0.5, alpha=0.3)

    # 各个按钮
    vbox:
        xpos 800
        yalign 0.5
        xysize (1100, 600)
        spacing 20
        rect info rect_info.__copy__() xysize (900, 100) event_callback hight_light
        rect info rect_info.__copy__() xysize (900, 100) event_callback hight_light
        rect info rect_info.__copy__() xysize (900, 100) event_callback hight_light
        rect info rect_info.__copy__() xysize (900, 100) event_callback hight_light
        rect info rect_info.__copy__() xysize (900, 100) event_callback hight_light

