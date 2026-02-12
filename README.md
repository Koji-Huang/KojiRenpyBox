# Koji Renpy Box

这里是科基的个人 Renpy 组件仓库, 希望里面的组件能对你的开发提供一些帮助什么的
对这些组件的使用有疑问或者希望我帮你写组件可以发邮件至 koji233@163.com

Koji's Renpy Widget Repositories. Hope these widget can give you some help
if there is some question or wish I write widget for you, send email to koji233@163.com

Bilibili 账号: https://space.bilibili.com/1146352855
视频合集: https://space.bilibili.com/1146352855/lists/5362589?type=season

---

# 使用须知

-   在使用的时候请注意并遵守部分文件内存在的协议信息
-   每一个组件都是独立的, 就算存在依赖也会将依赖放入同文件夹内
-   所有素材本人都未持有版权, 仅作测试例, 使用到项目中请记得删去
-   几乎每一个组件都在文件夹下写有 Readme(说明) 与 Sample(示例), 记得看
-   部分组件在 B站 有演示视频, 但是一切参数与调用请以 Readme 与 Sample 为准
-   可能因为版本差异带来的问题, 请参照文末对组件源码进行修改

---

# 组件索引:

## CDD - 创作者自定义的可视化组件

[Canvas: 带圆角与描边的 直线, 矩形, 圆 组件](CDD/canvas)

[CircleMenu: 圆环布局 与 圆盘菜单](CDD/circle_menu)

[Dammu: 滚动弹幕组件](CDD/dammu)

[PressButton: 带按压样式词条的图像按钮](CDD/press_button)

[RenderDebugger: 渲染树查看工具](CDD/render_debugger)

[SplitLayout: 分割线容器](CDD/split_layout)

[StelaButton: 一个带简单动画的按钮 (无 Readme)](CDD/stela_button)

## GLSLShader - 借助着色器实现的相关效果

[Glitch: 简单的故障效果, 可用于转场](GLSL/glitch)

[Perspective: 单点透视小姑组件](GLSL/perspective)

[TrailingGlitch: 带拖尾的故障效果](GLSL/trailing_glitch)

[UV_Frame: UV 图像应用播放组件](GLSL/uv_frame)

[CloudNode: 点云图效果](GLSL/cloud_node)

[Particle: 图像粉状消失效果 (无 Readme)](GLSL/particle)

[RectColor: 颜色渐变矩形 (无 Readme)](GLSL/rect_color)

[RectMap: 双色网格 (无 Readme)](GLSL/rect_map)

## Markdown - 一些文章

[Renpy CDD 相关组件的解析与编写教程](Markdown/Renpy%20CDD%20相关组件的解析与编写教程.md)


[将任意目录添加到 Renpy 中作为游戏资源](Markdown/将任意目录添加到%20Renpy%20中作为游戏资源.md)


[自定义 Live2D 组件动作的一些思路](Markdown/自定义%20Live2D%20组件动作的一些思路.md)

[无视 UI 控件 ( 指定图层 ) 截图的一个方法](Markdown/无视%20UI%20控件%20(%20指定图层%20)%20截图的一个方法.md)


---

# 版本与平台问题

## Renpy 8.5.x 及后续版本的 pygame 调用

>   Renpy 文档: https://www.renpy.org/doc/html/changelog.html#pygame-sdl2-removal
>
>   因为 Renpy 的更新计划, pygame 包被移动到了不同的地方, 以下代码将不能使用
>
>   ```python
>   import pygame
>   from pygame import *
>   ```
>
>   这样的语句应该被替换为
>
>   ```python
>   import renpy.pygame
>   from renpy.pygame import *
>   ```
>
>   记住, 只有 8.5.x 及以上的版本需要这么做

## GLSL 出现不允许函数参数带默认值

>   部分平台与机器在处理 GLSL 时, 不允许 `fragment_function` 与 `vertex_function` 中定义的函数带有初始值
>
>   在运行时会爆一个这样的错:
>
>   ``` python
>   ShaderError: ERROR: x:x: '=': syntax error syntax error
>   ```
>
>   解决方法就是在 shader 源码里面把他们删了, 检查传参是否受影响
