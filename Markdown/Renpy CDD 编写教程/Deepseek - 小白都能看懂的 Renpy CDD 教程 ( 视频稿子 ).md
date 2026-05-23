# 写在前面
因为 Deepseek Token 清仓大甩卖所以我买了10块钱的 Token 没处花后来仓库找找素材, 然后找到了我这几篇写的灾难的东西, 想着: Deepseek 会写成什么样子? 于是就把之前的视频稿子丢过来让它重写了一遍, 嗯至少语言风格上比我写的好多了, 我的文笔真的很幼稚和口语对不起 ( )  
这篇重新生成的内容也还看得过去, 以及相关的使用例也是用的我的源码, 相比不会出现太大的问题, 所以我原本写的那篇太晦涩, 太抽象的话看看这个也不错的嗯


# 小白都能看懂的 Ren'Py CDD 教程（视频稿子）

> **系列定位**：面向有一点 Ren'Py 基础、想突破系统限制实现自定义效果的开发者。从零开始，每一步都有可运行的代码。
>
> **符号说明**：带 `*` 的章节为可选内容——用于保证知识体系的完整性，但跳过也不影响后续学习。

---

## Opening

大家好，我是 Koji。

如果你在用 Ren'Py 做游戏，一定遇到过这种情况：你想实现一个独特的按钮效果、一个炫酷的转场动画、或者一种官方组件做不到的布局方式——翻遍文档也找不到现成方案。

这种时候，你就需要 **CDD（Creator-Defined Displayable，创作者定义的可视组件）**。

用官方文档的话说：*"最复杂也最强大，能够定制 Ren'Py 表现效果的方式，就是使用创作者定义的可视组件。"*

在过去的一年里，我研究并编写了不少 CDD，深深感受到了这个系统的强大与灵活。所以我想把学到的这些东西整理成教程，既给自己留个记录，也希望对你有帮助。

本教程的核心思路是：**从代码出发，用可运行的例子辅助理解**。每节课我们都会写一个能实际跑起来的小组件，逐步升级，直到你能随心所欲地创造自己的组件。

那我们开始吧。

---

## Stage 1 — 认识可视化组件

> **本节目标**：理解什么是可视化组件，知道如何查看系统源码，以及如何把一个组件显示到屏幕上。

### 1.1 什么是可视化组件？

简单来说，**可视化组件 = 画面 + 交互**。

你看视频网站上的播放器——有进度条、有全屏按钮、有弹幕列表。这些东西都在屏幕上显示画面，并且能响应你的鼠标点击——它们就是可视化组件。

在 Ren'Py 里也是一样的道理。我们平时写 `screen` 语句用到的东西——`text`、`button`、`frame`——本质上都是可视化组件。Ren'Py 预设了很多这样的组件供我们使用。

但预设总归有限。当你想要一个"鼠标按下时会变形的按钮"，或者"跟随鼠标视差滚动的背景"时——对不起，没有现成的。

这时候就需要 **自定义可视化组件（CDD）** 了。它能让你：

- 完全控制组件渲染出的每一个像素
- 捕获任意的鼠标、键盘事件并自定义响应
- 把其他组件当作"积木"组合成新的布局

> 一句话总结：CDD 就是把 Ren'Py 的 UI 能力从"用积木搭房子"升级到"自己造积木"。

### 1.2 去哪里看系统源码？

有些组件在文档里是找不到的。比如 `button`——你只能查到它的 screen 语法词条，找不到它的可视化组件类名。

这时候就需要直接看 Ren'Py 引擎的源码。这些源码是你最好的学习资料，推荐重点关注三个文件：

| 文件 | 用途 |
|------|------|
| `renpy/display/displayable.py` | **Displayable 根类**——所有可视化组件的祖先，定义了最基础的框架和接口 |
| `renpy/display/behavior.py` | **交互组件**——Button、Bar、Timer、Input 等都在这里 |
| `renpy/display/layout.py` | **布局组件**——Container、Fixed、Crop 等容器类 |

> 小技巧：用 VS Code 打开 Ren'Py 安装目录，搜索这些文件名就能找到。

### 1.3 如何显示一个可视化组件？

在 screen 里显示一个组件，最简单的方式是 `add` 语句：

```renpy
screen hello_screen:
    add Text("你好世界")
```

运行后，屏幕上就会出现"你好世界"四个字。

还可以附加 transform 特性来控制位置：

```renpy
screen hello_screen:
    add Text("你好世界") xalign 0.5 yalign 0.5
```

现在文字就在屏幕正中央了。

### * 1.4 add 语句的本质

如果你把组件提前定义好再 add 呢？

```renpy
default hello = Text("你好世界")

screen hello_screen:
    add hello
    add hello
    add hello
```

你会发现三个 add 添加的是**同一个对象**。如果换成能响应鼠标的 `TextButton`，三个按钮中任意一个被 hover，其他两个也会跟着变化——因为它们共享同一个源对象。

> **结论**：`add` 语句本质上是一个带 transform 特性的**引用语句**，不是复制。

### * 1.5 神奇的 as 语句

`as` 可以让你在 screen 里捕获自动生成的可视组件对象：

```renpy
screen test_as:
    text "hello" as t
    $ print(t)  # 打印出 Text 对象
```

这在调试 screen 语句生成的组件时非常有用。

---

## Stage 2 — 编写第一个 CDD

> **本节目标**：理解 `render` 方法和 `Render` 对象，写出一个能动起来的组件。

### 2.1 两个核心概念

写 CDD 绕不开两个东西：**render 方法**和 **Render 对象**。

**render 方法**是你必须重写的函数。引擎在需要绘制你的组件时会调用它，并把以下信息传进来：

| 参数 | 含义 | 通俗理解 |
|------|------|----------|
| `width`, `height` | 布局分配给此组件的可用空间（像素） | "给你这么大的画布" |
| `st` | 显示时间轴（秒），从组件首次出现在屏幕时开始计时 | "你从出场到现在过了多久" |
| `at` | 动画时间轴（秒），从同标签组件首次显示时计时 | "这一组动画从开始到现在过了多久" |

**Render 对象**是 render 方法的返回值。你可以把它理解为一张**透明的画布**——在这张画布上绘制画面，然后交给引擎去显示。用 `renpy.Render(width, height)` 创建一张新画布。

### 2.2 最简 CDD：空组件

先从最小的可运行代码开始：

```python
class EmptyComponent(renpy.Displayable):
    def __init__(self):
        super().__init__()

    def render(self, width, height, st, at):
        return renpy.Render(width, height)
```

然后在 screen 里 add 它：

```renpy
screen test:
    add EmptyComponent()
```

运行不报错，恭喜——你已经写出了人生中第一个 CDD！

> **常见错误排查**：
> - 报错说不是 Displayable → 检查是否继承了 `renpy.Displayable`
> - 报错说 render 返回值不对 → 检查 render 方法是否返回了 `renpy.Render` 对象
> - 屏幕一片黑但没有报错 → 这是正常的！空组件确实什么都不显示。

### 2.3 让它显示画面

接下来我们让组件真正显示一些东西。`renpy.displayable()` 函数可以把字符串（颜色代码或图片路径）转成可视化组件：

```python
class ColorBlock(renpy.Displayable):
    def __init__(self, color="#f00", size=(200, 150)):
        super().__init__()
        self.block = renpy.displayable(color)  # 把颜色字符串转成组件
        self.size = size

    def render(self, width, height, st, at):
        rv = renpy.Render(*self.size)
        # 获取色块的画面，渲染到指定大小
        block_render = self.block.render(*self.size, st, at)
        # 把色块的画面"贴"到我们的画布上
        rv.blit(block_render, (0, 0))
        return rv
```

运行后，你会看到一个 200×150 的红色矩形。

### 2.4 让组件动起来！

动画的关键是 `st`（时间轴）和 `renpy.redraw()`（请求刷新）：

```python
from math import sin, cos

class BouncingBlock(renpy.Displayable):
    def __init__(self, color="#f00"):
        super().__init__()
        self.block = renpy.displayable(color)

    def render(self, width, height, st, at):
        rv = renpy.Render(width, height)
        block_render = self.block.render(80, 80, st, at)

        # 用三角函数让色块做圆周运动
        x = int(width/2 + sin(st * 2) * 150 - 40)
        y = int(height/2 + cos(st * 2) * 150 - 40)

        rv.blit(block_render, (x, y))

        # 请求下一帧刷新——0 表示越快越好
        renpy.redraw(self, 0)
        return rv
```

一个绕圈运动的小方块就完成了！`renpy.redraw(self, 0)` 告诉引擎"尽快再调用一次我的 render"，这样就形成了连续的动画。

### * 2.5 render 参数的深入理解

`width` 和 `height` 的值取决于**父布局**：

- 在 `fixed` 中：等于 fixed 的可用空间
- 在 `hbox` 中：由水平排列的兄弟组件共同决定
- 被 `xysize` 限制时：等于限制后的值

`st` 和 `at` 的区别用一个例子说明：

```renpy
image my_cdd = MyCDD()

label start:
    show my_cdd       # st=0, at=0（首次出现）
    "……"
    show my_cdd       # st=0（重新开始计时）, at=继续（同标签未中断）
    hide my_cdd
    show my_cdd       # st=0, at=0（hide 后重新 show，两者都重置）
```

> 大多数情况下用 `st` 就够了。只有当你需要跨 show/hide 保持动画连续性时才需要关注 `at`。

---

## Stage 3 — 响应用户交互

> **本节目标**：掌握 `event` 方法，实现按压切换、悬停检测，并学会阻止事件穿透。

### 3.1 认识 event 方法

`event` 是 CDD 接收用户交互的入口。它的签名是：

```python
def event(self, ev, x, y, st):
```

最重要的参数是 `ev`——一个 pygame 事件对象。通过 `ev.type` 来判断事件类型：

| 事件常量 | 含义 |
|----------|------|
| `pygame.MOUSEBUTTONDOWN` | 鼠标按键按下 |
| `pygame.MOUSEBUTTONUP` | 鼠标按键抬起 |
| `pygame.MOUSEMOTION` | 鼠标移动 |
| `pygame.KEYDOWN` | 键盘按键按下 |
| `pygame.KEYUP` | 键盘按键抬起 |

`x` 和 `y` 是以**当前组件左上角为原点**的鼠标相对坐标。

> 也可以用 `renpy.map_event()` 来检测 Ren'Py 自定义的一些事件（如滚轮），它兼容 pygame 常量并提供额外的识别能力。

### 3.2 实战一：按压切换图片

这是我们第一个真正有用的 CDD——按住鼠标时显示一张图，松开时显示另一张：

```python
import pygame

class PressSwitch(renpy.Displayable):
    def __init__(self, idle_image, pressed_image):
        super().__init__()
        self.idle_image = renpy.displayable(idle_image)
        self.pressed_image = renpy.displayable(pressed_image)
        self.pressing = False

    def event(self, ev, x, y, st):
        if ev.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            old = self.pressing
            # pygame.mouse.get_pressed() 返回 (左,中,右) 三个布尔值
            self.pressing = any(pygame.mouse.get_pressed())
            if old != self.pressing:
                renpy.redraw(self, 0)  # 状态变了，请求重绘

    def render(self, width, height, st, at):
        img = self.pressed_image if self.pressing else self.idle_image
        return img.render(width, height, st, at)
```

> **技巧**：用 `any(pygame.mouse.get_pressed())` 而不是判断 `ev.button`，因为它能正确处理"鼠标在组件外松开"的情况。

### 3.3 实战二：悬停检测

只需要在 `MOUSEMOTION` 事件中判断鼠标坐标是否在范围内：

```python
class HoverDetector(renpy.Displayable):
    def __init__(self, normal_image, hover_image, area=(200, 100)):
        super().__init__()
        self.normal_image = renpy.displayable(normal_image)
        self.hover_image = renpy.displayable(hover_image)
        self.area = area
        self.hovering = False

    def event(self, ev, x, y, st):
        if ev.type == pygame.MOUSEMOTION:
            old = self.hovering
            self.hovering = (0 < x < self.area[0] and 0 < y < self.area[1])
            if old != self.hovering:
                renpy.redraw(self, 0)

    def render(self, width, height, st, at):
        img = self.hover_image if self.hovering else self.normal_image
        return img.render(width, height, st, at)
```

### 3.4 阻止事件穿透

如果你把上面的组件盖在一个 button 上，你会发现点了组件后 button 也会被点到。这是因为事件默认会**向下传播**。

用一行代码阻止它：

```python
raise renpy.display.core.IgnoreEvent()
```

只需要在 event 方法里你**确认要吞掉这个事件**的地方加上它即可。通常结合区域检测使用——鼠标在组件内时才拦截：

```python
def event(self, ev, x, y, st):
    if ev.type == pygame.MOUSEBUTTONDOWN:
        if 0 < x < self.width and 0 < y < self.height:
            # 处理点击……
            self.pressing = True
            renpy.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()  # 阻止传播
```

> **小结**：三种交互模式已经覆盖了大多数场景——按压切换、悬停检测、事件拦截。组合起来就能做出各种交互组件。

---

## Stage 4 — 编写布局容器：QuickMenu 底边栏

> **本节目标**：掌握子组件管理，学会正确使用 `renpy.render()` 和 `place()` 方法。

前面我们都是操作单个组件。现在来做点更实际的——一个能自动排列子组件的**横向布局容器**，类似简化版的 `hbox`。

我们会用**三次迭代**来逐步完善它。

### 4.1 第一版：固定间距排列

最简单的方式——给每个子组件分配一个固定的 x 坐标：

```python
class EasyQuickMenu(renpy.Displayable):
    def __init__(self, *items):
        super().__init__()
        self.items = tuple(renpy.displayable(i) for i in items)
        self.spacing = 200  # 固定间距
        self.positions = []  # 记录位置，供 event 使用

    def render(self, width, height, st, at):
        rv = renpy.Render(width, height)
        self.positions = []
        for idx, item in enumerate(self.items):
            x = idx * self.spacing
            item_render = item.render(100, 100, st, at)
            rv.blit(item_render, (x, 0))
            self.positions.append(x)
        return rv

    def event(self, ev, x, y, st):
        for idx, item in enumerate(self.items):
            item.event(ev, x - self.positions[idx], y, st)
```

能用了，但问题明显：不管子组件实际多大，都硬塞在 100×100 的空间里，间距也是固定的。

### 4.2 第二版：根据实际大小排列

每个子组件渲染后的实际大小可以通过 `render.get_size()` 获取。我们用它来动态决定下一个组件的位置：

```python
class NeatQuickMenu(renpy.Displayable):
    def __init__(self, *items):
        super().__init__()
        self.items = tuple(renpy.displayable(i) for i in items)
        self.spacing = 20
        self.positions = []

    def render(self, width, height, st, at):
        rv = renpy.Render(width, height)
        x = 0
        self.positions = []

        for item in self.items:
            item_render = item.render(width, height, st, at)
            rv.blit(item_render, (x, 0))
            self.positions.append(x)
            # 关键：根据实际宽度来推下一个位置
            x += item_render.get_size()[0] + self.spacing

        return rv

    def event(self, ev, x, y, st):
        for idx, item in enumerate(self.items):
            item.event(ev, x - self.positions[idx], y, st)
```

现在组件之间不会重叠了，间距也是固定的——就像一个真正的 hbox。

### 4.3 第三版：解决 redraw 失效问题

如果你把一个会自己动的组件（比如 Stage 2 的 `BouncingBlock`）放进 QuickMenu，你会发现它**不动了**。

原因在于我们直接用 `item.render()` 绕过了 Ren'Py 的渲染缓存机制。正确做法是使用 `renpy.render()` 函数：

```python
# ❌ 错误：绕过缓存，子组件 redraw 失效
item_render = item.render(width, height, st, at)

# ✅ 正确：走系统缓存，子组件 redraw 正常
item_render = renpy.render(item, width, height, st, at)
```

改完后再试——子组件的动画恢复了！

### 4.4 锦上添花：使用 place 处理样式

有些组件自带位置样式（如 `xanchor`、`yalign` 等）。用 `place()` 方法可以自动处理这些：

```python
for item in self.items:
    item_render = renpy.render(item, width, height, st, at)
    # place 会根据组件的样式特性自动计算偏移，返回实际放置位置
    offset = item.place(rv, x, 0, width, height, item_render)
    self.offsets.append(offset)
    x += item_render.get_size()[0] + self.spacing
```

到此，一个功能完善的横向布局容器就完成了。用同样的思路，你可以做出纵向布局、网格布局甚至更复杂的布局。

> **本节核心**：管理子组件有三个要点——① 用 `renpy.render()` 而非直接 `.render()`；② 用 `get_size()` 获取实际大小；③ 用 `place()` 处理样式。记住这三点，布局组件就不难了。

---

## Stage 5 — 特效实战：流光文字

> **本节目标**：运用 `subsurface` 裁剪、缓动曲线、Canvas 绘制做出一款炫酷的动画文字。

先看看成品效果——文字上有一道光泽从左到右扫过，鼠标悬停时动画播放，移开时动画倒放。（展示画面）

这个效果用到了三个新技巧，我们逐一掌握。

### 5.1 裁剪效果：subsurface

`Render.subsurface((x, y, w, h))` 可以裁出画布的一个矩形区域。它和 `Crop` 组件不同——纯 CPU 计算，在某些场景下更灵活（但大量使用时要注意性能）。

实现流光文字的基本思路：

1. 准备两个不同颜色的 `Text` 组件（比如白色文字 + 灰色文字）
2. 对灰色文字进行裁剪，只显示当前动画进度对应的那一部分
3. 把裁剪后的灰色文字覆盖到白色文字上面

```python
class StellaText(renpy.Displayable):
    def __init__(self, text, font_size=100):
        super().__init__()
        self.base = Text(text, color="#fff", size=font_size)       # 底色：白色
        self.overlay = Text(text, color="#aaa", size=font_size)    # 覆盖：灰色

    def render(self, width, height, st, at):
        rv = renpy.Render(width, height)

        # 先画白色底
        base_render = self.base.render(width, height, st, at)
        rv.blit(base_render, (0, 0))

        # 画灰色覆盖层——但只裁剪出当前进度的那部分
        text_width = base_render.get_size()[0]
        progress = (st % 2) / 1.0  # 0→1 循环，周期 2 秒
        cut_x = int(progress * text_width)

        overlay_render = self.overlay.render(width, height, st, at)
        # subsurface 的参数是 (x, y, 宽度, 高度)
        overlay_render = overlay_render.subsurface((0, 0, cut_x, overlay_render.get_size()[1]))
        rv.blit(overlay_render, (0, 0))

        renpy.redraw(self, 0)
        return rv
```

### 5.2 加上缓动曲线让动画更自然

线性运动看起来很机械。缓动曲线可以让动画有"加速"或"减速"的感觉。

Ren'Py 内置了大量缓动函数，在 `_warper` 模块中。比如 `_warper.ease_quint` 就是一个先快后慢的曲线：

```python
from renpy.easy import _warper

# 对 progress 应用缓动——自动将 0→1 映射为缓动后的值
cut_time = st % 2  # 0→2 原始时间
head_pos = _warper.ease_quint(cut_time - 1) * text_width if cut_time > 1 else 0
end_pos = _warper.ease_quint(cut_time) * text_width if cut_time < 1 else text_width
```

你可以去 [easings.net](https://easings.net/zh-cn) 预览各种曲线效果，然后在 Ren'Py 文档的 [warpers 页面](https://doc.renpy.cn/zh-CN/transforms.html#warpers) 找到对应的函数名。

### 5.3 用 Canvas 绘制装饰

`Render.canvas()` 返回一个可以直接画几何图形的对象，支持矩形、圆形、线条、多边形：

```python
rv.canvas().rect("#fff", (x, y, w, h))      # 画矩形
rv.canvas().circle("#f00", (cx, cy), 10)    # 画圆
rv.canvas().line("#0f0", (x1,y1), (x2,y2), width=3)  # 画线
```

给流光文字加一个白色背景条，让效果更明显：

```python
# 在覆盖层下方画一个半透明光带
bar_half = 15
rv.canvas().rect("#fff4", (end_pos - bar_half, 0, bar_half * 2, height))
rv.blit(overlay_render, (0, 0))
```

### 5.4 悬停触发 / 离开恢复

结合 Stage 3 的悬停检测技巧，让动画在鼠标悬停时正向播放，离开时反向恢复：

```python
class HoverStellaText(renpy.Displayable):
    def __init__(self, text, font_size=100):
        super().__init__()
        self.base = Text(text, color="#fff", size=font_size)
        self.overlay = Text(text, color="#aaa", size=font_size)
        self.progress = 0.0          # 当前动画进度 0→1
        self.hovering = False
        self.last_st = None

    def event(self, ev, x, y, st):
        if ev.type == pygame.MOUSEMOTION:
            self.hovering = (0 < x < self.base_width and 0 < y < self.base_height)

    def render(self, width, height, st, at):
        if self.last_st is None:
            self.last_st = st - 0.01

        # delta time 驱动，避免时间跳跃问题
        dt = st - self.last_st
        target = 1.0 if self.hovering else 0.0
        self.progress += (target - self.progress) * min(dt * 5, 1)
        self.progress = max(0.0, min(1.0, self.progress))
        self.last_st = st

        # …后续用 self.progress 替代 st 做渲染
        # 只要还没到目标值，就继续刷新
        if self.progress not in (0.0, 1.0):
            renpy.redraw(self, 0)
```

> **三个常见陷阱**：
> 1. **动画轴超限**——确保 progress 始终 clamp 在 [0, 1] 内
> 2. **时间跳跃**——用 `delta time`（`st - self.last_st`）驱动动画，而非直接用 `st` 的绝对值
> 3. **动画中断**——只要 `progress` 没到目标值就继续 `renpy.redraw(self, 0)`，否则移开鼠标后动画会停在半路

---

## Stage 6 — 注册 SL 语法：像内置组件一样调用

> **本节目标**：使用 `renpy.register_sl_displayable()` 把自己的组件注册为 screen 语言关键字。

写了那么多 CDD，每次都要 `add MyComponent(...)` ——如果能像 `text`、`button` 那样直接用就好了。`register_sl_displayable` 就是做这件事的。

### 6.1 注册一个简单组件

以最简单的色块组件为例：

```python
class ShowColor(renpy.Displayable):
    def __init__(self, color, size=(100, 100)):
        super().__init__()
        self.color = color
        self.size = size

    def render(self, w, h, st, at):
        rv = renpy.Render(*self.size)
        block = renpy.displayable(self.color)
        rv.blit(block.render(*self.size, st, at), (0, 0))
        return rv

# 注册：关键字 "show_color"，接收 0 个子组件
renpy.register_sl_displayable("show_color", ShowColor, 0
    ).add_positional("color"   # 固定参数——使用时必须传入
    ).add_property("size"      # 可选属性——通过关键字传入
    )
```

注册之后就可以在 screen 里像内置组件一样使用了：

```renpy
screen test:
    show_color "#f00" size (300, 200)
```

### 6.2 注册一个容器组件

容器组件（能容纳子组件的那种）需要特殊处理——必须实现 `add` 方法，并且注册时子组件数设为 `""`（不限数量）：

```python
import random
from math import sin, cos

class ShakeLayout(renpy.Displayable):
    def __init__(self, shake_range=(10, 5)):
        super().__init__()
        self.shake_range = shake_range
        self.children = []

    def add(self, child):
        """接收子组件——这是容器组件的必备方法"""
        self.children.append(renpy.displayable(child))

    def render(self, w, h, st, at):
        rv = renpy.Render(w, h)
        rand = random.random() * 6.28
        ox = int(sin(rand) * self.shake_range[0])
        oy = int(cos(rand) * self.shake_range[1])
        for child in self.children:
            cr = renpy.render(child, w, h, st, at)
            child.place(rv, ox, oy, w, h, cr)
        renpy.redraw(self, 0)
        return rv

# 注册：子组件数 "" 表示不限制数量
renpy.register_sl_displayable("shake_layout", ShakeLayout, "", 0
    ).add_property("shake_range"
    )
```

用法和内置布局一样自然：

```renpy
screen test:
    shake_layout:
        shake_range (15, 8)
        text "晃动的文字"
        textbutton "晃动的按钮"
```

### 6.3 进阶：继承内置组件并注册

你还可以直接继承 Ren'Py 内置组件来扩展，保留原有功能的同时添加新特性：

```python
from random import random

class ShakeText(renpy.text.text.Text):
    def __init__(self, text, shake_range=(10, 5), **kwargs):
        super().__init__(text, **kwargs)
        self.shake_range = shake_range

    def render(self, w, h, st, at):
        base = super().render(w, h, st, at)    # 先让 Text 正常渲染
        rv = renpy.Render(*base.get_size())
        rand = random() * 6.28
        ox = int(sin(rand) * self.shake_range[0])
        oy = int(cos(rand) * self.shake_range[1])
        rv.blit(base, (ox, oy))                 # 偏移绘制
        renpy.redraw(self, 0)
        return rv

renpy.register_sl_displayable("shake_text", ShakeText, 0
    ).add_positional("text"
    ).add_property("shake_range"
    ).add_property_group("text")  # ← 关键！继承 text 的所有样式属性
)
```

关键一步是 `add_property_group("text")`——这行代码让 `shake_text` 拥有了 `size`、`color`、`font`、`bold`、`italic` 等所有 `text` 语句支持的样式属性。

> 现在你可以写：`shake_text "抖起来！" shake_range (8, 4) size 50 color "#f00" bold True`

### 6.4 进阶项目参考

在你的 workspace 里，有一些基于 CDD 开发的实际项目可以作为进阶参考：

| 项目 | 路径 | 说明 |
|------|------|------|
| 按压切换按钮 | `press_button/` | 带按压态切换的按钮，含完整 SL 注册 |
| 可拖动分割线 | `split_layout/` | 水平和垂直分屏布局组件 |
| 流光文字按钮 | `stela_button/` | Stage 5 效果的完整交互版 |
| 一点透视组件 | `GLSL/perspective/` | 结合 GLSL Shader 的高级 CDD |
| 环形菜单 | `circle_menu/` | 带 Canvas 绘制的圆弧菜单 |
| 弹幕显示 | `dammu/` | 实时弹幕渲染组件 |

> 建议学完教程后去读这些项目的源码——看到自己学到的知识被用在真实项目中，会对 CDD 的能力有更直观的认识。

---

## 总结

回顾一下我们走过的路：

| Stage | 核心技能 | 你能做什么了 |
|-------|----------|-------------|
| 1 | 理解可视化组件概念 | 知道 CDD 是什么，能查看系统源码 |
| 2 | render + Render | 写出能显示画面、能动起来的组件 |
| 3 | event 事件处理 | 实现按压反馈、悬停检测、事件拦截 |
| 4 | 子组件管理 + 布局 | 编写自己的 hbox/vbox 布局容器 |
| 5 | subsurface + 缓动 + Canvas | 制作带特效动画的视觉组件 |
| 6 | SL 注册 | 把组件注册为 screen 语言关键字 |

CDD 是 Ren'Py 最强大的扩展机制。掌握了它，你的 UI 想象力就不再受系统组件的限制——你能想到的效果，基本都能实现。

如果教程对你有帮助，欢迎去我的项目仓库点个 Star，也欢迎提 Issue 交流问题。

感谢观看，我们下个系列见！
