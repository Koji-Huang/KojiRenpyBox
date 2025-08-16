# [canvas (圆, 长方形, 直线)](./canvas)

<img src=".\sample_capture\canvas.png" height="150" align="right" />

   纯 Shader 实现的画直线, 长方形, 圆形的三个组件, 拥有圆角效果

- canvas_data_ren 为抽象数据类型文件
- canvas_shader_ren 为注册 shader 文件
- canvas_ren 为组织 CDD 的文件

注意: [sample](./CDD/canvas/sample.rpy) 中的 screen canvas_texture_info 需要 rect_map 组件来生成带有对比度的背景, 如果不需要的话可以注释掉 `add RectMap()` 这句话或者把 rect_map 组件加进去

   演示视频: https://www.bilibili.com/video/BV1Ri7kzzERC/

<br></br>

# [dammu (弹幕组件)](./dammu)

<img src=".\sample_capture\dammu.png" height="150" align="right" />

   非常简易的弹幕组件, dammu_ren.py 就是这个组件的所有内容

   sample 里实现了右侧图片的样式

<br></br>
<br></br>

# [press_buttom (按下效果)](./press_button)

   在 Imagebutton 的基础上加上了一个自定义的 press 属性用来相应鼠标按下的图片

   Base on Imagebuttton, added a custom 'press' attribute to correspond pressed by the mouse

   此组件的描述链接: https://www.renpy.cn/forum.php?mod=viewthread&tid=1605

<br></br>
<br></br>

# [split_layout (分割线布局)](./split_layout)

<img src=".\sample_capture\split_layout.png" height="150" align="right" />

   分割线容器, 此组件允许接收两个子组件并用分割线隔开, 此分割线可以自由调整

   Split line container, this component allows receiving two sub components and separating them with a split line, which can be freely adjusted

<br></br>
<br></br>

# [stela_button (简单的带效果按钮)](./stela_button)

   一个动画效果的 Textbutton 按钮, 并不是什么很厉害的组件

<br></br>
<br></br>