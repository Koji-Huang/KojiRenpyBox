"""renpy

python early:
"""
 
from math import sin, cos

class NormalPicture(renpy.Displayable):
    def __init__(self, image):
        super().__init__()
        # 获取 Image 对象
        self.image = renpy.displayable(image)

    def render(self, width, height, st, at):
        # 获取 Image 对象的 Render
        image_render = self.image.render(width, height, st, at)

        return image_render  # 直接返回这个 Render
    

class MovePicture(renpy.Displayable):
    def __init__(self, image):
        super().__init__()
        self.image = renpy.displayable(image)
        self.pos = (0, 0)

    def render(self, width, height, st, at):
        # 创建一个新的 Render 来放置 image 的 Render
        rv = renpy.Render(width, height)  

        # 获取 image 的 Render
        image_render = self.image.render(width, height, st, at) 

        # 坐标利用三角函数, 以时间为轴进行画圆
        self.pos = (sin(st) * 100, cos(st) * 100)

        # 将 image 的 Render 绘制到新的 Render 上
        rv.blit(image_render, self.pos)

        # 以尽可能快的速度重新绘制此组件
        renpy.redraw(self, 0)

        return rv


class FadePicture(renpy.Displayable):
    def __init__(self, image):
        super().__init__()

        # 创建一个 image 对象
        self.image = renpy.displayable(image)

        # 创建一个子对象为 image 的 Transform 对象
        self.transform = Transform(self.image)

    def render(self, width, height, st, at):
        # 改变 Transform 的 alpha 值
        self.transform.alpha = st % 1

        # 获取 Transform 的 Render
        transform_render = self.transform.render(width, height, st, at)

        renpy.redraw(self, 0)

        return transform_render  # 返回这个 Render


class MoveFadePicture(renpy.Displayable):
    def __init__(self, image):
        super(MoveFadePicture, self).__init__()
        self.image = renpy.displayable(image)
        self.transform = Transform(self.image)
        self.pos = (0, 0)

    def render(self, width, height, st, at):
        rv = renpy.Render(width, height)

        self.transform.alpha = st % 1
        transform_render = self.transform.render(width, height, st, at)

        self.pos = (sin(st) * 100, cos(st) * 100)
        rv.blit(transform_render, self.pos)

        renpy.redraw(self, 0.015)

        return rv

