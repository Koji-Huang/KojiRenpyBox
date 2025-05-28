
#  sample 相关的布局需要 split_layout (KojiRenpyBox\CDD\split_layout) 中的 split 组件进行布局, 记得导入

# 此处为图片存放的路径
default fp_uv = "uv_frame"

default fp_uv_image = fp_uv + "test1.png"
default fp_uv_sample_1 = fp_uv + "uv_sample_1.png"
default fp_uv_sample_2 = fp_uv + "uv_sample_2.png"
default fp_uv_sample_3 = fp_uv + "uv_sample_3.png"
default fp_uv_sample_4 = fp_uv + "uv_sample_4.png"
default fp_uv_sample_basic = fp_uv + "uv_sample_basic.png"


# Anima 相关的 uv 我保存有 Blender 文件于目录下, 可以自行渲染
# 或从下面的蓝奏云链接下载 ( 没买有会员, 不知道什么时候会寄 )

# uv_frame
# https://koji233.lanzouu.com/b00uz6jhkj
# 密码:6le8
default fp_uv_frame = tuple(fp_uv + "uv_frame/0%s%s%d.png" % ("" if i>99 else "0", "" if i>9 else "0", i) for i in range(0, 112))

# uv_frame_2
# https://koji233.lanzouu.com/ig9Yq2xe15yf
default fp_uv_frame_2 = tuple(fp_uv + "uv_frame_2/00%s%d.png" % ("" if i>9 else "0", i) for i in range(0, 61))



screen sample_uv_frame:
    split:
        event_limit False
        horizontal_nor_vertical False
        split:
            event_limit False
            fixed:
                add SingleUV_Frame(fp_uv_image, fp_uv_sample_1, render_image_size=False, only_uv=True) align(0.5, 0.5)
                text "sample_1 - UV 贴图" align (0.02, 0.03)
            fixed:
                add SingleUV_Frame(fp_uv_image, fp_uv_sample_1, render_image_size=False) align(0.5, 0.5)
                text "sample_1 - 显示效果" align (0.02, 0.03)
        split:
            event_limit False
            fixed:
                add SingleUV_Frame(fp_uv_image, fp_uv_sample_2, render_image_size=False, only_uv=True) align(0.5, 0.5)
                text "sample_2 - UV 贴图" align (0.02, 0.03)
            fixed:
                add SingleUV_Frame(fp_uv_image, fp_uv_sample_2, render_image_size=False) align(0.5, 0.5)
                text "sample_2 - 显示效果" align (0.02, 0.03)

    text "{alpha=0.70}{b}技术原理就是通过预生成好的 UV 来重新映射纹理位置\n{size=25}UV 图像的具体原理解释起来太久, 文件夹下我存有一张以 Renpy 为标准的 UV 贴图{/size}{/b}\n{size=20}通过形变 UV 贴图就可以形变图片的显示{/size}{/alpha}" align(0.1, 0.9)


screen sample_uv_frame_animation:
    split:
        event_limit False
        horizontal_nor_vertical False
        split:
            event_limit False
            fixed:
                add AnimaUV_Frame(fp_uv_image, fp_uv_frame, anima_loop_time=2.0, render_image_size=False, only_uv=True) align(0.5, 0.5)
                text "AnimaUV_Frame - UV 贴图" align (0.02, 0.03)

            fixed:
                add AnimaUV_Frame(fp_uv_image, fp_uv_frame, anima_loop_time=2.0, render_image_size=False) align(0.5, 0.5)
                text "AnimaUV_Frame - 显示效果" align (0.02, 0.03)

        split:
            event_limit False
            fixed:
                add AnimaUV_Frame(fp_uv_image, fp_uv_frame_2, anima_loop_time=2.0, render_image_size=False, only_uv=True) align(0.5, 0.5)
                text "AnimaUV_Frame - UV 贴图" align (0.02, 0.03)

            fixed:
                add AnimaUV_Frame(fp_uv_image, fp_uv_frame_2, anima_loop_time=2.0, render_image_size=False) align(0.5, 0.5)
                text "AnimaUV_Frame - 显示效果" align (0.02, 0.03)

    text "{alpha=0.70}{b}AnimaUV_Frame 组件可以传入多个 uv 图像来达到动画的效果\n{size=25}anima_loop_time 参数可以设置一轮动画的时间{/size}{/b}\n{size=20}这些动态的图片可以使用 AE, PR 甚至是 Blender 制作{/size}{/alpha}" align(0.1, 0.9)



screen sample_uv_frame_sample_level:
    style_prefix "sample_uv"
    default level = 6
    split:
        event_limit False
        add renpy.displayable(fp_uv_image) yalign 0.5

        fixed:
            add SingleUV_Frame(fp_uv_image, fp_uv_sample_basic, sample_level=level) yalign 0.5
            text "sample_level 为 %d" % level color "fff" align (0.98, 0.03)

    text r"""
{alpha=0.70}{b}sample_level 参数为 uv 贴图采样的算法
{size=25}['[']0, 1)时表示无修正, ['[']1, 2)&['[']2, 3)为固定点采样( 5 & 9 个采样点 ), ['[']3, 4)...['[']6, 7)为圆周采样, 
层数为 10x2, 20x2, 20x3, 30x3 个采样点(圆分割数x向内步进数), 默认为 3.0 ( 10x2 ) 采样{/size}{/b}
{size=20}通过渲染好的图片来获取UV是有损的, 所以需要采样算法修正这个问题,
另外, Renpy 的 Shader 无法传入整型, 所以只能给一个浮点表示层级了 (在shader里会转换成 int 的, 不用担心 case 犯傻){/size}{/alpha}""" align(0.1, 0.9)


screen sample_uv_frame_sample_dis:
    style_prefix "sample_uv"
    
    split:
        event_limit False
        horizontal_nor_vertical False
        split:
            event_limit False
            fixed:
                add SingleUV_Frame(fp_uv_image, fp_uv_sample_basic, render_image_size=False, sample_dis=0.0001)
                text "sample_dis 为 0.0001" align (0.02, 0.03)
            fixed:
                add SingleUV_Frame(fp_uv_image, fp_uv_sample_basic, render_image_size=False, sample_dis=0.001)
                text "sample_dis 为 0.001" align (0.02, 0.03)
        split:
            event_limit False
            fixed:
                add SingleUV_Frame(fp_uv_image, fp_uv_sample_basic, render_image_size=False, sample_dis=0.005)
                text "sample_dis 为 0.005" align (0.02, 0.03)
            fixed:
                add SingleUV_Frame(fp_uv_image, fp_uv_sample_basic, render_image_size=False, sample_dis=0.01)
                text "sample_dis 为 0.01" align (0.02, 0.03)

    text "{alpha=0.70}{b}sample_dis 参数为 uv 贴图采样的距离参数\n{size=25}这个参数会影响到 uv 采样的效果{/size}{/b}\n{size=20}距离短时图片的噪点会非常明显, 长时会让UV过渡混合{/size}{/alpha}" align(0.1, 0.9)



screen sample_uv_frame_alpha_pow:
    style_prefix "sample_uv"
    default kwrgs = {"image": fp_uv_image, "uv": fp_uv_sample_4, "sample_level": 6, "sample_dis": 0.005, "render_image_size": False}
    
    split:
        event_limit False
        horizontal_nor_vertical False
        split:
            event_limit False
            fixed:
                add Frame(fp_uv_sample_4)
                text "uv 贴图原样" align (0.02, 0.03)
            fixed:
                add SingleUV_Frame(**kwrgs)
                text "blend_alpha 为 False" align (0.02, 0.03)
        split:
            event_limit False
            fixed:
                add SingleUV_Frame(**kwrgs, blend_alpha=True, alpha_pow=1)
                text "blend_alpha 为 True, alpha_pow 为 1" align (0.02, 0.03)

            fixed:
                add SingleUV_Frame(**kwrgs, blend_alpha=True, alpha_pow=5)
                text "blend_alpha 为 True, alpha_pow 为 5" align (0.02, 0.03)

    text "{alpha=0.70}{b}blend_alpha 参数为 True 时, 会使用采样后的 alpha 作为图片的 alpha\n{size=25}alpha_pow 参数为对透明区域进行乘方的值 ( 一般是 blend_alpha 为 True 时用 ){/size}{/b}\n{size=20}blend_alpha 默认为 False, alpha_pow 默认为 1{/size}{/alpha}" align(0.1, 0.9)


screen sample_uv_frame_other:
    add SingleUV_Frame(fp_uv_image, fp_uv_sample_3, render_image_size=False) align (0.5, 0.5)
    vbox:
        align (0.5, 0.25)
        spacing 10
        text "load_cache 参数: \n    默认为 True\n    会在载入图像时强制渲染一次 model 来确保 texture 传入了组件, 这样可以保证动画播放时流畅\n    但相对的, 在载入 Anima 时, 这个组件的启动时间是非常久的 ( 堪比鸡煲" align (0.02, 0.03)
        text "render_image_size 参数: \n    默认为 True\n    会按照图片本身的大小渲染组件"
        text "anisotropic 参数: \n    默认为 True\n    是否使用过采样渲染图片 ( 默认为 True )"
        text "only_uv 参数: \n    默认为 False\n    开启后仅显示计算后的 uv 贴图"

    text "{alpha=0.70}{b}一些其他参数\n{/b}{/alpha}" align(0.1, 0.9)


style sample_uv_text:
    color "046"