# 单图样例
screen sample_perspective_single:
    add OnePointPerspective(
        Frame("single_test.jpg"), 
        mask_center = (0.4, 0.95),
        mask_area = (0.3, 0.52, 0.22, 0.68),
        addin=(
            ResetArgAddin(),
            AreaMouseTrackAddin(), 
            CenterMouseTrackAddin(), 
            IntensityAddin(),
            ScaleAreaAddin()
            )
        )
    text "此处是单个图片进行单点透视的样例" yalign 1.0


# 调试控件样例
screen sample_perspective_debug:
    # split 是分割线控件, 也是自己写的
    split:
        horizontal_nor_vertical False

        split:
            fixed:
                add PerspectivePreview(
                    Frame("single_test.jpg"),
                    center=(141 / (834 - 483), 0.95),
                    area = (0.3, 0.52, 0.22, 0.68)
                    )
                text "PerspectivePreview 组件\n此组件会在图片上根据 center, area 的值绘制出透视线" yalign 1.0

            fixed:
                add PerspectiveValMonitor(
                    PerspectivePreview(
                        Frame("single_test.jpg"),
                        center=(141 / (834 - 483), 0.95),
                        area=(0.3, 0.52, 0.22, 0.68)
                        )
                    )
                text "PerspectiveValMonitor 组件\n此组件可以通过条来调整 PerspectivePreview 的值达到快速调试的效果" yalign 1.0

        split:
            fixed:
                add PerspectiveValMonitor(OnePointPerspective(
                        Frame("single_test.jpg"), 
                        mask_center = (0.4, 0.95),
                        mask_area = (0.3, 0.52, 0.22, 0.68),
                        )
                    )
                text "同样是 PerspectiveValMonitor 组件\n此组件也可以通过条来调整 OnePointPerspective 的值达到快速调试的效果" yalign 1.0

            fixed:
                add PerspectiveValMonitor(OnePointPerspective(
                        Frame("single_test.jpg"), 
                        mask_center = (0.4, 0.95),
                        mask_area = (0.3, 0.52, 0.22, 0.68),
                        addin=(
                            ResetArgAddin(),
                            AreaMouseTrackAddin(), 
                            CenterMouseTrackAddin(), 
                            IntensityAddin(),
                            ScaleAreaAddin()
                            )
                        )

                    )
                text "同样是 PerspectiveValMonitor 组件\n由于此 OnePointPerspective 带有 Addin 动态调整参数, 无法通过条来调整动态变化的值\n但我们可以把它当成信息显示的工具" yalign 1.0


# 插件样例
screen sample_perspective_addin:
    split:
        horizontal_nor_vertical False

        split:
            frame:
                add PerspectiveValMonitor(OnePointPerspective(
                    Frame("single_test.jpg"), 
                    mask_center = (0.4, 0.95),
                    mask_area = (0.3, 0.52, 0.22, 0.68),
                    addin=(
                        ResetArgAddin(),
                        AreaMouseTrackAddin(),
                    )))
                text "AreaMouseTrackAddin\n此插件会根据鼠标位置改变 Area 的参数" yalign 1.0

            frame:
                add PerspectiveValMonitor(OnePointPerspective(
                    Frame("single_test.jpg"), 
                    mask_center = (0.4, 0.95),
                    mask_area = (0.3, 0.52, 0.22, 0.68),
                    addin=(
                        ResetArgAddin(),
                        CenterMouseTrackAddin(), 
                    )))
                text "CenterMouseTrackAddin\n此插件会根据鼠标位置改变 Center 的参数" yalign 1.0

        split:
            frame:
                add PerspectiveValMonitor(OnePointPerspective(
                    Frame("single_test.jpg"), 
                    mask_center = (0.4, 0.95),
                    mask_area = (0.3, 0.52, 0.22, 0.68),
                    addin=(
                        ResetArgAddin(),
                        IntensityAddin()
                    )))
                text "IntensityAddin\n此插件会相应鼠标滚轮改变 Intensity 的参数" yalign 1.0

            frame:
                add PerspectiveValMonitor(OnePointPerspective(
                    Frame("single_test.jpg"), 
                    mask_center = (0.4, 0.95),
                    mask_area = (0.3, 0.52, 0.22, 0.68),
                    addin=(
                        ResetArgAddin(),
                        ScaleAreaAddin()
                    )))
                text "ScaleAreaAddin\n此插件会相应鼠标滚轮改变 Area 的参数" yalign 1.0


# 多图样例
screen sample_perspective_mix:
    # 背景图层
    add OnePointPerspective(
        "script/2_dialog/GLSL_Perspective/bg.png",
        (0.45, 0.47), 
        (0.24, 0.85, 0.275, 0.75),
        addin=(
                ResetArgAddin(),
                AreaMouseTrackAddin(area=(0.4, 0.4, 0.4, 0.4), catch_fullscreen=True), 
                CenterMouseTrackAddin(catch_fullscreen=False), 
                IntensityAddin(limit=(0.1, 1.0)),
                ScaleAreaAddin()
                ),
        )

    # 头顶的图层
    add OnePointPerspective(
        "script/2_dialog/GLSL_Perspective/ahead.png",
        (0.485, 0.362), 
        (0.482, 0.549, 0.483, 0.526),
        addin=(
                ResetArgAddin(),
                AreaMouseTrackAddin((0.4, 0.4, 0.6, 0.6), catch_fullscreen=True, mode=3), 
                CenterMouseTrackAddin((0.1, 1.0), catch_fullscreen=False), 
                IntensityAddin(),
                ScaleAreaAddin(0.025)),
        ignore_area=(True, True, False, True),
        ignore_center=True,
        )

    # 左侧桌椅
    add OnePointPerspective(
        "script/2_dialog/GLSL_Perspective/ahead_1.png",
        (0.07, 0.36), 
        (0.504, 0.619, 0.412, 0.652),
        addin=(
                ResetArgAddin(),
                AreaMouseTrackAddin(area=((-0.4, 0.4), (-0.4, 0.4), (-0.5, 0.5), (-0.4, 0.4)), catch_fullscreen=True), 
                CenterMouseTrackAddin(center=((1.0, 2.0), (1.0, 1.0)), catch_fullscreen=False, mode=1), 
                IntensityAddin(),
                ScaleAreaAddin(0.05)),
        ignore_area=(False, True, True, True),
        ignore_center=True,
        )

    # 右侧桌椅
    add OnePointPerspective(
        "script/2_dialog/GLSL_Perspective/ahead_2.png",
        (0.899, 0.36),
        (0.347, 0.51, 0.428, 0.624),
        addin=(
                ResetArgAddin(),
                AreaMouseTrackAddin(area=((-0.4, 0.4), (-0.4, 0.4), (-0.5, 0.5), (-0.4, 0.4)), catch_fullscreen=True), 
                CenterMouseTrackAddin(center=((0.9, 1.0), (1.0, 1.0)), catch_fullscreen=False, mode=1), 
                IntensityAddin(),
                ScaleAreaAddin(0.05)),
        ignore_area=(True, False, True, True),
        ignore_center=True,
        ) xpos 40
