default aaa = (0.0, 0.0, 0.0, 0.0)

screen cloud_node_color:
    split:
        event_limit False
        horizontal_nor_vertical False
        split:
            event_limit False
            fixed:
                text "color 为 (1.0, 1.0, 1.0, 0.0)" align (0.02, 0.03)
                add CloudNode(color=(1.0, 1.0, 1.0, 0.0), node_add_speed=30)
            fixed:
                text "color 为 (1.0, 1.0, 1.0, 1.0)" align (0.02, 0.03)
                add CloudNode(color=(1.0, 1.0, 1.0, 1.0), node_add_speed=30)
        split:
            event_limit False
            fixed:
                text "color 为 (10, 10, 10, 0.0)" align (0.02, 0.03)
                add CloudNode(color=(10, 10, 10, 10), node_add_speed=30)

            fixed:
                text "color 为 (0.0, 0.6, 1.0, 0.0)" align (0.02, 0.03)
                add CloudNode(color=(0.0, 0.8, 1.0, 0.0), node_add_speed=30)

    text "{alpha=0.70}{b}color 参数为点云的颜色\n{size=25}还是老样子的 (0~1) 的四个参数, 对应了 RGB 通道{/size}{/b}\n{size=20}按区域设置颜色或者渐变色什么的自己写啦, 不难的{/size}{/alpha}" align(0.1, 0.9)


screen cloud_node_node_dead_time:
    split:
        event_limit False
        horizontal_nor_vertical False
        split:
            event_limit False
            fixed:
                text "node_dead_time 为 1.0" align (0.02, 0.03)
                add CloudNode(node_dead_time=1.0, node_add_speed=30)
            fixed:
                text "node_dead_time 为 3.0" align (0.02, 0.03)
                add CloudNode(node_dead_time=3.0, node_add_speed=30)
        split:
            event_limit False
            fixed:
                text "node_dead_time 为 5.0" align (0.02, 0.03)
                add CloudNode(node_dead_time=5, node_add_speed=30)

            fixed:
                text "node_dead_time 为 10.0" align (0.02, 0.03)
                add CloudNode(node_dead_time=10, node_add_speed=30)

    text "{alpha=0.70}{b}node_dead_time 参数为点消失的时间\n{size=25}这个值会直接影响到点的数量, 谨慎一点{/size}{/b}\n{size=20}另外, 点的渐入渐出写死在 update_node 函数里了, 可以自己改{/size}{/alpha}" align(0.1, 0.9)


screen cloud_node_node_add_speed:
    split:
        event_limit False
        horizontal_nor_vertical False
        split:
            event_limit False
            fixed:
                text "node_add_speed 为 1.0" align (0.02, 0.03)
                add CloudNode(node_add_speed=10, mouse_k=3)
            fixed:
                text "node_add_speed 为 0.2" align (0.02, 0.03)
                add CloudNode(node_add_speed=30, mouse_k=3)
        split:
            event_limit False
            fixed:
                text "node_add_speed 为 0.03" align (0.02, 0.03)
                add CloudNode(node_add_speed=60, mouse_k=3)

            fixed:
                text "node_add_speed 为 0.0" align (0.02, 0.03)
                add CloudNode(node_add_speed=100, mouse_k=3)

    text "{alpha=0.70}{b}node_add_speed 参数为每秒生成点的数量\n{size=25}参数为浮点, 默认 60.0 (也就是每秒60个){/size}{/b}\n{size=20}话说我为什么不命名成 node_addin_per_second 呢 ({/size}{/alpha}" align(0.1, 0.9)



screen cloud_node_link_length:
    split:
        event_limit False
        horizontal_nor_vertical False
        split:
            event_limit False
            fixed:
                text "link_length 为 0.03" align (0.02, 0.03)
                add CloudNode(link_length=0.03, node_add_speed=30)
            fixed:
                text "link_length 为 0.1" align (0.02, 0.03)
                add CloudNode(link_length=0.1, node_add_speed=30)
        split:
            event_limit False
            fixed:
                text "link_length 为 0.15" align (0.02, 0.03)
                add CloudNode(link_length=0.15, node_add_speed=30)

            fixed:
                text "link_length 为 0.2" align (0.02, 0.03)
                add CloudNode(link_length=0.2, node_add_speed=30)

    text "{alpha=0.70}{b}link_length 参数为边连接的长度\n{size=25}虽然是 0.0~1.0 的值, 但不传入 Shader 计算, 而是在外部结算{/size}{/b}\n{size=20}数量越大单个点可连接的距离就最大{/size}{/alpha}" align(0.1, 0.9)


screen cloud_node_line_width:
    split:
        event_limit False
        horizontal_nor_vertical False
        split:
            event_limit False
            fixed:
                text "line_width 为 0.2" align (0.02, 0.03)
                add CloudNode(line_width=0.2, node_add_speed=30)
            fixed:
                text "line_width 为 0.4" align (0.02, 0.03)
                add CloudNode(line_width=0.4, node_add_speed=30)
        split:
            event_limit False
            fixed:
                text "line_width 为 0.6" align (0.02, 0.03)
                add CloudNode(line_width=0.6, node_add_speed=30)

            fixed:
                text "line_width 为 0.8" align (0.02, 0.03)
                add CloudNode(line_width=0.8, node_add_speed=30)

    text "{alpha=0.70}{b}line_width 参数为连接线的粗细\n{size=25}传入一个浮点数, 不过也是很小的 ( 默认 0.1 ){/size}{/b}\n{size=20}这个倒是传入 Shader 结算了{/size}{/alpha}" align(0.1, 0.9)


screen cloud_node_node_size:
    split:
        event_limit False
        horizontal_nor_vertical False
        split:
            event_limit False
            fixed:
                text "node_size 为 (3, 3)" align (0.02, 0.03)
                add CloudNode(node_size=(3, 3), node_add_speed=30)
            fixed:
                text "node_size 为 (5, 5)" align (0.02, 0.03)
                add CloudNode(node_size=(5, 5), node_add_speed=30)
        split:
            event_limit False
            fixed:
                text "node_size 为 (10, 10)" align (0.02, 0.03)
                add CloudNode(node_size=(10, 10), node_add_speed=30)

            fixed:
                text "node_size 为 (10, 3)" align (0.02, 0.03)
                add CloudNode(node_size=(10, 3), node_add_speed=30)

    text "{alpha=0.70}{b}node_size 参数为点的大小\n{size=25}这个参数倒是在外部结算了, 传入的是点的大小 (单位像素){/size}{/b}\n{size=20}这个写法是为了传入 render_node 函数, 这个函数可以自定义{/size}{/alpha}" align(0.1, 0.9)


screen cloud_node_mouse_r:
    split:
        event_limit False
        horizontal_nor_vertical False
        split:
            event_limit False
            fixed:
                text "mouse_r 为 0.1, mouse_R 为 0.2" align (0.02, 0.03)
                add CloudNode(mouse_r=0.1, mouse_R=0.2, node_add_speed=30)
            fixed:
                text "mouse_r 为 0.03, mouse_R 为 0.2" align (0.02, 0.03)
                add CloudNode(mouse_r=0.03, mouse_R=0.2, node_add_speed=30)
        split:
            event_limit False
            fixed:
                text "mouse_r 为 0.1, mouse_R 为 0.4" align (0.02, 0.03)
                add CloudNode(mouse_r=0.1, mouse_R=0.4, node_add_speed=30)

            fixed:
                text "mouse_r 为 0.03, mouse_R 为 0.4" align (0.02, 0.03)
                add CloudNode(mouse_r=0.03, mouse_R=0.4, node_add_speed=30)

    text "{alpha=0.70}{b}mouse_r 参数为鼠标吸附的停靠半径, mouse_R 为 鼠标吸附的半径\n{size=25}为了让顶点分散一些, 所以弄了两个参数来做区别{/size}{/b}\n{size=20}至于为什么草草的用大R小r, 当然是懒啦 ( ){/size}{/alpha}" align(0.1, 0.9)


screen cloud_node_mouse_w:
    split:
        event_limit False
        horizontal_nor_vertical False
        split:
            event_limit False
            fixed:
                text "mouse_w 为 5.0" align (0.02, 0.03)
                add CloudNode(mouse_w=5.0, node_add_speed=30)
            fixed:
                text "mouse_w 为 1.0" align (0.02, 0.03)
                add CloudNode(mouse_w=1.0, node_add_speed=30)
        split:
            event_limit False
            fixed:
                text "mouse_w 为 0.0" align (0.02, 0.03)
                add CloudNode(mouse_w=0.0, node_add_speed=30)

            fixed:
                text "mouse_w 为 None" align (0.02, 0.03)
                add CloudNode(mouse_w=None, node_add_speed=30)

    text "{alpha=0.70}{b}mouse_w 参数为在鼠标范围内点运动的强度\n{size=25}参数为浮点, 默认值为 1.0, 设置为 None 时不计算鼠标影响{/size}{/b}\n{size=20}这个参数为 0.0 时受影响的顶点将停止移动, 但是计算仍然是会进行的{/size}{/alpha}" align(0.1, 0.9)


screen cloud_node_mouse_k:
    split:
        event_limit False
        horizontal_nor_vertical False
        split:
            event_limit False
            fixed:
                text "mouse_k 为 5.0" align (0.02, 0.03)
                add CloudNode(mouse_k=5.0, node_add_speed=30)
            fixed:
                text "mouse_k 为 1.0" align (0.02, 0.03)
                add CloudNode(mouse_k=1.0, node_add_speed=30)
        split:
            event_limit False
            fixed:
                text "mouse_k 为 0.0" align (0.02, 0.03)
                add CloudNode(mouse_k=0.0, node_add_speed=30)

            fixed:
                text "mouse_k 为 -10.0 (算是 bug 玩法)" align (0.02, 0.03)
                add CloudNode(mouse_k=-10.0, node_add_speed=30)

    text "{alpha=0.70}{b}mouse_k 参数为鼠标吸附效果的强度\n{size=25}参数为浮点, 默认为 1.0, {/size}{/b}\n{size=20}这个值是通过直接修改点原本的向量实现的, 与 mouse_k, mouse_f 结算{/size}{/alpha}" align(0.1, 0.9)


screen cloud_node_mouse_f:
    split:
        event_limit False
        horizontal_nor_vertical False
        split:
            event_limit False
            fixed:
                text "mouse_f 为 1.0" align (0.02, 0.03)
                add CloudNode(mouse_f=1.0, node_add_speed=30, mouse_k=3)
            fixed:
                text "mouse_f 为 0.2" align (0.02, 0.03)
                add CloudNode(mouse_f=0.2, node_add_speed=30, mouse_k=3)
        split:
            event_limit False
            fixed:
                text "mouse_f 为 0.03" align (0.02, 0.03)
                add CloudNode(mouse_f=0.03, node_add_speed=30, mouse_k=3)

            fixed:
                text "mouse_f 为 0.0" align (0.02, 0.03)
                add CloudNode(mouse_f=0.0, node_add_speed=30, mouse_k=3)

    text "{alpha=0.70}{b}mouse_f 参数为惯性对点影响的强度\n{size=25}应该是一个范围为 0.0~1.0 的浮点, 默认为 0.25{/size}{/b}\n{size=20}这里也调高了 mouse_k 的参数来让效果更明显一些{/size}{/alpha}" align(0.1, 0.9)

