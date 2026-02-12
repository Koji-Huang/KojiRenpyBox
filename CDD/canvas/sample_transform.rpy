


transform line_animation_transform:
    LineTransform()
    
    parallel:
        u_start_pos (1910, 10)
        ease 6 u_start_pos (10, 10)
        ease 6 u_start_pos (1910, 10)
        repeat
    parallel:
        u_end_pos (10, 1070)
        ease 8 u_end_pos (1910, 1070)
        ease 8 u_end_pos (10, 1070)
        repeat
    parallel:
        u_width 0
        ease 1.5 u_width 100
        ease 1.5 u_width 0
        repeat
    parallel:
        u_round 0
        ease 1.1 u_round 100
        ease 1.1 u_round 0
        repeat

transform rect_animation_transform:
    RectTransform()
    parallel:
        ease 3 u_pos (1920/3.0, 1080/3.0)
        ease 3 u_pos (1920/3.0*2, 1080/3.0*2)
        repeat
    parallel:
        ease 2.4 u_size (100, 30)
        ease 2.4 u_size (30, 100)
        repeat
    parallel:
        ease 1.5 u_width 5
        ease 1.5 u_width 2
        repeat
    parallel:
        ease 1.2 u_round 10
        ease 1.2 u_round 5
        repeat

# 制作动画
transform circle_animation_transform(info=default_circle_info):
    CircleTransform(info)
    u_width 20
    u_r 100
    u_pos (1920/2., 1080/2.)
    u_round 10

    parallel:
        u_offset 0
        linear 1.5 u_offset 3.1415926*2
        repeat
    parallel:
        u_radius 1
        ease 3 u_radius 6
        ease 3 u_radius 1
        repeat

    