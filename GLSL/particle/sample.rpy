
#  sample 相关的布局需要 split_layout (KojiRenpyBox\CDD\split_layout) 中的 split 组件进行布局, 记得导入

# 带粒子的消失组件
screen sample_particle_dust:
    add ParticleDust(Fixed(Frame("test5.jpg", align=(0.5, 0.5), xysize=(600, 300)), ), "tex1.png")

# 粒子效果
screen sample_particle_mask:  # 简易测试
    split:
        horizontal_nor_vertical False
        split:
            fixed:
                text "mask 为 tex0"
                add ParticleLayer("tex0.png", percent=0.8, mask_range=(0.2, 0.95), speed=0.3, center=(0.5, -3.0), vector_speed=(0.03, 0.1), vector_weight=(0.5, 2.0), color=(1.0, 1.0, 1.0, 0.0))
                add Transform("tex0.png", alpha = 0.5, crop=(0, 0, 300, 300), align=(0.9, 0.5))
            fixed:
                text "mask 为 tex1"
                add ParticleLayer("tex1.png", percent=0.8, mask_range=(0.0, 1.0), speed=0.3, center=(0.5, -3.0), vector_speed=(0.03, 0.1), vector_weight=(0.5, 2.0), color=(1.0, 1.0, 1.0, 0.0), delay=0.0, rand=114)
                add Transform("tex1.png", alpha = 0.5, crop=(0, 0, 300, 300), align=(0.9, 0.5))
        split:
            fixed:
                text "mask 为 tex2"
                add ParticleLayer("tex2.png", percent=0.5, mask_range=(0.3, 0.75), speed=0.3, center=(0.5, -3.0), vector_speed=(0.03, 0.1), vector_weight=(0.5, 2.0), color=(1.0, 1.0, 1.0, 0.0), delay=0.0, rand=191)
                add Transform("tex2.png", alpha = 0.5, crop=(0, 0, 300, 300), align=(0.9, 0.5))

            fixed:
                text "将调好参数的三个 mask 一起用"
                add ParticleLayer("tex0.png", percent=0.8, mask_range=(0.2, 0.95), speed=0.3, center=(0.5, -3.0), vector_speed=(0.03, 0.1), vector_weight=(0.5, 2.0), color=(1.0, 1.0, 1.0, 0.0))
                add ParticleLayer("tex1.png", percent=0.8, mask_range=(0.0, 1.0), speed=0.3, center=(0.5, -3.0), vector_speed=(0.03, 0.1), vector_weight=(0.5, 2.0), color=(1.0, 1.0, 1.0, 0.0), delay=0.0, rand=114)
                add ParticleLayer("tex2.png", percent=0.5, mask_range=(0.3, 0.75), speed=0.3, center=(0.5, -3.0), vector_speed=(0.03, 0.1), vector_weight=(0.5, 2.0), color=(1.0, 1.0, 1.0, 0.0), delay=0.0, rand=191)

    text "{alpha=0.70}{b}mask 参数为粒子的权重图\n{size=25}这张图片决定了粒子的分布, 大小等参数{/size}{/b}\n{size=20}实际上, 你看到的粒子飘动效果也就是形变了 mask 这张图片而已{/size}{/alpha}" align(0.1, 0.9)


screen sample_particle_center:  # 改变 Center 为左
    split:
        horizontal_nor_vertical False
        split:
            fixed:
                text "发射源位于中心 center = (0.5, 0.5)"
                add ParticleLayer("tex1.png", center=(0.5, 0.5))
            fixed:
                text "发射源位于正上方 center = (0.5, 0.0)"
                add ParticleLayer("tex1.png", center=(0.5, 0.0))
        split:
            fixed:
                text "发射源位于左侧 center = (0.0, 0.5)"
                add ParticleLayer("tex1.png", center=(0.0, 0.5))
            fixed:
                text "发射源位于左上角 center = (0.25, 0.25)"
                add ParticleLayer("tex1.png", center=(0.25, 0.25))

    text "{alpha=0.70}{b}center 参数为粒子计算步进矢量的中心点\n{size=25}center: tuple['[']float, float[']']{/size}{/b}\n{size=20}好长的名字, 叫发射源吧 ( ){/size}{/alpha}" align(0.1, 0.9)


screen sample_particle_mix:
    split:
        horizontal_nor_vertical False

        split:
            fixed:
                text "大粒子 (贴图: tex0.png)"
                add ParticleLayer("tex0.png", percent=0.8, mask_range=(0.2, 0.95), speed=0.3, center=(0.5, -3.0), vector_speed=(0.03, 0.1), vector_weight=(0.5, 2.0), color=(1.0, 1.0, 1.0, 0.0))
            
            fixed:
                text "中粒子 (贴图: tex1.png)"
                add ParticleLayer("tex1.png", percent=0.8, mask_range=(0.0, 1.00), speed=0.3, center=(0.5, -3.0), vector_speed=(0.03, 0.1), vector_weight=(0.5, 2.0), color=(1.0, 1.0, 1.0, 0.0), delay=0.0, rand=114)
            
        split:
            fixed:
                text "小粒子 (贴图: tex2.png)"
                add ParticleLayer("tex2.png", percent=0.9, mask_range=(0.0, 0.70), speed=0.3, center=(0.5, -3.0), vector_speed=(0.03, 0.1), vector_weight=(0.5, 2.0), color=(1.0, 1.0, 1.0, 0.0), delay=0.0, rand=191)
            
            fixed:
                text "组合效果"
                add ParticleLayer("tex0.png", percent=0.8, mask_range=(0.2, 0.95), speed=0.3, center=(0.5, -3.0), vector_speed=(0.03, 0.1), vector_weight=(0.5, 2.0), color=(1.0, 1.0, 1.0, 0.0))
                add ParticleLayer("tex1.png", percent=0.8, mask_range=(0.0, 1.00), speed=0.3, center=(0.5, -3.0), vector_speed=(0.03, 0.1), vector_weight=(0.5, 2.0), color=(1.0, 1.0, 1.0, 0.0), delay=0.0, rand=114)
                add ParticleLayer("tex2.png", percent=0.9, mask_range=(0.0, 0.70), speed=0.3, center=(0.5, -3.0), vector_speed=(0.03, 0.1), vector_weight=(0.5, 2.0), color=(1.0, 1.0, 1.0, 0.0), delay=0.0, rand=191)

    text "{alpha=0.70}{b}权重贴图中的 Red 通道 (红色通道) 决定了粒子的分布\n{size=25}为何不是按照 RGBA 通道的所有值?{/size}{/b}\n{size=20}因为要多写几个字, 摸了{/size}{/alpha}" align(0.1, 0.9)


screen sample_particle_percent:
    split:
        horizontal_nor_vertical False

        split:
            fixed:
                text "临界值为 0.8"
                add ParticleLayer("tex0.png", percent=0.8)
            
            fixed:
                text "临界值为 0.7"
                add ParticleLayer("tex0.png", percent=0.7)
            
        split:
            fixed:
                text "临界值为 0.6"
                add ParticleLayer("tex0.png", percent=0.6)
            
            fixed:
                text "临界值为 0.5"
                add ParticleLayer("tex0.png", percent=0.5)


    text "{alpha=0.70}{b}percent 参数为截取显示的权重临界\n{size=25}该值为一个 0.0~1.0 的数{/size}{/b}\n{size=20}相当于是 Blender 里颜色渐变节点的两个滑块中靠左的那个滑块的位置{/size}{/alpha}" align(0.1, 0.9)


screen sample_particle_mask_range:
    split:
        horizontal_nor_vertical False

        split:
            fixed:
                text "mask_range 为 (0.0, 1.0), percent 为 0.5"
                add ParticleLayer("tex2.png", percent=0.5)
            
            fixed:
                text "mask_range 为 (0.0, 1.0), percent 为 0.3"
                add ParticleLayer("tex2.png", percent=0.3)
            
        split:
            fixed:
                text "mask_range 为 (0.2, 0.8), percent 为 0.5"
                add ParticleLayer("tex2.png", percent=0.5, mask_range=(0.3, 0.7))
            
            fixed:
                text "mask_range 为 (0.2, 0.8), percent 为 0.3"
                add ParticleLayer("tex2.png", percent=0.3, mask_range=(0.3, 0.7))


    text "{alpha=0.70}{b}mask_range 参数会将权重在 mask_range 内的权重重新映射为 0.0~1.0\n{size=25}weight = (weight - mask_range[r'[0]']) / (mask_range[r'[1]'] - mask_range[r'[0]'] if (mask_range[r'[0]'] < weight < mask_range[r'[1]']) else weight > mask_range[r'[0]']{/size}{/b}\n{size=20}这个值是用来对一些 R 通道最大最小值达不到 1.0, 0.0 的图像做的兼容, 在最大最小值不匹配时就会出现上面闪烁的样子{/size}{/alpha}" align(0.1, 0.9)


screen sample_particle_vector_speed:
    split:
        horizontal_nor_vertical False

        split:
            fixed:
                text "vector_speed 为 (1.0, 1.0)"
                add ParticleLayer("tex0.png", vector_speed=(1.0, 1.0))
            
            fixed:
                text "vector_speed 为 (-1.0, 1.0)"
                add ParticleLayer("tex0.png", vector_speed=(-0.1, 1.0))
            
        split:
            fixed:
                text "vector_speed 为 (1.0, 5.0)"
                add ParticleLayer("tex0.png", vector_speed=(1.0, 5.0))
            
            fixed:
                text "vector_speed 为 (0.5, 0.3)"
                add ParticleLayer("tex0.png", vector_speed=(0.5, 0.3))


    text "{alpha=0.70}{b}vector_speed 参数会会影响粒子的运动速度\n{size=25}vector_speed[r'[0]']: 坐标差速度, vector_speed[r'[1]']: 位移函数速度{/size}{/b}\n{size=20}坐标差是点与发射源的坐标差, 位移函数就是一个三角函数, 用于让点伪随机移动A{/size}{/alpha}" align(0.1, 0.9)


screen sample_particle_vector_weight:
    split:
        horizontal_nor_vertical False

        split:
            fixed:
                text "vector_weight 为 (1.0, 1.0)"
                add ParticleLayer("tex0.png", vector_weight=(1.0, 1.0))
            
            fixed:
                text "vector_weight 为 (0.0, 1.0)"
                add ParticleLayer("tex0.png", vector_weight=(0.0, 1.0))
            
        split:
            fixed:
                text "vector_weight 为 (1.0, 0.0)"
                add ParticleLayer("tex0.png", vector_weight=(1.0, 0.0))
            
            fixed:
                text "vector_weight 为 (0.1, 10.0)"
                add ParticleLayer("tex0.png", vector_weight=(0.1, 10.0))


    text "{alpha=0.70}{b}vector_weight 参数会会影响粒子的运动的强度\n{size=25}vector_weight[r'[0]']: 坐标差强度, vector_weight[r'[1]']: 位移函数强度{/size}{/b}\n{size=20}不难发现其实坐标差的两个值等效于乘算到一起了, 不过分开也是为了以后能改写成其他东西做铺垫嘛{/size}{/alpha}" align(0.1, 0.9)


screen sample_particle_obj:
    split:
        horizontal_nor_vertical False

        split:
            fixed:
                text "此处没有传入 obj 参数, color 为默认的 (1.0, 0.9, 0.5, 0.0)"
                add ParticleLayer("tex1.png")
            
            fixed:
                text "此处没有传入 obj 参数, color 为 (1.0, 1.0, 1.0, 0.0)\n我们可以看到粒子还是挺干净的"
                add ParticleLayer("tex1.png", color=(1.0, 1.0, 1.0, 0.0))
            
        split:
            fixed:
                text "此处没有传入 obj 参数, color 为 (1.0, 1.0, 1.0, 1.0)\n观察这串字可以看到粒子边缘出现了黑边\n这与 shader 中 alpha 结算的算法有关"
                add ParticleLayer("tex1.png", color=(1.0, 1.0, 1.0, 1.0))
            
            fixed:
                text "传入 test5.jpg 作为 obj 参数, 粒子的颜色从 test5.jpg 中获得\n{size=20}虽然这里的演示根本不明显, 但它就是从那张纹理上采样的!{/size}"
                add ParticleLayer("tex1.png", "test5.jpg")


    text "{alpha=0.70}{b}obj 参数为粒子的着色纹理, 当没有给时粒子将以 color 参数渲染颜色\n{size=25}obj 参数为一个可视化组件, color 参数为一个包含四个 0.0~1.0 参数的元组{/size}{/b}\n{size=20}{b}注意: {/b}无论是 mask 还是 obj 参数, 他们最终渲染的大小均会被映射到正方形的 0-1 区间里, 再被拉伸到 ParticleLayer 的大小{/size}{/alpha}" align(0.1, 0.9)


# 消失效果
screen sample_dust_with_particle:
    split:
        horizontal_nor_vertical False

        split:
            fixed:
                add Frame("test5.jpg")
                text "原始图像"

            fixed:
                add DustLayer("test5.jpg", speed=0.3)
                text "消失效果"

        split:
            fixed:
                text "粒子层"
                add ParticleLayer("tex0.png", "test5.jpg", percent=0.8, mask_range=(0.2, 0.95),)
                add ParticleLayer("tex1.png", "test5.jpg", percent=0.8, mask_range=(0.0, 1.0),)
                add ParticleLayer("tex2.png", "test5.jpg", percent=0.4, mask_range=(0.3, 0.75),)


            fixed:
                add ParticleDust(Fixed(Frame("test5.jpg", xysize=(640, 360), align=(0.5, 0.5))), speed=0.3, lock=False)
                text "合在一起"


    text "{alpha=0.70}{b}这里是一个整合示例\n{size=25}将消失效果和粒子组合到一起做一个 Fadeout 的效果{/size}{/b}\n{size=20}但其实一开始就是要做这个效果, 最后搓出来一套粒子, 难崩{/size}{/alpha}" align(0.1, 0.9)
