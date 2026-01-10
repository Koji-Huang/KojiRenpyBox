# 图片
default trailing_glitch_image = Frame("bg.png")


screen trailing_glitch_sample:
    add trailing_glitch_image:
        at transform:
            trailing_glitch(0.5, 0.5, 0.0)

            # 持续刷新确保画面更新
            block:
                xpos 0
                ease 0.1 xpos 1
                repeat


screen trailing_glitch_weight:
    add trailing_glitch_image:
        at transform:
            trailing_glitch(0.5, 0.5, 0.0)

            # 持续刷新确保画面更新
            block:
                u_weight 0.0
                ease 0.5 u_weight 1.0
                ease 0.5 u_weight 0.0
                repeat


screen trailing_glitch_color_weight:
    add trailing_glitch_image:
        at transform:
            trailing_glitch(0.5, 0.5, 0.0)

            # 持续刷新确保画面更新
            block:
                u_color_weight 0.0
                ease 0.5 u_color_weight 1.0
                ease 0.5 u_color_weight 0.0
                repeat


init python:
    from math import sin, cos

    # 出于优化的考虑角度的值在外面计算好了再传入
    # 但由于三角函数不是线性的变换所以得借助函数来传参
    # 虽然使用 warpper 也许可以得到类似的效果, 但还是没必要了

    def change_angle(trans, st, at):
        trans.u_angle = (sin(st), cos(at))
        return 0


screen trailing_glitch_angle:
    add trailing_glitch_image:
        at transform:
            trailing_glitch(0.5, 0.5, 0.0)
            function change_angle
