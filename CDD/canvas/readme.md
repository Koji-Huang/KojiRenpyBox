# canvas

canvas 通过 shader 绘制直线, 圆, 矩形, 支持圆角与描边

使用例请见目录下 Sample

<img src="readme.png" height="400" />

   演示视频: https://www.bilibili.com/video/BV1Ri7kzzERC/

---

# 组件类型:

canvas 的各个组件的定义在 canvas_ren.py 里面可以找到

## 基类

每一个 Canvas 组件都有以下参数:

| 参数名 | 数据类型 | 描述 | 默认值 |
| -------------------- | ---- | ---- | ---- |
| render_callback | Function | 渲染时的回调函数 | None |
| event_callback | Function | 时间回调函数 | None |
| info | InfoObj | 此组件的绘制信息 ( 见下文 ) | None |

## Line

line 组件有以下参数:

| 参数名 | 数据类型 | 描述 | 默认值 |
| -------------------- | ---- | ---- | ---- |
| start_pos | Iterable[int, int] | 起始坐标 | (0, 0) |
| end_pos | Iterable[int, int] | 终点坐标 | (0, 0) |
| width | float | 宽度 | 5 |
| round | float | 圆角像素 | 0.0 |
| texture | TextureInfo | 绘制纹理 | None |

## Rect

rect 组件有以下参数:

| 参数名 | 数据类型 | 描述 | 默认值 |
| -------------------- | ---- | ---- | --- |
| rect_area | Iterable[int, int, int, int] | 矩形的范围  (x, y, w, h) | (0, 0, 100, 100) |
| round | float | 圆角像素 | 0.0 |
| width | float | 描边的像素 | 0.0 |
| texture | TextureInfo | 绘制纹理 | None |

## Circle

circle 组件有以下参数:

| 参数名 | 数据类型 | 描述 | 默认值 |
| -------------------- | ---- | ---- | ---- |
| pos | Iterable[int, int] | 圆心 | (0, 0) |
| r | int | 半径 | 30 |
| width | float | 描边的像素 | 0.0 |
| degree | Iterable[float, float] | 需传入一个数组 ( 圆旋转的弧度, 圆的弧长(0~2pi) ) | (0, pi*2) |
| round | float | 圆角像素 | 0.0 |
| texture | TextureInfo | 绘制纹理 | None |

---

# Info 与 Texture

为了方便绘制多个类似的几何图形与传递同一份纹理的引用来减少渲染, 我使用一个自定义的类 InfoObj 来封装, 传递这些参数

## 组件 info

每个组件都有自己对应的 Info, 定义可以在 canvas_data_ren.py 里面找到

-   line -> LineInfo
-   rect -> RectInfo
-   circle -> CircleInfo

Info 的传参与组件的参数一致, 需要让一个组件使用一个 info 直接传参即可, 例如:

```python
default circle_info = CircleInfo((150, 75), r=50)

circle info circle_info
```

info 定义有 `__copy__` 函数来进行复制以及修改信息

```python
default circle_info = CircleInfo((150, 75), r=50)

circle info circle_info
circle info circle_info.__copy__(r=75)
circle info circle_info.__copy__(r=100)
```

## TextureInfo

由于不同组件类型的 info 并不互通, 因此我额外设计了一个通用的 TextureInfo, 作为组件 info 的一个参数进行传递, 例如:

```python
texture_info = TextureInfo("text.png")

line_info = LineInfo(start_pos=(0, 0), end_pos=(10, 10), texture=texture_info)
rect_info = RectInfo(rect_area=(20, 20, 10, 10), texture=texture_info)
circle_info = LineInfo(pos=(0, 0), r=50, texture=texture_info)
```

在这里, `line_info`, `rect_info`, `circle_info` 虽然是不同的组件, 但是他们都使用同一份纹理进行绘制

---

# Transform

为了方便制作一些非交互的动画效果, 我编写了一些 transform, 这些 transform 直接使用 shader 而不是自定义组件进行绘制, 但是他们依然可以传入 info 来对动画进行初始化, 他们的定义写在了 canvas_transform.rpy 里面, 动画的定义可以查看 sample_transform.rpy