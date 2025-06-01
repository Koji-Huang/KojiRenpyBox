"""renpy

init python:
"""

class InfoObj:
    # Info 数据基型
    def __init__(self):...
    # 将此 info 初始化到 model 上
    def init_model(self, model: Model, **kwargs) -> None:...
    # 将此 info 中的数据更新到 model 上
    def apply_uniform(self, model: Model, **kwargs) -> None:...
    # 拷贝该 info
    def __copy__(self) -> InfoObj:...


class TextureInfo(InfoObj):
    # 一个可视化组件, 也就是纹理, 没有时默认为 Null()
    displayable: any

    # 纹理的叠加颜色
    # 存在可视化组件时会被默认设置为 (0.0, 0.0, 0.0, 0.0)
    # 没有可视化组件时值会被默认设置为 (1.0, 1.0, 1.0, 1.0)
    base_color: tuple[float, float, float, float]
    
    # a 通道的乘算值
    alpha: float

    # rgb 通道的乘算值
    blend: float = 1.0

    # 值通道的乘方值
    pow: float = 0.1

    # 是否使用相对坐标
    relative_coord: bool = True

    def __init__(
        self, 
        displayable: Displayable = None, 
        color: tuple[float, float, float, float] = None, 
        alpha: float = 1.0, 
        blend: float = 1.0, 
        val_pow: float = 0.1, 
        relative_coord: bool = True
        ):...


class WithTextureInfo(InfoObj):
    # 这个 info 里都会带有一个 texture_info 对象
    # 并写好了一些针对 texture 的方法
    texture: TextureInfo

    def __init__(self, texture: TextureInfo=None):...


class LineInfo(WithTextureInfo):
    # 起始点
    start_pos: tuple[float, float]

    # 结束点
    end_pos: tuple[float, float]

    # 材质纹理
    texture: TextureInfo

    # 圆角的像素值
    round: float

    # 线条宽度
    width: float

    def __init__(
        self, 
        start_pos: tuple[float, float], 
        end_pos: tuple[float, float], 
        width: float = 10, 
        round: float = 0.0,
        texture: TexureInfo = None, 
        ):...


class RectInfo:
    # 大小
    size: tuple[int, int]

    # 圆角的像素值
    round: float

    # 为None时渲染实心, 否则表示为线条宽度
    width: int

    # 纹理参数
    texture: TextureInfo

    def __init__(
        self, 
        rect_area: tuple[int, int, int, int], 
        round: float = 0.0, 
        width: float = 0.0, 
        texture: TextureInfo = None
        ):...


class CircleInfo:
    # 圆坐标
    pos: tuple[int, int]

    # 为None时渲染实心, 否则表示为线条宽度
    width: int

    # 圆的弧度
    # 第一个值为弧的偏移角度
    # 第二个值为弧度(超过 2 pi 就是满圆, 默认为满圆)
    degree: tuple[float, float]

    # 圆角的像素值
    round: float

    # 纹理
    texture: TextureInfo


    def __init__(
        self, 
        pos: tuple[int, int], 
        r: float=20, 
        width: float=0, 
        degree: tuple[float, float] = (0, pi*2), 
        round: tuple = 0, 
        texture: TextureInfo=None
        ):..