# Koji Renpy Box

---

科基的个人 Renpy 组件仓库, 希望里面的组件能对你的开发提供一些帮助什么的, 对这些组件的使用有疑问或者希望我帮你写组件可以发邮件至 koji233@163.com

Bilibili 账号: https://space.bilibili.com/1146352855

视频合集: https://space.bilibili.com/1146352855/lists/5362589?type=season

Koji's Renpy Widget Repositories. Hope these widget can give you some help, if there is some question or wish I write widget for you, send email to koji233@163.com

Bilibili Account: https://space.bilibili.com/1146352855

Video Collection: https://space.bilibili.com/1146352855/lists/5362589?type=season

---

[TOC]

---

## CDD

### 1. [canvas (圆, 长方形, 直线)](./CDD/canvas)

>   纯 Shader 实现的画直线, 长方形, 圆形的三个组件, 拥有圆角效果
>
>   canvas_data_ren 为抽象数据类型文件
>
>   canvas_shader_ren 为注册 shader 文件
>
>   canvas_ren 为组织 CDD 的文件
>
>   注意: [sample](.\CDD\canvas\sample.rpy) 中的 screen canvas_texture_info 需要 [rect_map](.\GLSL\rect_map) 组件来生成带有对比度的背景, 如果不需要的话可以注释掉 `add RectMap()` 这句话或者把 rect_map 组件加进去
>
>   演示视频: https://www.bilibili.com/video/BV1Ri7kzzERC/
>
>   <img src=".\sample_capture\canvas.png" style="zoom: 30%;" />

### 2. [dammu (弹幕组件)](.\CDD\dammu)

>   非常简易的弹幕组件, dammu_ren.py 就是这个组件的所有内容, sample 里实现了以下图片的样式
>
>   <img src=".\sample_capture\dammu.png" style="zoom:50%;" />

### 3. [press_buttom (按下效果)](.\CDD\press_button)

>   在 Imagebutton 的基础上加上了一个自定义的 press 属性用来相应鼠标按下的图片
>
>   Base on Imagebuttton, added a custom 'press' attribute to correspond pressed by the mouse
>
>   此组件的描述链接: https://www.renpy.cn/forum.php?mod=viewthread&tid=1605

### 4. [split_layout (分割线布局)](.\CDD\split_layout)

>   分割线容器, 此组件允许接收两个子组件并用分割线隔开, 此分割线可以自由调整
>
>   Split line container, this component allows receiving two sub components and separating them with a split line, which can be freely adjusted
>
>   <img src=".\sample_capture\split_layout.png" style="zoom:50%;" />

### 5. [stela_button (简单的带效果按钮)](.\CDD\stela_button)

>   一个动画效果的 Textbutton 按钮, 并不是什么很厉害的组件
>
>   Just a Textbutton with a easy anima

---

## GLSL

### 1. [cloud_node (点云图)](.\GLSL\cloud_node)

>   基于 Python 和 Shader 实现的点云图
>
>   Cloud Node base on Python and Shader
>
>   演示视频: https://www.bilibili.com/video/BV1WnJ3zTEiT/
>
>   <img src=".\sample_capture\cloud_node.png" style="zoom:40%;" />

### 2. [glitch (画面撕裂效果)](.\GLSL\glitch)

>   破旧电视机的画面形变效果, 写有一个 transform 和作用到 CDD 上的函数
>
>   The image distortion effect of a worn-out TV. written with a transform and a function applied to CDD
>
>   <img src=".\sample_capture\glitch.png" style="zoom:50%;" />

### 3. [particle (贴图粒子效果)](.\GLSL\particle)

>   粒子效果, 以及一个以图像素材变成粉末淡出的shader(其实是用 CDD 把两个 Shader 整合到一起)
>
>   Particle, with a image fadeout like dust shader ( but it just a cdd which mix two shader )
>
>   演示视频: https://www.bilibili.com/video/BV1mhVNzCEji/

### 4. [perspective (单点透视网格)](.\GLSL\perspective)

>   单点透视形变效果, 相应系统的相关插件, Debug 工具
>
>   Single point perspective deformation effect, addin and debug tool
>
>   <img src=".\sample_capture\perspective.png" style="zoom:70%;" />

### 5. [rect_color (渐变色长方形)](.\GLSL\rect_color)

>   渐变色矩阵, 用于快速添加渐变色到屏幕上
>
>   Gradient color matrix, used to quickly add gradient colors to the screen
>
>   <img src=".\sample_capture\rect_color.png" style="zoom:50%;" />

### 6. [rect_map (双色网格)](.\GLSL\rect_map)

>   网格效果, 用于添加双色网格
>
>   Grid effect, used to add dual color grids
>
>   <img src=".\sample_capture\rect_map.png" style="zoom:50%;" />

### 7. [uv_frame (uv 播放器)](.\GLSL\uv_frame)

>   根据渲染好的 UV 图像来渲染图片的位置
>
>   Use rendered UV to render image
>
>   演示视频: https://www.bilibili.com/video/BV1tLjBzyEGE/
>
>   <img src=".\sample_capture\uv_frame.png" style="zoom: 70%;" />

---

## Markdown

### 1. [小白都能看懂的 CDD 教程](.\Markdown\小白都能看懂的 Renpy CDD 教程.md)

>   自己写给萌新群友康的