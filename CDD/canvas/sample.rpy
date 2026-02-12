
default canvas_image = "script/2_dialog/Canvas/test4.png"
default canvas_texture = TextureInfo(canvas_image, relative_coord=True)


screen canvas_displayable:
    text "可视化组件" size 50 ypos 100 xpos 50

    line start_pos (0, 240) end_pos (1920, 240) texture canvas_texture
    rect rect_area (0, 0, 1920, 1080) texture canvas_texture.__copy__(blend=0.1, alpha=0.1)

    fixed:
        xysize (1920, 1080 - 360)
        ypos 300

        vbox:
            spacing 20
            xalign .5
            text "目前一共有三个组件\nline (cdd: DrawLine) 绘制直线  |  rect (cdd: DrawRect) 绘制正方形  |  circle (cdd: DrawCircle) 绘制圆形"
            fixed:
                xysize (1600, 300)
                rect rect_area (0, 0, 1600, 300) texture canvas_texture
                circle pos (0, 150) r 40 texture canvas_texture.__copy__(blend=0.2, alpha=0.0)
                circle pos (0, 150) r 80 texture canvas_texture.__copy__(blend=0.2, alpha=0.0)
                circle pos (0, 150) r 120 width 20 round 10 degree (0.5, 2) texture canvas_texture.__copy__(blend=0.2, alpha=0.0)
                circle pos (0, 150) r 160 texture canvas_texture.__copy__(blend=0.2, alpha=0.0)

                for i in range(36):
                    line start_pos(1920 / 4 + i* 40, -10) end_pos(1920 / 4 + i * 40-200, 310) width i texture canvas_texture

                rect rect_area (100, 240, 1400, 50) round 25 texture canvas_texture.__copy__(blend=0.3, alpha=0.0)
            
                line start_pos (0, 40) end_pos (1920, 40) texture canvas_texture.__copy__(blend=0.5, alpha=0.0)

                text "{size=15}rect (0, 0, 1600, 300)"
                text "{size=15}{color=#000}circle (0, 150) r=40\ncircle (0, 150) r=80\ncircle(0, 150) r=120 degree(0.5, 2)\ncircle(0, 150) r=160" pos (5, 140)

                text "{size=15}{color=#fff}line: \nfor i in range(40):\nstart_pos=(480 + i*40, -10)\nend_pos=(480 + i*40 - 200, 310)\nwidth=i/4" pos (1300, 100)
            text "每个组件都继承自 DrawEasy 对象, 此对象有两个参数, render_callback 和 event_callback\n这两个参数用于在 render 和 event 时回调(具体用法可见 sample_menu)"
            text "此外, 每个组件都有对应的信息存储类型(Info), 这部分内容请见 screen canvas_info"
            text "DrawEasy 对象会创建 model 作为组件渲染的模型, 具体的 shader 配置则在 Info 中\n在绘制时会从 Info 对象中获取 Shader 所需的 uniform 参数应用到 model 上"


screen canvas_info:
    default circle_size = (300, 150)
    default circle_info = CircleInfo((150, 75), r=50, texture=canvas_texture)

    text "Info 和 Displayable" size 50 ypos 100 xpos 50

    line start_pos (0, 240) end_pos (1920, 240) texture canvas_texture
    rect rect_area (0, 0, 1920, 1080) texture canvas_texture.__copy__(blend=0.1, alpha=0.1)

    default tex0 = TextureInfo(canvas_image)
    default lin0 = LineInfo((0, 0), (10, 100), round=3, texture=tex0)
    default rec0 = RectInfo((0, 0, 100, 100), texture=tex0)

    fixed:
        xysize (1920, 1080 - 360)
        ypos 300

        vbox:
            spacing 30
            yalign 0.5
            xalign 0.5

            text "所谓 Info 其实就是把一些参数封装到了同一个类里, 方便我们重复调用"

            hbox:
                spacing 100
                vbox:
                    xsize 400
                    text "{size=25}我们可以直接传入参数来让组件自己生成 Info 对象"
                    rect:
                        rect_area (0, 0, 100, 100) 
                        xysize (100, 100)
                    
                vbox:
                    xsize 400
                    text "{size=25}我们也可以通过指定 Info 对象直接引用生成好的 Info"
                    rect info rec0 xysize (100, 100)
                    
                vbox:
                    xsize 400
                    text "{size=25}在 add 组件时为了方便, add 的第一个参数为 Info 时也可以被识别"
                    add DrawRect(rec0) xysize (100, 100)
            
            text "不同的组件有不同的 Info 数据, 分别为 LineInfo(直线), RectInfo(正方形), CircleInfo(圆形)\n此外这些 Info 内都包含有一个用来储存纹理的 TextureInfo\n这几个 Info 的相关内容可以见存根文件和对应的 sample screen"

            text "同时, 为了方便使用, 所有的 Info 对象都有 __copy__ 函数\n除了拷贝以外还允许接受新的参数直接应用到新的 Info 上, 例如下面的排线"

            fixed: 
                xsize 1600
                for i in range(50):
                    line info lin0.__copy__((i*30, 10), (i*30+90, 100))

screen canvas_texture_info:
    default rect_size = (400, 150)
    default rect_info = RectInfo((0, 0, *rect_size), round=30, texture=canvas_texture)
    

    text "TextureInfo 的相关参数" size 50 ypos 100 xpos 50

    line start_pos (0, 240) end_pos (1920, 240) texture canvas_texture

    fixed:
        xysize (1920, 1080 - 360)
        ypos 300
        add RectMap()

        vbox:
            spacing 30
            yalign 0.5
            xalign 0.5
            
            hbox:
                spacing 30
                text "alpha 参数将传入纹理与 Shader 的 alpha 通道乘算\n{size=20}右侧示例: 0.0 -> 0.4 -> 0.8" xysize (rect_size[0] + 100, rect_size[1]) yalign 0.5
                rect info rect_info.__copy__(texture=canvas_texture.__copy__(alpha=0.0)) xysize rect_size
                rect info rect_info.__copy__(texture=canvas_texture.__copy__(alpha=0.4)) xysize rect_size
                rect info rect_info.__copy__(texture=canvas_texture.__copy__(alpha=0.8)) xysize rect_size
            hbox:
                spacing 30
                text "blend 参数将传入纹理与 Shader 的 RGB 通道乘算\n{size=20}右侧示例: 0.2 -> 0.4 -> 0.8" xysize (rect_size[0] + 100, rect_size[1]) yalign 0.5
                rect info rect_info.__copy__(texture=canvas_texture.__copy__(blend=0.2)) xysize rect_size
                rect info rect_info.__copy__(texture=canvas_texture.__copy__(blend=0.4)) xysize rect_size
                rect info rect_info.__copy__(texture=canvas_texture.__copy__(blend=0.8)) xysize rect_size
            hbox:
                spacing 30
                text "val_pow 参数将传入纹理, 在计算矢量图像的权重作为乘方\n{size=20}右侧示例: 1.0 -> 0.1 -> 0.0" xysize (rect_size[0] + 100, rect_size[1]) yalign 0.5
                rect info rect_info.__copy__(texture=canvas_texture.__copy__(val_pow=1.0)) xysize rect_size
                rect info rect_info.__copy__(texture=canvas_texture.__copy__(val_pow=0.1)) xysize rect_size
                rect info rect_info.__copy__(texture=canvas_texture.__copy__(val_pow=0.0)) xysize rect_size
            hbox:
                spacing 30
                text "relative_coord 参数为 True 时将以屏幕坐标来计算纹理位置, 否则以组件位置计算纹理位置\n{size=20}右侧示例: True : False\n这个参数就是为何这套组件有一种蒙蔽感的来源" xysize (rect_size[0] + 100, rect_size[1]) yalign 0.5
                rect info rect_info.__copy__(texture=canvas_texture.__copy__()) xysize rect_size
                rect info rect_info.__copy__(texture=canvas_texture.__copy__(relative_coord=False)) xysize rect_size


screen canvas_line_info:
    default line_pos = ((25, 25), (325, 175))
    default line_size = (350, 200)
    default line_info = LineInfo(*line_pos, width=40, round=0, texture=canvas_texture)
    
    # add RectMap()

    text "LineInfo 的相关参数" size 50 ypos 100 xpos 50

    line start_pos (0, 240) end_pos (1920, 240) texture canvas_texture
    rect rect_area (0, 0, 1920, 1080) texture canvas_texture.__copy__(blend=0.1, alpha=0.1)


    fixed:
        xysize (1920, 1080 - 360)
        ypos 300

        vbox:
            spacing 30
            yalign 0.5
            xalign 0.5

            fixed:
                ysize line_size[1]
                xsize 1600
                text "start_pos, end_pos 对应了线条的起点和终点\n{size=20}右侧示例: \n((500, 50), (1500, 50))\n((500, 50), (500, 200))\n((500, 50), (1500, 200))" xysize (line_size[0] + 100, line_size[1]) yalign 0.5
                line info line_info.__copy__((500, 50), (1500, 50)) xysize (1500, 300)
                line info line_info.__copy__((500, 50), (500, 200)) xysize (1500, 300)
                line info line_info.__copy__((500, 50), (1500, 200)) xysize (1500, 300)

            hbox:
                spacing 30
                text "width 参数为线条的宽度\n{size=20}右侧示例: 10 -> 30 -> 50" xysize (line_size[0] + 100, line_size[1]) yalign 0.5
                line info line_info.__copy__(width=10) xysize line_size
                line info line_info.__copy__(width=30) xysize line_size
                line info line_info.__copy__(width=50) xysize line_size
            hbox:
                spacing 30
                text "round 参数为线条圆边的像素值\n{size=20}右侧示例: 10 -> 30 -> 50" xysize (line_size[0] + 100, line_size[1]) yalign 0.5
                line info line_info.__copy__(round=0) xysize line_size
                line info line_info.__copy__(round=10) xysize line_size
                line info line_info.__copy__(round=20) xysize line_size


screen canvas_rect_info:
    default rect_size = (350, 150)
    default rect_info = RectInfo((0, 0, *rect_size), texture=canvas_texture)

    text "LineInfo 的相关参数" size 50 ypos 100 xpos 50

    line start_pos (0, 240) end_pos (1920, 240) texture canvas_texture
    rect rect_area (0, 0, 1920, 1080) texture canvas_texture.__copy__(blend=0.1, alpha=0.1)


    fixed:
        xysize (1920, 1080 - 360)
        ypos 300

        vbox:
            spacing 30
            yalign 0.5
            xalign 0.5

            hbox:
                spacing 30
                text "rect_area 为矩形的位置与大小信息\n{size=20}右侧示例: \n(0, 0, 100, 100)\n(0, 0, 300, 100)\n(100, 0, 100, 100)" xysize (rect_size[0] + 100, rect_size[1]) yalign 0.5
                rect info rect_info.__copy__(rect_area=(0, 0, 100, 100)) xysize rect_size
                rect info rect_info.__copy__(rect_area=(0, 0, 300, 100)) xysize rect_size
                rect info rect_info.__copy__(rect_area=(100, 0, 100, 100)) xysize rect_size

            hbox:
                spacing 30
                text "round 为矩形圆边的像素值, 参数为0时不计算圆边\n{size=20}右侧示例: \n10 -> 30 -> 50" xysize (rect_size[0] + 100, rect_size[1]) yalign 0.5
                rect info rect_info.__copy__(round=10) xysize rect_size
                rect info rect_info.__copy__(round=30) xysize rect_size
                rect info rect_info.__copy__(round=50) xysize rect_size

            hbox:
                spacing 30
                text "width 为 0 时矩阵实心填充, 大于 0 时将按照 width 的值描边\n{size=20}右侧示例: \n5 -> 10 -> 20" xysize (rect_size[0] + 100, rect_size[1]) yalign 0.5
                rect info rect_info.__copy__(width=5) xysize rect_size
                rect info rect_info.__copy__(width=10) xysize rect_size
                rect info rect_info.__copy__(width=20) xysize rect_size
            hbox:
                spacing 30
                text "注意: 当 width 大于 round 时, 描边的值出现负数, 会错误的填充空白区域\n{size=20}右侧示例: \nround:30  width:10 -> 30 -> 50" xysize (rect_size[0] + 100, rect_size[1]) yalign 0.5
                rect info rect_info.__copy__(round=30, width=10) xysize rect_size
                rect info rect_info.__copy__(round=30, width=30) xysize rect_size
                rect info rect_info.__copy__(round=30, width=50) xysize rect_size


screen canvas_circle_info:
    default circle_size = (300, 150)
    default circle_info = CircleInfo((150, 75), r=50, texture=canvas_texture)

    text "CircleInfo 的相关参数" size 50 ypos 100 xpos 50

    line start_pos (0, 240) end_pos (1920, 240) texture canvas_texture
    rect rect_area (0, 0, 1920, 1080) texture canvas_texture.__copy__(blend=0.1, alpha=0.1)


    fixed:
        xysize (1920, 1080 - 360)
        ypos 300

        vbox:
            spacing 30
            yalign 0.5
            xalign 0.5

            fixed:
                ysize circle_size[1]
                xsize 1600
                text "pos 为圆的中心点, r 为圆的半径\n{size=20}右侧示例: \npos=(850, 75), r=20\npos=(1000, 175), r=100\npos=(1150, 50), r=30" xysize (circle_size[0] + 100, circle_size[1]) yalign 0.5
                circle info circle_info.__copy__(pos=(850, 75), r=20) xysize (1600, circle_size[1])
                circle info circle_info.__copy__(pos=(1000, 175), r=100) xysize (1600, circle_size[1])
                circle info circle_info.__copy__(pos=(1150, 50), r=30) xysize (1600, circle_size[1])


            hbox:
                spacing 30
                text "width 为 0 时圆将实心填充, 大于 0 时将按照 width 的值描边\n{size=20}右侧示例: \n5 -> 10 -> 20" xysize (circle_size[0] + 100, circle_size[1]) yalign 0.5
                circle info circle_info.__copy__(width=5) xysize circle_size
                circle info circle_info.__copy__(width=10) xysize circle_size
                circle info circle_info.__copy__(width=20) xysize circle_size
            hbox:
                spacing 30
                text "degree 参数的第一个数为偏移的弧度, 第二个参数为绘制的弧度\n{size=20}右侧示例: \n  (0, 1) -> (0, 3) -> (1, 3)" xysize (circle_size[0] + 100, circle_size[1]) yalign 0.5
                circle info circle_info.__copy__(degree=(0, 1)) xysize circle_size
                circle info circle_info.__copy__(degree=(0, 3)) xysize circle_size
                circle info circle_info.__copy__(degree=(1, 3)) xysize circle_size

            hbox:
                spacing 30
                text "在 degree, width 生效时, round 为圆边的像素值, 参数为0时不计算圆边\n{size=20}右侧示例: \n10 -> 30 -> 50" xysize (circle_size[0] + 100, circle_size[1]) yalign 0.5
                circle info circle_info.__copy__(degree=(1, 4), width=30, round=0) xysize circle_size
                circle info circle_info.__copy__(degree=(1, 4), width=30, round=10) xysize circle_size
                circle info circle_info.__copy__(degree=(1, 4), width=30, round=15) xysize circle_size


