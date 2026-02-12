# Renpy CDD 相关组件的解析与编写教程



Copyright 2025.6.1 Koji-Huang(koji233@163.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

---

这个教程最开始的想法虽然说是为了小白都能看懂, 写着写着才发现表达的方法完全不小白, 但却是我对 Renpy CDD 系统的理解的浓缩

有耐心看完这篇 Markdown, 你也可以写出和我仓库里一样的 CDD

---

## 写在前面

>   为什么要写这个东西呢? 因为群友太笨就写了 ( 才怪 )
>
>   此教程会以解释概念为主, 代码为辅来教大家如何编写 `CDD`, 拥有编程基础的人能快速理解里面写的意思, 如果你是0编程基础的小白的话, 立马理解里面的每一个概念可能有点困难, 但在看不下去前, 不妨先运行里面的代码, 也许运行的效果能代替那些听不懂的专业名词.
>
>   即使本教程写的相当的简短, 但想理解全部的内容可能需要不少的时间, 可千万别抱着'看完本文我就是`CDD`糕手'的想法噢, 最好自己动手编写此教程里的每一个组件, 这样不仅会让你更好的理解组件的运作关系, 也许你会有属于自己的新的理解
>
>   此教程中所有的 d 都为拓展内容, 他们并不是入门选项所以我打上了 * 号, 但他们都是相当有价值的内容, 在阅读完基础部分后不妨阅读一下, 如果感到理解困难就先跳过吧

---

## Stage 1. 可视化组件相关概念

### a. 什么是可视化组件与 `CDD`

>   可视化组件, 顾名思义, 是一种用于绘制, 显示图像的类型. `Renpy` 预设了大量的可视化组件以便于大家使用, 但总有些人想追求一些预设没有的组件, 有些人费尽心思用预设的可视化组件实现了自己的功能, 但是性能消耗却远远超出预期, 最终弃用
>
>   而 `CDD`, 全程 `Creator Defined Displayables`, 文档里的译名为"创作者定义的可视组件". 是一种允许大家通过自己的手段来编写属于自己的可视化组件, 它允许大家用各种手段来绘制出自己想要的可视化组件, 也能给大家性能优化的手段 ( 代码心理学, 优化的手段, 成神术 )
>
>   `CDD` 的编写需要一定的 `Python` 基础以及 `GUI` 系统交互原理的理解, 本篇并不会补齐这些知识, 仅仅是讲讲可视化组件编写的相关方式, 如果阅读起来感到困难的话, 咱没办法了 ( )
>
>   ---

### b. 系统的可视化组件

>   这里列出部分 `Renpy` 系统内的可视化组件对应的文件位置, 假如某天我们希望引用, 模仿或者改写某个组件的样式时, 我们可以先来看看这些代码, 毕竟是第一手的源码
>
>   `renpy/display/displayable.py`
>
>   > `Displayable` (所有可视化组件的基形)
>
>   `renpy/display/behavior.py`
>
>   >   `Button` (按钮对象)
>   >
>   >   `Input` (输入对象)
>   >
>   >   `Timer` (计时器对象)
>   >
>   >   ...
>   
>   `renpy/display/im.py`
>   
>   >   `Image` (图像对象)
>   >
>   >   `Composite` (多图像组合对象)
>   >
>   >   `Scale` (图像缩放对象)
>   >
>   >   ...
>
>   `renpy/display/layout.py`
>
>   >   `Null` (空对象)
>   >
>   >   `Container` (多子对象对象)
>   >
>   >   `Grid` (布局对象)
>   >
>   >   ...
>   
>   ---

### c. 如何声明一个可视化组件

> 一个基础的可视化组件必须遵循两个要素
>
> 1. 所有的派生类或者他们的父对象都需要继承自 `renpy.display.displayable.Displayable` 类 ( 调用时可以简写为 `renpy.Displayable` )
> 2. 所有派生类或者他们的父类都需要定义一个 `render` 函数
>
> 这里举一个例子
>
> ```python
> # 定义一个叫做 MyButton 的自定义可视化组件, 该组件定义上继承自 renpy.display.behavior.Button
> class MyButton(renpy.display.behavior.Button):
>     # 该可视化组件的初始化函数
>     def __init__(self, *args, **kwargs):
>         # 调用父类的初始化函数继承特性
>         super().__init__(*args, **kwargs)
>         self.name = "MyButton"
> 
>     # 由于父类已经定义过了 render 函数, 所以我们可以不用定义一个新的 render 函数
> ```
>
> 注意: `super().__init__()` 是必须的(此语句用于调用父组件的初始化函数, 不懂的话可以百度`python super`这个词条), 不然会爆出一个很无厘头的错误
>
> ---

### *d. 如何调用一个可视化组件

>   在 `Renpy` 代码里可视化组件有三种显示方式
>
>   1. `add` 语句
>
>      > `add` 语句可以添加一个待实例化, 已实例化的可视化组件到 `screen` 上, 并调整对应的样式, 例如
>      >
>      > ```python
>      > init python:
>      >        my_button = TextButton("AAA")
>      > 
>      > screen test_screen:
>      >        # 添加待实例化的可视化组件
>      >        add TextButton("BBB") xalign 0.0
>      >        # 添加已实例化的组件
>      >        add my_button xalign 1.0
>      > ```
>
>   2. `show` 语句
>
>      > `show` 语句是用于 演出脚本 里的语句, 例如
>      >
>      > ```python
>      > define my_button = TextButton("AAA")
>      > 
>      > script test_script:
>      >        show my_button
>      > ```
>
>   3. 注册语句
>
>      > 注册语句的方法能让可视化组件调用起来更加方便, 但注册起来略微麻烦, 此内容将在 `Stage6` 进行讲解 
>      >

---

## Stage 2: 显示一个图片并添加一些效果

>    在上文里我们已经提过了该怎么定义一个可视化组件, 如果我们期望可视化组件按我们的期望显示的话, 我们首先来讲讲 `CDD` 的 `render` 函数, 此函数负责接收参数与传回此可视化组件的画面的函数
>
>    这里引用一下 `renpy.displayable.display` 中 `Displayable.render` 函数的代码注释
>
>    ```python
>def render(self, width, height, st, at):
>        """
>        Called to display this displayable. This is called with width
>        and height parameters, which give the largest width and height     
>        that this drawable can be drawn to without overflowing some
>        bounding box. It's also given two times. It returns a Surface
>        that is the current image of this drawable.
>    
>    	调用以显示此可视化组件。
>    	被调用时会传入宽度和高度参数，它们给出了这个可视化组件可以绘制到的最大宽度和高度，而不会溢出一些边界框。
>    	也会传入两个时间戳
>    	它会返回一个Surface对象, 即此可视化组件的当前图像。
>    
>        @param st: The time since this widget was first shown, in seconds.
>        @param at: The time since a similarly named widget was first shown,
>        in seconds.
>    
>        @参数 st: 以秒为单位, 此可视化组件第一次被显示时的时间戳
>        @参数 at: 以秒为单位, 一个相同名称的可视化组件被第一次显示时的时间戳
>        """
>    ```
>    
>    以下是我对这些参数的解释:
>
>    `width, height`:
>
>    >   `width, height` 为此可视化组件应该绘制的大小, 注意, 是应该绘制的, 此参数会随着一些布局以及参数发生变化, 但这不代表我们只能在 `width, height` 的范围内绘制图像, 我们可以超出或小于这个范围绘制, 这个值仅仅是一个指导值, 方便于适应界面的布局方式.
>>
>    >   ---
>    
>    `st, at`:
>
>    >    `st` 在组件被 `add, show` 时都会从`0`开始计数, 它与 `at` 的不同需要一个小小的例子来展示:
>    >    
>    >    ```python
>    >    image a = A_Displayable() # 注意这里的 A_Displayable 指的是任意一个可视化组件, 本身没有这个类型
>    >    
>    >    label start:
>    >       show a
>    >       "现在 st 和 at 都从 0 开始计数"
>    >       show a
>    >       "现在 st 被重置为 0 了, 但 at 仍然是之前的计数"
>    >       hide a
>    >       "...."
>    >       show a
>    >       "现在 st 和 at 都从 0 开始计数"
>    >    ```
>    >
>    >    大概是这样的关系, 如果你写的是一个 `UI` 控件的话, 大概率是不需要理会 `at` 参数的
  ---
>    
>    `render` 函数的返回值:
>
>    >   `render` 函数必须返回一个 `Render` 对象, `Render` 对象是储存并传递此可视化组件画面的对象
>>
>    >   我们可以通过 `renpy.Render(w, h)`来获取一个空白的 `Render` 对象,  `w, h` 为此对象应该占据的宽高 ( 但实际上我们绘制的范围是可以超出此宽高的, 这两个参数有他用 ), 在获取时此对象是完全透明的
>    >
>    >   Render 对象在文档中的描述: https://doc.renpy.cn/zh-CN/cdd.html#renpy.Render
>    
>    ---

### 		a. 显示一张图片

> 我们可以通过返回其他可视化组件返回的 `Render` 作为此组件的效果, 例如, 我们可以通过调用 `renpy.displayable` 函数来获取一个 `Image` 对象, 然后直接返回此对象的 `Render`
>
> ```python
> class NormalPicture(renpy.Displayable):
> 	def __init__(self, image):
> 		super().__init__()
> 		# 获取 Image 对象
> 		self.image = renpy.displayable(image)
> 
> 	def render(self, width, height, st, at):
> 		# 获取 Image 对象的 Render
> 		image_render = self.image.render(width, height, st, at)
> 
> 		return image_render  # 直接返回这个 Render
> ```
>
> 调用
>
> ```python
> add NormalPicture("#fff")
> ```
>
> 此组件会显示为一个纯白的正方形, 此正方形的大小为此组件占据的大小, 如果希望限制这个大小, 我们可以给 `add` 语句传入一些参数来限制效果, 例如
>
> ```python
> add NormalPicture("#fff") xsize 100 ysize 100
> ```
>
> 此组件的大小为 `100x100` , 后文不会再赘述这个内容
>
> ---

### 		b. 显示一张图片并进行移动

> `Render` 类型有一个 `blit` 函数 , 此函数用于将其他 `Render` 对象按坐标绘制到此 `Render` 上, 这里引用官方文档的内容
>
> `blit(source, pos, main=True)` [link](https://doc.renpy.cn/zh-CN/cdd.html#renpy.Render.blit)
>
> >   在这个`Render`对象中绘制另一个`Render`对象。
>>
> >   -   `source`
> >
> >       > 待绘制的`Render`对象。
> >
> >   -   `pos`
> >
> >       > 绘制的位置。是一个`(x, y)`元组，表示从目标`Render`对象左上角为原点的坐标。
> >
> >   -   `main`
> >
> >       > 唯一的关键词参数。若为`True`， `source` 将会在样式检查器中显示。
> >
> >   ---
> 
> 此外, `Renpy` 默认会在很低的情况下更新可视化组件, 如果希望主动请求刷新组件, 我们可以使用 `renpy.redraw` 函数来命令系统重新调用 `render` 函数更新, 这里引用官方文档
>
> `renpy.redraw(d, when)` [link](https://doc.renpy.cn/zh-CN/cdd.html#renpy.redraw)
>
> >   经过 `when` 秒之后重新绘制可视组件 `d` 。 有时候可视组件的重绘间隔可能比设置的短(比如子组件重绘后)，那时将省略重绘。
>>
> >   ---
>
> ```python
>from math import sin, cos
> 
> class MovePicture(renpy.Displayable):
>     def __init__(self, image):
>        super().__init__()
>         self.image = renpy.displayable(image)
>        self.pos = (0, 0)
> 
>     def render(self, width, height, st, at):
>         # 创建一个新的 Render 来放置 image 的 Render
>         rv = renpy.Render(width, height)  
> 
>         # 获取 image 的 Render
>         image_render = self.image.render(width, height, st, at) 
> 
>         # 坐标利用三角函数, 以时间为轴进行画圆
>         self.pos = (sin(st) * 100, cos(st) * 100)
> 
>         # 将 image 的 Render 绘制到新的 Render 上
>         rv.blit(image_render, self.pos)
> 
>         # 以尽可能快的速度重新绘制此组件
>         renpy.redraw(self, 0)
> 
>         return rv
> ```
> 
> 调用
> 
> ```python
> add MovePicture("#fff")
> ```
> 
> 此组件会持续的画圆
>
> ---

### 		c. 显示一张图片并进行渐变

> 我们可以利用其他的可视化组件来对我们需要的图像进行处理, 例如 `Transform`, `Alpha`, `Tile` 等组件, 他们都能修改其子组件的显示效果来辅助我们达成我们想要的效果.
>
> 这里选用`Transform`, 因为这个可视化组件具有相当多的属性, 这些特性请参见文档: https://doc.renpy.cn/zh-CN/transform_properties.html#transform
>
> 下面的例子里我通过修改 `Transform` 对象 `alpha` 参数的值来影响最终 `Render` 出来图像的透明度
>
> ```python
> class FadePicture(renpy.Displayable):
> def __init__(self, image):
>   super().__init__()
> 
>   # 创建一个 image 对象
>   self.image = renpy.displayable(image)
> 
>   # 创建一个子对象为 image 的 Transform 对象
>   self.transform = Transform(self.image)
> 
> def render(self, width, height, st, at):
>   # 改变 Transform 的 alpha 值
>   self.transform.alpha = st % 1
> 
>   # 获取 Transform 的 Render
>   transform_render = self.transform.render(width, height, st, at)
> 
>   renpy.redraw(self, 0)
> 
>   return transform_render  # 返回这个 Render
> ```
>
> 调用
>
> ```python
> add FadePicture("#fff")
> ```
>
> 此组件会以每秒为周期从不透明变为透明
>
> ---

### 		*d. 如何获取子组件实际的位置

> 有些时候, 组件是带有些样式特性的, 例如 `ypos`, `xanchor` 等, 如果我们希望处理这些特性, 可以使用 `renpy.Displayable` 类中的方法 `place` 来自动处理这些参数, 此方法会根据组件内的这些特性以及对应的 `Render` 计算出子组件应该在的位置, 此处引用一下源码及其注释
>
> ```python
> def place(self, dest, x, y, width, height, surf, main=True):
>         """
>         This places a render (which must be of this displayable)
>         within a bounding area. Returns an (x, y) tuple giving the location
>         the displayable was placed at.
>         
>         这将通过一个给定的边界区域在此组件里放置一个 render
>         来返回一个包含了 (x, y) 的元组
>         此元组为此可视化组件所在的位置
> 
>         `dest`
>             If not None, the `surf` will be blitted to `dest` at the
>             computed coordinates.
>             
>         	如果不是 None，则 "surf" 将在计算出的坐标处被 blit 到 "dest" 上
> 
>         `x`, `y`, `width`, `height`
>             The bounding area.
>         
>         	限制的区域
> 
>         `surf`
>             The render to place.
>         
>         	用于 place 的 Render 对象
> 
>         `main`
>             This is passed to Render.blit().
>         
>         	此参数会传递给 Render.blit()
>         
>         """
> ```
>
> 下面引用 `Renpy` 中 `Conatiner` 组件的 `render` 函数的源码来讲解此函数
>
> ```python
> def render(self, width, height, st, at):
>     # 最开始获取了一个 Render 对象
>     rv = Render(width, height)
>     # 随后将此组件上次各个组件的位置信息清除
>     self.offsets = self._list_type()
>     
>     # 随后遍历各个子组件
>     for c in self.children:
>         # 这个是获取可视化组件的 Render 的另一种方式 (它的作用在下文有讲解)
>         cr = render(c, width, height, st, at)
>         # 调用 place 函数获取子组件的位置并将画面绘制到 rv 上
>         # rv 为绘制到的 Render, 对应 dest 参数
>         # 0, 0, width, height 对应 x, y, width, height
>         # cr 对应刚刚获取的可视化组件的 Render
>         offset = c.place(rv, 0, 0, width, height, cr)
>         # 将子组件的位置保存
>         self.offsets.append(offset)
>     
>     # 返回处理过的 rv
>     return rv
> ```

---

## Stage 3: 按下就改变显示图片的组件

>   在上文里我们已经讲过了要怎么让可视化输出画面 ,在这里, 我们讲一下要怎么让可视化组件与用户进行交互, 也就是 `CDD` 的 `event` 函数, `event` 函数是用于处理可视化组件事件的函数, 当存在新的事件时会调用这个函数来接收并处理对应的事件
>
>   ---

### a. `event` 函数的传参 `ev`

>   首先引用一下 `renpy.display.displayable.py` 里 `event` 函数的代码注释
>
>   ```python
>   def event(self, ev, x, y, st):
>       """
>       Called to report than an event has occured. Ev is the raw
>        pygame event object representing that event. If the event
>        involves the mouse, x and y are the translation of the event
>        into the coordinates of this displayable. st is the time this
>        widget has been shown for.
>   
>   		调用以响应发生的事件。
>   		ev 是表示该事件的 '原始 pygame event' 对象。
>   		如果事件涉及鼠标，则x和y是事件到该可显示对象坐标的转换。
>   		st是显示此小部件的时间。
>   
>       @returns A value that should be returned from Interact, or None if
>       no value is appropriate.
>   
>        @返回值 一个因为此 Interact 而返回的值，在没有合适的值的情况下应该返回None。
>       """
>   ```
>
>   在这个教程里, 我先不讲 `event` 函数的返回值具有什么意义 ( 实际上我也没利用过这个机制 ), 而是重点聚焦在前面的第一个参数 `ev`首先引用一下 `renpy.display.displayable.py` 里 `event` 函数的代码注释
>
>   ```python
>   def event(self, ev, x, y, st):
>       """
>       Called to report than an event has occured. Ev is the raw
>        pygame event object representing that event. If the event
>        involves the mouse, x and y are the translation of the event
>        into the coordinates of this displayable. st is the time this
>        widget has been shown for.
>   
>   		调用以响应发生的事件。
>   		ev 是表示该事件的 '原始 pygame event' 对象。
>   		如果事件涉及鼠标，则x和y是事件到该可显示对象坐标的转换。
>   		st是显示此小部件的时间。
>   
>       @returns A value that should be returned from Interact, or None if
>       no value is appropriate.
>   
>        @返回值 一个因为此 Interact 而返回的值，在没有合适的值的情况下应该返回None。
>       """
>   ```
>
>   在这个教程里, 我先不讲 `event` 函数的返回值具有什么意义 ( 实际上我也没利用过这个机制 ), 而是重点聚焦在前面的第一个参数 `ev`, 以下是对 `ev` 的相关解析:
>
>   1.   `ev` 拥有一个 `type` 参数来判断对应的事件
>
>        >   `type` 参数为 `int` 值, `Pygame` 里存在一些常量用于确认对应的类型, 比如 `pygame.MOUSEBUTTONDOWN = 1025`
>        >
>        >   所以当我们需要判断一个 `ev` 为某个事件时, 就可以用 `ev.type == pygame.xxx(某个常量)` 来判断当前 `ev` 是否为某个事件, 比如 `ev.type == pygame.MOUSEBUTTONDOWN`就是判断当前事件是否为鼠标按下事件
>        >
>        >   各个常量的命名都不一样, 这里给出最常用的几种事件: 
>        >
>        >   键盘事件: https://www.pygame.org/docs/ref/key.html
>        >
>        >   鼠标事件 ( https://www.pygame.org/docs/ref/mouse.html )
>        >
>        >   1.   `MOUSEBUTTONDOWN` (鼠标按下)
>        >   2.   `MOUSEBUTTONUP` (鼠标抬起)
>        >   3.   `MOUSEMOTION` (鼠标移动)
>        >
>        >   手柄事件: https://www.pygame.org/docs/ref/sdl2_controller.html
>        >
>        >   
>        >
>        >   此外, `Renpy` 也有自己的事件检测方式 `renpy.map_event`, 这个函数对比起 `pygame` 里声明的常量能额外检测出 `Renpy` 系统定义的 `ev`, 具体的介绍在文档 ([link](https://doc.renpy.cn/zh-CN/cdd.html#renpy.map_event)) 里已经相当的详细了, 假如你的组件需要接收 `Renpy`的一些特色事件或者不希望使用 `Pygame` 的检测, 可以使用这个
>        >
>        >   ---
>
>   2.   `ev` ( `pygame` 事件对象 ) 中包含有次事件对应的参数:
>
>        >   这个不难理解, 我们可以用 `ev.__dict__` 把 `ev` 的属性打印出来, 就比如 `MOUSEBUTTONDOWN` 事件:
>        >
>        >   ```python
>        >   {
>        >      '_type': 1025, 
>        >      'button': 1, 
>        >      'pos': (187, 238), 
>        >      'which': 0, 
>        >      'touch': False, 
>        >      'timestamp': 2953, 
>        >      'mod': 0
>        >   }
>        >   ```
>        >
>        >   在这里我们可以通过 `button` 参数来获取此 `MOUSEBUTTONDOWN` 事件中鼠标按下的按钮为哪一个
>        >
>        >   注意, 不同的 `ev` 甚至是同个 `type` 的 `ev` 都会有不一样的属性(例如滚轮滑动, 它的 `type` 也是 `MOUSEBUTTONDOWN`, 但参数却有所不同)
>        >
>        >   ---
>
>   3.   不要把 `ev` 来作为事件信息获取的唯一手段:
>
>        >   举个简单的例子, 假如我们希望一个按钮在鼠标左右键按下时触发, 用 `event` 函数传入的 `ev` 就需要两个变量来保存鼠标左右键的状态, 有没有更好的解法呢? 有的兄弟有的, 那就是使用 `pygame.mouse.get_pressed`(此函数会获取鼠标各个键按下的状态), 然后在每一次`ev.type == MOUSEBUTTONDOWN`的时候检查参数就可以了 ( 当然 `Renpy` 里也有对应的获取鼠标按下的接口 )
>        >
>        >   像这样的库, `pygame` 中有 `pygame.mouse`, `pygame.key`, `pygame.joystick`, `Renpy` 里也有相关的接口, 更进一步的话我们也可以自己定义一些事件获取/传输的手段. 这里更多想表达的意思是, 就算 `event` 有 `ev` 来传参数, 我们也可以考虑其他方法来获取我们想要的事件, 手段不应该是单一的, 高效的解决问题才是目的
>
>   ---

### 		b. 实现按下鼠标就改变图片

> 这里的代码没啥好解释的, 上面说的内容足够你理解这里的代码了
>
> ```python
> class PressChange(renpy.Displayable):
> 	def __init__(self, press_image, unpress_image):
> 		super().__init__()
> 		self.press_image = renpy.displayable(press_image)  # 按下时的图片
> 		self.unpress_image = renpy.displayable(unpress_image)  # 鼠标常态图片 ( 不按下时 )
> 		self.is_pressing = False
> 
> 	def event(self, ev, x, y, st):
> 		# 如果鼠标按钮按下或者抬起, 则进行一次检测
> 		if ev.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
> 			# 储存上次的状态
> 			old_state = self.is_pressing
> 
> 			# 如果存在按下的鼠标按钮, is_pressing 为 True
> 			self.is_pressing = True in pygame.mouse.get_press()
> 
> 			# 如果状态发生变化, 重新绘制该可视化组件
> 			if old_state != self.is_pressing:
> 				renpy.redraw(self, 0)
> 
> 	def render(self, width, height, st, at):
> 		# 根据不同的情况返回不同的 Render
> 		if self.is_pressing:
> 			return self.press_image.render(width, height, st, at)
> 		else:
> 			return self.unpress_image.render(width, height, st, at)
> ```
>
> 调用:
>
> ```python
> add PressChange("#fff", "#888")
> ```
>
> 调用此组件, 在鼠标未按下时为白色(`#fff`), 按下后为灰色(`#888`)
>
> ---

### 		c. 在组件区域内就改变图片

> 这里就需要提到 `x` 与 `y` 参数了, 这两个参数是当前 `ev` 相对于此可视化组件左上角的坐标 ( 注意, 是相对坐标, 不是绝对坐标 ), 右下为正, 左上为负
>
> 我们这里通过定义一个 area 参数作为检测区域, 当鼠标移动到这个区域时就改变对应的图片
>
> ```python
> class HoverChange(renpy.Displayable):
>     def __init__(self, hover_image, unhover_image, area=(100, 100)):
>         super(HoverChange, self).__init__()
>         self.hover_image = renpy.displayable(hover_image)
>         self.unhover_image = renpy.displayable(unhover_image)
>         self.area = area  # 定义检测区域
>         self.hovering = False
> 
>     def event(self, ev, x, y, st):
>         old_state = self.hovering
> 
>         # 判断状态
>         self.hovering = 0 < x < self.area[0] and 0 < y < self.area[1]
> 
>         if self.hovering != old_state:
>             renpy.redraw(self, 0)
> 
>     def render(self, width, height, st, at):
>         if self.hovering:
>             return self.hover_image.render(width, height, st, at)
>         else:
>             return self.unhover_image.render(width, height, st, at)
> ```
>
> 调用:
>
> ```python
> add HoverChange("#fff", "#888")
> ```
>
> 调用此组件, 当鼠标不在此组件限定的 area (纵横 100 像素) 内时显示为纯白, 在此范围内时显示为灰. 我们可以通过传入`area` 参数来改变这个区间
>
> ---

### 		*d. 如何阻止事件传播到其他组件

> 在上面的代码里, 我们的按钮在鼠标按下就会立即相应, 但我们依然可以正常的点击其他按钮, 也就是说, 这次点击事件也被传输到其他可视化组件里了, 这显然是一个不合理的事情
>
> 在这个时候, 我们可以使用 `raise renpy.display.core.IgnoreEvent()` 来抛出一个异常, 此异常会阻止事件传输到其他的可视化组件里
>
> ```python
> class PressHoverChange(renpy.Displayable):
>     def __init__(self, active_image, negative_image, area=(100, 100)):
>         super(PressHoverChange, self).__init__()
>         self.active_image = renpy.displayable(active_image)
>         self.negative_image = renpy.displayable(negative_image)
>         self.area = area
>         self.is_active = False
> 
>     def event(self, ev, x, y, st):
>         old_state = self.is_active
> 
>         # 当鼠标在范围内按下时
>         if ev.type == pygame.MOUSEBUTTONDOWN and (0 < x < self.area[0] and 0 < y < self.area[1]):  
>             self.is_active = True
> 
>             # 因为 raise 的机制, 我们只能在 raise 前检测 state 是否发生变化
>             if old_state != self.is_active:
>                 renpy.redraw(self, 0)
> 
>             # 阻止事件传输到其他可视化组件
>             raise renpy.display.core.IgnoreEvent()
> 
>         # 当鼠标抬起并且控件处于按下状态时
>         if ev.type == pygame.MOUSEBUTTONUP and self.is_active:
>             self.is_active = True in pygame.mouse.get_pressed()
> 
>             if old_state != self.is_active:
>                 renpy.redraw(self, 0)
> 
>             # 阻止事件传输到其他可视化组件
>             raise renpy.display.core.IgnoreEvent()
> 
> 
>     def render(self, width, height, st, at):
>         if self.is_active:
>             return self.active_image.render(width, height, st, at)
>         else:
>             return self.negative_image.render(width, height, st, at)
> ```
>
> 调用: 
>
> ```python
> add PressHoverChange("#fff", "888")
> ```
>
> 此时, 只有鼠标左键按下并且处于 `area` 时, 组件的颜色才会从白色切换成灰色
>
> 试着写一个在区域内按下鼠标左键, 右键, 中键按下都会有不同图案的组件吧

---

## Stage 4: 实现一个实用的底边栏

>   在上文里我们已经介绍过生成可视化组件的基础方法, 在这节里我们将尝试实现对多个子组件进行管理, 也就是一个布局方式
>
>   最简单的布局方式就是横向排版布局, 底边栏就是一个很好的例子
>
>   ---

### 		a. 基础的实现方法

>   在这里, 我们定义一个底边栏类, 此类会根据 `item_spacing` 参数来自动调整子组件的间隔
>
>   ```Python 
>   class EasyQuickMenu(renpy.Displayable):
>      def __init__(self, *menu_items):
>          super().__init__()
>           self.items = tuple(renpy.displayable(i) for i in menu_items)  # 生成各个子控件
>           self.item_spacing = 200  # 每个控件的间隔
>           self.items_ypos = list(0 for _ in self.items)  # 每个控件的 y 坐标 ( 会更新 )
>           self.items_xpos = tuple(i * self.item_spacing for i in range(len(self.items)))  # 每个控件的 x 坐标
>   
>      def event(self, ev, x, y, st):
>           # 循环传入事件
>           for i in range(len(self.items)):
>               self.items[i].event(ev, x - self.items_xpos[i], y - self.items_ypos[i], st)
>   
>       def render(self, width, height, st, at):
>           # 循环绘制所有子组件
>          rv = renpy.Render(width, height)
>           for i in range(len(self.items)):
>               rv.blit(self.items[i].render(100, 100, st, at), (self.items_xpos[i], self.items_ypos[i]))
>           return rv
>   ```
>
>   调用:
>
>   ```python
>   add EasyQuickMenu("#fff", "#fff", "#fff", "#fff", "#fff")
>   ```
>
>   显示此组件, 应该会出现五个大小为`100x100`的白色的正方形 ( 大小为 `100x100` 是因为我在 `render` 函数里给子组件传入的 `width, height` 始终为 `100x100`, 没有特殊的意义 )
>
>   ---

### B. 按照子组件的实际大小布局组件

>   在上面的代码里, 每个组件的坐标都是通过 `spacing` 参数进行控制的, 并不会根据组件的大小自动调整, 这里我们就需要通过某种方法来获取子组件的大小
>
>   `Render` 函数有一个 `get_size` 方法, 这个方法可以获取到子组件实际`Render` 的大小, 通过上文我们现在都知道 `render` 函数会传入 `width, height` 参数, 但有时候, 我们尝试获取子组件的 `Render` 时传入的 `width, height` 参数和实际获取到的 `Render` 大小并不匹配, 例如 `Text` 对象, 编写下面的这段程序
>
>   ```python
>   a = Text("一个字体对象")
>   for i in range(10):
>   	size = (1920 / i, 1080 / i)
>   	text_render = a.render(*size, 0, 0)
>   	print("字体对象传入的 size 为: ", size)
>   	print("字体对象实际的 size 为: ", text_render.get_size())
>   ```
>
>   我们可以发现无论怎么改变传入的 `size`, 实际的 `size` 始终为一个固定值, 有些组件出于布局或者其他的要求会返回与传入值不同的大小. 我们创造自己的组件时也可以根据情况, 动态的变更组件 `Render` 的大小
>
>   所以, 我们可以在绘制子组件时记录各个子组件的 `size`, 再根据这个 `size` 来放置各个组件
>
>   ```python
>   class NeatQuickMenu(renpy.Displayable):
>       def __init__(self, *menu_items):
>           super().__init__()
>           self.items = tuple(renpy.displayable(i) for i in menu_items)  # 生成各个子控件
>           self.item_spacing = 20
>           self.items_ypos = list(0 for _ in self.items)  # 每个控件的 y 坐标 ( 会更新 )
>           self.items_xpos = list()
>   
>       def event(self, ev, x, y, st):
>           # 如果 xpos 并没有正确, 直接不接受此事件
>           if len(self.items_xpos) != len(self.items):
>               return
>           
>           for i in range(len(self.items)):
>               self.items[i].event(ev, x - self.items_xpos[i], y - self.items_ypos[i], st)
>   
>       def render(self, width, height, st, at):
>           rv = renpy.Render(width, height)
>           
>           # 子组件所在的 xpos
>           xpos = 0
>           
>           # 循环绘制所有子组件
>           for i in range(len(self.items)):
>               # 获取子组件的 render
>               render = self.items[i].render(width, height, st, at)
>               # 将此 render 绘制到 rv 上
>               rv.blit(render, (xpos, self.items_ypos[i]))
>               # 将此坐标加入到自己坐标记录里
>               self.items_xpos.append(xpos)
>               # 下一个组件的 xpos 就为此组件的 xpos + 固定的间距 + 当前子组件的宽
>               xpos += self.item_spacing + render.get_size()[0]
>   
>           return rv
>   ```
>

### 		c. 子组件无法被 `redraw` 重绘的问题

>   如果我们使用上面的代码时 `menu_item` 的入参是一些使用 `renpy.redraw` 来更新自身画面的组件时, 我们会发现他们调用的`renpy.redraw` 居然完全失效了 ( 例如传入的是 `Stage 2` 中的 `MovePicture`) , 此组件的子组件没法正常的被 `redraw`, 别人找我写可视化组件时我在这里懵逼了半天, 最后面发现了一个极其....难以评价的答案----
>
>   那就是不使用 `xxx.render(w, h, st, at)` 这个函数来获取子组件的 `Render`, 而是使用 `renpy.render` 这个奇妙的函数. 通过这个函数来渲染子组件会将此 `Render` 缓存到 `Renpy` 系统内某个不知名的地方, 也就是需要通过这个完全不透明的机制后, 此组件的子组件才能正常的调用 `redraw ` 来更新自己的图像 ( 不仅仅是这一个机制需要使用这个函数 ). 所以使用 `renpy.render` 来绘制图像多消耗一些性能, 但能将组件的一些特殊参数保存下来, 假如子组件本身具有一定的功能性, 出于保险起见, 我推荐使用 `renpy.render` 来将子组件绘制到此组件的 `Render` 上, 而那些不具有功能, 本身只负责提供基础图像的组件, 用 `render` 也足够了
>
>   我没在文档里找到过任何与此有关的内容, 你问我我是怎么找到的? 答案是在翻阅 `Renpy` 源码山穷水尽的时候我 `Ctrl C V` 了一个正常的组件, 逐层分析后定位到起作用的是这一句话.....
>
>   ```python
>   class RedrawableQuickMenu(renpy.Displayable):
>       def __init__(self, *menu_items):
>           super().__init__()
>           self.items = tuple(renpy.displayable(i) for i in menu_items)
>           self.item_spacing = 20
>           self.items_ypos = list(0 for _ in self.items)
>           self.items_xpos = list()
>   
>       def event(self, ev, x, y, st):
>           for i in range(len(self.items)):
>               self.items[i].event(ev, x - self.items_xpos[i], y - self.items_ypos[i], st)
>   
>       def render(self, width, height, st, at):
>           rv = renpy.Render(width, height)
>   
>           self.items_xpos.clear()
>           xpos = 0
>   
>           for i in range(len(self.items)):
>               # 使用新的函数获取 render
>               rend = renpy.render(self.items[i], 100, 100, st, at)
>               rv.blit(rend, (self.items_xpos[i], self.items_ypos[i]))
>               self.items_xpos.append(xpos)
>               xpos += self.item_spacing + render.get_size()[0]
>   
>           return rv
>   ```
>
>   调用
>
>   ```python
>   add EasyQuickMenu(MovePicture("#fff"), MovePicture("#fff"), MovePicture("#fff"), MovePicture("#fff"))
>   ```
>
>   此时应该会显示四个纯白的 `MovePicture` 组件
>

>   ---

### *d. event 函数的基础优化思路

> 在上面的代码里, 我们实现了一个布局组件基本应有的内容
>
> 在我们上面写过的组件里, 如果你曾往其中任意一个组件 `event` 函数里添加过 `print`来查看相关数据的话, 不难发现`event`函数的调用频率高的吓人, 屏幕的正常刷新, 鼠标每此的移动, 等等, 假如你的界面里存在100个按钮, 你可以想象一下, 明明只有一个按钮需要响应鼠标移动带来的 `hover`, 但所有的组件都被迫跑了一次 `event`, 在这样的极端案例下, `event` 函数的性能消耗是相当庞大的, 所以既然我们写的是一个布局, 那么我们就可以阻止部分 `event` 传入到子组件里, 以减少调用的次数
>
> 我这里的优化思路是, 当鼠标移动时, 会判定当前鼠标有没有从一个组件移动到另一个组件上, 如果当前覆盖的组件发生了变化时才给受影响子组件传入一次事件, 鼠标点击则是始终给当前覆盖着的组件传入, 这样我们就可以节省下大量的性能了
>
> ```python
> class QuickerQuickMenu(renpy.Displayable):
>  def __init__(self, *menu_index):
>      super().__init__()
>      self.items = menu_index
>      self.item_spacing = 200
>      self.items_ypos = list(0 for _ in self.items)
>      self.items_xpos = tuple(i * self.item_spacing for i in range(len(self.items)))
>      self.selected_index = -1
>      self.hovered_index = -1
> 
>  def event(self, ev, x, y, st):
>      # 当鼠标移动时
>      if ev.type == pygame.MOUSEMOTION:
> 
>          # 记录旧索引, 重置新索引
>          old_hover = self.hovered_index
>          self.hovered_index = -1
> 
>          # 如果鼠标在次可视化组件内并选中了一个组件, 更新当前选中的索引
>          # 这里的值是写死的, 仅仅是为了缩减字数
>          if 0 <= y <= 100:
>              self.hovered_index = int(x / self.item_spacing)
>              if (0 <= self.hovered_index < len(self.items)) is False:
>                  self.hovered_index = -1
> 
>          # 如果有当前覆盖和上次覆盖的对象不一样且上次确实覆盖了一个子对象, 向上次覆盖的子对象传入事件
>          if old_hover != self.hovered_index and old_hover != -1:
>              self.items[old_hover].event(ev, x - self.items_xpos[old_hover], y - self.items_ypos[old_hover], st)
>              renpy.redraw(self, 0)
> 
>          # 如果当前覆盖的对象不为空, 传入 event
>          if self.hovered_index != -1: 
>              self.items[self.hovered_index].event(ev, x - self.items_xpos[self.hovered_index], y - self.items_ypos[self.hovered_index], st)
> 
>      # 如果是鼠标按下事件
>      if ev.type == pygame.MOUSEBUTTONDOWN and self.hovered_index != -1:
>          self.selected_index = self.hovered_index
>          renpy.redraw(self, 0)
>          self.items[self.hovered_index].event(ev, x - self.items_xpos[self.hovered_index], y - self.items_ypos[self.hovered_index], st)
>          raise renpy.display.core.IgnoreEvent()
> 
>      # 如果是鼠标抬起事件
>      if ev.type == pygame.MOUSEBUTTONUP and self.selected_index != -1:
>          self.selected_index= -1
>          renpy.redraw(self, 0)
>          return self.items[self.hovered_index].event(ev, x - self.items_xpos[self.hovered_index], y - self.items_ypos[self.hovered_index], st)
>          raise renpy.display.core.IgnoreEvent()
> 
>  def render(self, width, height, st, at):
>      rv = renpy.Render(width, height)
>      for i in range(len(self.items)):
>          rend = renpy.render(self.items[i], 100, 100, st, at)
>          rv.blit(rend, (self.items_xpos[i], self.items_ypos[i]))
>      return rv
> ```
>
> 调用
>
> ```python
> init python:
>     # 一个用于打印出此组件接收到所有事件的组件
>     class ShowEvent(renpy.Displayable):
>         def __init__(self, image):
>             self.image = image
> 
>         def event(self, ev, x, y, st):
>             print(self, ev, x, y, st)
> 
>         def render(self, w, h, st, at):
>             return self.image.render(w, h, st, at)
>      
>     objs = tuple(ShowEvent("#fff") for _ in range(10))
> 
>     
> screen test:
>     default choice = False
>     
>     vbox:
>         textbutton "切换组件" action SetScreenVar("choice", not choice)
> 
>         if choice:
>             text "优化前的底边栏"
>             add RedrawableQuickMenu(*objs)
>         else:
>             text "优化后的底边栏"
>             add QuickerQuickMenu(*objs)
>     
>     timer 1.0 action Function(print, "----------------") repeat True
> ```
>
> 此处我们定义一个新的可视化组件`ShowEvent`, 它的作用是不断地将接收到的所有 `event` 打印到控制台上, 同时定义了一个界面, 这个界面有一个按钮, 按下时会切换优化前和优化后的底边栏, 每个底边栏都会显示10个 `ShowEvent` 对象, 另外我还定义了一个每秒执行一次的 `action`, 此 `action` 会在命令行上打印一条线, 优化前后调用的频率自行对比吧
>
> ---

## Stage 5: 颜色切换的文字

>   这里介绍一些更高级的方法来让自己的组件变得美观, 先讲讲这个组件的效果吧, 本身的字体是颜色A的, 此组件会重复的从左到右将字体颜色变成B, 同时填充一个颜色A的背景, 再往右边离开, 以此循环

### a. 如何实现裁剪效果

>   在文档里我们就可以直接查到这个函数, 这里我们直接引用文档的内容:
>
>   `subsuface(rect)`  [link](https://doc.renpy.cn/zh-CN/cdd.html#renpy.Render.subsurface)
>
>   >   返回一个`Render`对象，原`Render`对象的剪裁。
>   >
>   >   -   `rect`
>   >
>   >       一个 `(x, y, width, height)` 元组。
>
>   在下面的代码里, 我们先获取 `A` 的 `Render` 与 `B` 的 `Render`, 随后对时间轴以 `2` 进行取余来作为动画的循环周期  `( 0.0~2.0 )`, 然后显示 `A` 组件与被裁剪的 `B` 组件
>
>   至于 `B` 组件的裁剪, 我们可以这样想象一下: 有 `head`, `end` 两个点, `end`在第 `0.0~1.0` 秒里从最左移动到最右并在`1.0~2.0`秒里始终保持在最右端, `head`在`0.0~1.0`秒里保持在最左端并`1.0~2.0`秒里从最左端移动到最右端, 这两个点中间的大小就是 `B` 组件显示的大小, 具体的代码就在下面了
>
>   ```python
>   from typing import Iterable
>   
>   
>   class EasyStellaText(renpy.Displayable):
>       def __init__(self, text, font_size = 100, *args, **kwargs):
>           super().__init__(*args, **kwargs)
>           # 可视化组件
>           self.text = Text(text, color="#fff", size=font_size)
>           self.anti_text = Text(text, color="#aaa", size=font_size)
>   
>   
>       def render(self, width, height, st, at):
>           # 渲染处理
>           rv = renpy.Render(width, height)
>           text_render = self.text.render(width, height, st, at)
>           anti_text_render = self.anti_text.render(width, height, st, at)  
>   
>           # 获取B组件覆盖A组件的宽度
>           text_width = anti_text_render.get_size()[0]
>   
>           # 计算 B 组件显示的头和尾
>           cut_time = st % 2
>           head_pos = (cut_time - 1) * text_width if 0 < cut_time - 1 < 1 else 0
>           end_pos  = cut_time * text_width if 0 < cut_time < 1 else text_width
>   
>           # 将此 Render 进行裁剪
>           anti_text_render = anti_text_render.subsurface((head_pos, 0, end_pos, anti_text_render.get_size()[1]))
>   
>           # 先绘制 A 组件
>           rv.blit(text_render, (0, 0))
>   
>           # 再绘制 B 组件
>           rv.blit(anti_text_render, (head_pos, 0))
>   
>           renpy.redraw(self, 0)
>   
>           return rv
>   ```

### 		b. 给动画使用缓动曲线

>   缓动曲线是一种将区间重映射的函数, 这种函数能将线性的值变得非线性, 例如下面这条函数
>
>   ```python
>def slow_func(n):
>       if n <= 0.5:
>           return sqrt(n * 2) / 2
>       else:
>           return 1.0 - slow_func(1.0 - n)
>   ```
>
>   此时传入一段 0.0, 0.1, 0.2....1.0 的参数, 输出的数据为:
>
>   | 0.0   | 0.1   | 0.2   | 0.3   | 0.4   | 0.5   | 0.6   | 0.7   | 0.8   | 0.9   | 1.0   |
>   | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
>   | 0.000 | 0.224 | 0.316 | 0.387 | 0.447 | 0.500 | 0.553 | 0.613 | 0.684 | 0.776 | 1.000 |
>   
>   我们可以发现经过映射后的数值开头结尾快, 中间慢, 这就是缓动函数的原理
>   
>   https://easings.net/zh-cn, 这是一个常用缓动函数的预览查询网站, `Renpy` 中也预设有这些缓动函数, 具体的对照关系见这里: https://doc.renpy.cn/zh-CN/transforms.html#warpers
>   
>   这些函数在一个叫做 `_warper` 的模块里, 比如 `ease_quint`, 我们可以使用 `_warper.ease_quint` 来调用这个函数
>   
>   在上面的源码里修改 `head_pos` 和 `end_pos` 的结算方式, 给他们加上缓动曲线, 我们就可以看到我们的组件已经有了缓动效果, 试试不同的缓动曲线吧
>   
>   ```python
>   		# 将 render 函数中此句 
>           head_pos = (cut_time - 1) * text_width if 0 < cut_time - 1 < 1 else 0
>           end_pos  = cut_time * text_width if 0 < cut_time < 1 else text_width
>           
>   		# 更改为
>           head_pos = _warper.ease_quint(cut_time - 1) * text_width if 0 < cut_time - 1 < 1 else 0
>           end_pos  = _warper.ease_quint(cut_time) * text_width if 0 < cut_time < 1 else text_width
>   ```
>   
>   ---

### 		c. 通过 `canvas` 绘制动态的背景

>   我们都知道可以通过 `renpy.displayable("#fff")` 这种格式来获取一个单色的组件, 但有没有更好的办法来绘制一些简单的图形呢? 当然是可以的, `Renpy` 保留了 `pygame` 中 `draw` 模块的功能, 此功能可以帮助我们快速画出一些简单的图形, 文档的链接: https://doc.renpy.cn/zh-CN/cdd.html#renpy.Render.canvas
>
>   比如下面的例子, 它以极少的代码绘制了出一个圆, 一个矩形, 几条线:
>
>   ```python
>   def canvas_test(renpy.Displayable):
>       def __init__(self):
>           super().__init__()
>       
>       def render(self, w, h, st, at):
>           rv = renpy.Render(w, h)
>           # 获取 rv 的 canvas 对象
>           canvas = rv.canvas()
>           # 在 rv 上绘制矩形, 颜色为 (255, 0, 0), 位置为 (0, 0, w, h), 宽度为 3
>           canvas.rect((255, 0, 0), (0, 0, w, h), 3) 
>           # 在 rv 上绘制圆形, 颜色为 (0, 255, 0), 中心点为 (w/2, h/2), 宽度为4
>           canvas.circle((0, 255, 0), (w/2, h/2), width=4)
>           # 在 rv 上绘制多个点, 颜色为 (0, 0, 255), 收尾不拼接, 点的顺序为
>           # (0, 0) -> (0, h) -> (w, h) -> (w/2, h/2)
>           # 宽度为 2
>           canvas.lines((0, 0, 255), False, ((0, 0), (0, h), (w, h), (w/2, h/2)), 2)
>           return rv
>   ```
>
>   对于原本的组件, 我们可以这样在 `anti_text_render` 被 `blit` 前这样绘制一个纯白的背景:
>
>   ```python
>   # 在 rv 上绘制矩形, 
>   # 矩形的坐标为 (B组件的起始位置, 0)
>   # 长宽为 (B组件的末尾位置减去起始位置, B 组件的高度)
>   # 不设置 width, 也就是填充整个矩形
>   rv.canvas().rect((255, 255, 255), (head_pos, 0, end_pos-head_pos, anti_text_render.get_size()[1]))
>   ```
>
>   ---

### 		*d.   让动画在鼠标覆盖时触发, 离开时恢复

>   在上面内容里我们不难发现, 这个效果涉及到了动画的时间轴, 如果我们需要将 A 以一定的时间过渡到 B 并过渡回来, 并且这个动画的发生是有条件的, 那么拆解掉两个问题:
>
>   首先, 既然动画是可逆的, 那么我们可以定义一个 `0~1` 的参数, 动画从 A 到 B 的比例就为此参数的值, 此动画的发生的有条件的话, 我们就不可以使用 `event` 函数的 `st` 来确定动画已经发生的时间, 而是需要记录相邻两帧动画的时间戳来更新动画.
>
>   我个人一般会使用以下的模板来构建一个 动画可逆且动画以某种方式触发 的组件的动画效果
>
>   ```python
>   class Timeline(renpy.Displayable):
>      def __init__(self):
>          super().__init__()
>          # 上次更新此组件的时间
>          self.last_st = None
>         # 动画进行的百分比
>          self.anima_ratio = 0.0
>          # 动画完成的时间
>          self.complete_time = 0.5
>          # 动画是否进行的方向
>      	self.anima_direction = True
>   
>      def event(self, ev, x, y, st):
>          # 如果 last_st 并没有被赋值, 就将当前的 st 赋予 last_st
>          if self.last_st is None:
>              self.last_st = st
>   
>          # 如果时间轴更新了
>          if st != self.last_st:
>              # 储存旧的 ratio
>             old_ratio = self.anima_ratio
>   
>             # 更新动画进行的百分比
>              self.anima_ratio += (st - self.last_st) / self.complete_time * (self.anima_direction - 0.5) * 2
>             # 如果动画当前或上次完成度在 0% ~ 100% 之间时, 更新画面
>              if 0.0 < self.anima_ratio < 1.0 or 0.0 < old_ratio < 1.0: 
>                 renpy.redraw(self, 0)
>                  renpy.timeout(0.015)
>   
>              # 当前值超出范围则取0或1
>             if (0.0 < self.anima_ratio < 1.0) is False:
>                  self.anima_ratio = self.anima_ratio > 0
>   
>              # 更新 last_st
>              self.last_st = st
>   ```
>
>   对于 `anima_ratio` 更新的解释:
>
>    >   在相同的 `st` 下可能会调用多次 `event`, 所以更新 `st` 时需要判断当前 `st` 是否与之前的 `st` 不同
>    >
>    >   `st - self.last_st` 是获取两次更新间的时差
>    >
>    >   `/ self.complete_time` 是将时差除以完成时间以获取动画进行的比例
>    >
>    >    `(self.anima_forward - 0.5) * 2` 这里, 当 `self.anima_forward` 为 `True` 时值为 `1`, 当 `self.anima_forward` 为 `False` 时值为 `-1`, 这个值乘上动画的比例就可以控制动画的进退
>
>   一些细节上的问题 (看不懂可以跳过先, 这里是给对模板有问题的人看的)
>
>    >   为什么时间轴不写在 `render` 里呢? 首先, `render` 一般情况下并不会一直被调用, 就比如一个按钮在添加到屏幕上, 它只会在我鼠标覆盖到时才会更新画面对吧? 那么假设我们添加了这样的按钮, 在初始化时它的 `st` 为 `0`秒, 我在 `st` 为 `10.0`秒的时候才用鼠标覆盖此按钮, 也就是两次调用 `render` 函数的间隔为  `10.0` 秒, 由于 `last_st` 为 `0.0` 此时动画会直接显示`10.0`秒后的画面. 
>    >
>    >   此外, `event` 函数更新的频率决定了 `anima_ratio` 更新的频率, 假如 `event` 函数每秒只被调用 `1` 次, `render` 函数被调用 `60` 次, 即使 `render` 被频繁的调用, 但由于 `anima_ratio` 没有更新, 全都基于 `anima_ratio` 参数的动画将完全不会被更新, 所以这里需要使用一个名为 `renpy.timeout(n)` 的函数, 此函数会在 `n` 秒后重新调用此组件的 `event` 函数. 在上文里, 动画如果在进行着就会以每 `0.015` 秒一次的速度调用 `event` 函数来确保 `anima_ratio` 被更新了以及此组件被 `redraw` 了
>    >
>    >   这两问题是属于这个框架下的问题, 我们可以通过改变更新的框架来避免这个问题, 例如我们可以让动画发生的第一帧不更新 `anima_rate`, 而是只更新 `last_st` , 这样在第二帧里 `st` 的差就是正确的了, 使用 `render` 函数更新也没有任何问题, 但写完整的话代码太长了,  `event` 函数本身的调用频率足够高来保证帧之间的差是正常的, 我希望先介绍一种入门的, 简易的更新时间轴的方法.
>
>   那么下面是最终的实现了
>
>   ```python
>   from typing import Iterable
>   
>   
>   class EasyStellaText(renpy.Displayable):
>       def __init__(self, text, font_size = 100, *args, **kwargs):
>           super().__init__(*args, **kwargs)
>           # 可视化组件
>           self.text = Text(text, color="#fff", size=font_size)
>           self.anti_text = Text(text, color="#888", size=font_size)
>   
>           # 时间轴相关参数
>           self.last_st = None
>           self.anima_ratio = 0.0
>           self.complete_time = 0.5
>           self.is_hover = None
>   
>           # 供事件参考的参数
>           self.size = (font_size*len(text), font_size)
>   
>       def event(self, ev, x, y, st):
>           # 更新判断鼠标是否覆盖到了此组件上
>           if ev.type == pygame.MOUSEMOTION:
>               self.is_hover = (0 < x < self.size[0] and 0 < y < self.size[1])
>   
>           # 时间轴处理
>           if self.last_st is None:
>               self.last_st = st
>   
>           if st != self.last_st:
>               old_ratio = self.anima_ratio
>   
>               self.anima_ratio += (st - self.last_st) / self.complete_time * (bool(self.is_hover) - 0.5) * 2
>               if 0.0 < self.anima_ratio < 1.0 or 0.0 < old_ratio < 1.0: 
>                   renpy.redraw(self, 0)
>                   renpy.timeout(0.015)
>   
>               if (0.0 < self.anima_ratio < 1.0) is False:
>                   self.anima_ratio = self.anima_ratio > 0
>   
>               self.last_st = st
>   
>   
>       def render(self, width, height, st, at):
>           # 渲染处理
>           rv = renpy.Render(width, height)
>           text_render = self.text.render(width, height, st, at)
>   
>           # 如果 self.size 与此组件实际渲染的大小对不上, 更新self.size
>           if self.size != text_render.get_size():
>               self.size = text_render.get_size()
>   
>           # 如果动画为 0.0, 只显示组件 A
>           if self.anima_ratio == 0:
>               rv.blit(text_render, (0, 0))
>               return rv
>   
>           # 如果动画为 1.0, 只显示组件 B
>           elif self.anima_ratio == 1:
>               anti_text_render = self.anti_text.render(width, height, st, at)
>               rv.blit(anti_text_render, (0, 0))
>               return rv
>   
>           # 如果动画介于 0.0 ~ 1.0 里
>           elif 0 < self.anima_ratio < 1:
>               # 获取B组件覆盖A组件的宽度
>               mid = int(text_render.get_size()[0]*_warper.ease_quint(self.anima_ratio))
>   
>               # 获取B组件完整的 Render
>               anti_text_render = self.anti_text.render(width, height, st, at)
>               # 将此 Render 进行裁剪
>               anti_text_render = anti_text_render.subsurface((0, 0, mid, anti_text_render.get_size()[1]))
>   
>               # 先绘制 A 组件
>               rv.blit(text_render, (0, 0))
>               
>               rv.canvas().rect((255, 255, 255), (0, 0, mid, anti_text_render.get_size()[1]))
>               
>               # 绘制 B 组件覆盖到 A 组件上
>               rv.blit(anti_text_render, (0, 0))
>   
>               return rv
>   ```
>

---

## Stage 6: 使用注册语句快速调用组件

>   在上面的内容里, 我们已经可以很容易的编写出自己的可视化组件了, 但我们在调用时会特别麻烦, 此时我们就需要用更好的方法来调用自己编写的组件, 也就是本节的内容

### a.  什么是注册语句

>   官网的文档链接: https://doc.renpy.cn/zh-CN/screen_python.html#creator-defined-sl
>
>   简单来说就是我们可以通过这个语句来将可视化组件注册为 `Renpy` 脚本可以识别的关键字, 我认为官网的文档写的足够健全了, 请浏览完官网文档的内容再看下面的内容吧 ( 决不是偷懒, 是我自己的表达能力实在是没官网的好 )

### b.  注册一个可视化组件显示到屏幕上

>   现在让我们编写一个建议的可视化组件作为例子吧
>
>   ```python
>   python early:
>      # 定义一个可视化组件
>      class ShowColor(renpy.Displayable):
>          def __init__(self, color, pos=(0, 0), size=(100, 100)):
>              # 此组件必须传入一个 color 参数, pos 和 size 均有默认值
>              super().__init__()
>              self.image = renpy.displayable(color)
>          	self.size = size
>              self.pos = pos
>   
>          def render(self, w, h, st, at):
>              rv = renpy.Render(*self.size)
>              rv.blit(self.image.render(*self.size, st, at), self.pos)
>              return rv
>   
>      # 将 'show_color' 关键字定义为 ShowColor 组件, 此组件接收0个子组件
>      renpy.register_sl_displayable("show_color", ShowColor, 0
>           ).add_positional("color"  # 此组件有一个名为 color 的固定入参
>   		).add_property("size"  # 此组件有一个 size 特性
>           ).add_property("pos")  # 此组件有一个 pos 特性
>   
>   
>   screen test:
>      vbox:
>          spacing 20
>      	show_color "#fff"   # 调用 ShowColor 组件, color 为 "#fff"
>   
>      	show_color "#ddd"   # 调用 ShowColor 组件, color 为 "#ddd"
>   
>      	show_color "#aaa":   # 调用 ShowColor 组件, color 为 "#aaa"
>              size (200, 100)   # 此组件的 size 为 200, 100
>   
>      	show_color "#888":  # 调用 ShowColor 组件, color 为 "#888"
>              pos (0, -20)   # 此组件的 pos 为 200, 100
>   ```
>

### c. 使用 group 来添加多个参数

>   有时候, 我们的组件继承自其他的组件, 这个时候如果想注册一个语句并希望能不用挨个 `add_property` 父组件的每一个属性的话, 我们可以用 `add_property_group`来添加一些常用的属性集合, (文档: https://doc.renpy.cn/zh-CN/screen_python.html#renpy.register_sl_displayable.add_property_group), 这些属性集合可以帮我们节省点内容, 就比如下面这个例子:
>
>   ```python
>   python early:
>       class ShakeText(renpy.text.text.Text):
>           def __init__(self, text, shake_range=(10, 5), *args, **kwargs):
>               super().__init__(text, *args, **kwargs)
>               self.shake_range = shake_range
>       
>           def render(self, w, h, st, at):
>               obj = super().render(w, h, st, at)
>               rand = 1.0*randint(0, 628)/100
>               rv = renpy.Render(*obj.get_size())
>               rv.blit(obj, (sin(rand)*self.shake_range[0], cos(rand)*self.shake_range[1]))
>               renpy.redraw(self, 0)
>               return rv
>           
>       renpy.register_sl_displayable("shake_text", ShakeText, "", 0
>           ).add_positional("text"  # 固定参数
>           ).add_property("shake_range"  # 额外参数
>           ).add_property_group('text')  # text 参数组
>   
>   
>   screen test:
>       hbox:
>           shake_text "一个抖动的字体"
>           shake_text "一个很大的抖动字体" size 50
>           shake_text "一个很粗很抖的抖动字体" shake_range (50, 50) bold True
>   ```
>
>   上面的例子里 `size`, `bold` 均为 `add_property_group` 加上的

### *d. 接收子组件的注册语句

>   有时候我们希望当前组件可以容纳其他组件, 作为一个布局容器来使用, 我翻遍文档都没有找到这个内容, 于是拜访了源码后我得出了一个结论: 以 `renpy.displayable.layout.Container` 为基础来编写, 可以将此组件视为布局组件的基型, 如果不想要继承该组件的话, 你的组件里必须包含两个方法: `add` 和 `remove`, 这两个方法用于添加及减少子组件, 例如我们改造一下上面的 `ShakeText`
>
>   ```python
>   init python:
>       class ShakeLayout(renpy.Displayable):
>           def __init__(self, shake_range=(10, 5), *args, **kwargs):
>               super().__init__()
>               self.shake_range = shake_range
>               self.children = list()
>               self.offset = list()
>   
>           def render(self, w, h, st, at):
>               rv = renpy.Render(w, h)
>               self.offset.clear()
>   
>               rand = 1.0*randint(0, 628)/100
>   
>               for i in self.children:
>                   son_rv = renpy.render(i, w, h, st, at)
>                   pos = i.place(rv, sin(rand)*self.shake_range[0], cos(rand)*self.shake_range[1], w, h, son_rv)
>                   self.offset.append(pos)
>   
>               renpy.redraw(self, 0)
>   
>               return rv
>   
>           def event(self, ev, x, y, st):
>               if len(self.children) != len(self.offset):
>                   return
>   
>               for i in range(len(self.children)):
>                   self.children[i].event(ev, x - self.offset[i][0], y - self.offset[i][1], st)
>   
>           def add(self, d):
>               self.children.append(d)
>   
>           def remove(self, d):
>               self.children.remove(d)
>   
>   
>       renpy.register_sl_displayable("shake", ShakeLayout, "", 2)
>   
>       
>   screen shake_layout_test
>       fixed:
>           xpos 0
>           shake:
>               xpos 300
>               text "你干嘛~"
>               text "干什么!" xpos 200
>               textbutton "什么功能都没有噢" clicked NullAction() ypos 100
>           
>       fixed:
>           xpos 300
>           shake:
>               shake_range (50, 50)
>               text "这边晃得更厉害了!"
>               text "头好晕啊啊啊啊" ypos 50
>   ```
>
>   

---

## Stage Extra: 如何写好可视化组件

> 心得体会?

### a. 减少不必要的调用

### b. 多注意初始化的参数

### c. 善于利用现成的源码 (我写的button)

### d. 多注意 `restrat_interation`

> 
