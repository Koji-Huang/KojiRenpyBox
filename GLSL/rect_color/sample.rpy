screen sample_rect_color:
    # 注意, 这里添加了 RectMap, 如果没载入此组件的话会报错
    # 虽然我们可以直接删掉这行语句来执行代码, 但是我希望能让颜色的对比更加明显可见, 所以加上了这个组件 ( 实际上 RectMap 本身也是为了 RectColor 写的 )
    add RectMap()

    grid 2 4:
        add RectColor() size(960, 270)
        add RectColor("#fff", "#fff0", "#fff", "#fff0") size(960, 270)

        add RectColor("#fff", "#fff", "#fff0", "#fff0", ) size(960, 270)
        add RectColor("#fff", "#fff", "#0000", "#0000", ) size(960, 270)

        add RectColor("#27f8ff", "#2986ff", "#27f8ff00", "#2986ff00", ) size(960, 270)
        add RectColor("#27f8ff", "#2986ff", "#fff", "#fff", ) size(960, 270)

        add RectColor("#f00", "#ff0", "#0f0", "#000") size(960, 270)
        add RectColor("#000", "#0f0", "#f00", "#ff0") size(960, 270)