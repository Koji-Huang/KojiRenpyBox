"""renpy

python early:
"""

class Dammu:
    def __init__(self, text: str="", show_st: float=None):
        self.text = text
        self.channel = None
        self.show_st = show_st


class DammuDisplay(renpy.Displayable):
    def __init__(self):
        super().__init__()
        # 弹幕池
        self.dammu_pool = tuple()
        # 渲染弹幕用的 Text
        self.dammu_render_text = Text("")
        # 弹幕的基础速度 ( 像素每秒 )
        self.dammu_basic_speed = 100
        # 每个字符/秒经过的像素
        self.each_char_speed = 15
        # [(可插入新弹幕的时间, 上一个弹幕离场的时间), ...]
        self.dammu_channel = list()
        # 当前的 st
        self.now_st = 0.0

    def add_dammu(self, dammus):
        if isinstance(dammus, Dammu): dammus = (dammus, )

        for dammu in dammus:
            speed = self.get_dammu_speed(dammu)
            width = self.render_single_dammu(dammu, 1920, 1080, 0.0, 0.0).get_size()[0]
            dammu.channel = self.insert_to_channel(dammu, speed, width)
        self.dammu_pool = self.dammu_pool + tuple(dammus)

    def insert_to_channel(self, dammu, speed, width):
        """
        @param dammu: 弹幕对象
        @param get_out_st: 弹幕的速度
        @param dammu_time: 整条弹幕的宽
        """
        if dammu.show_st is None:
            dammu.show_st = self.now_st
        
        dammu_time = width / speed
        get_out_st = dammu.show_st + 1920 / speed + dammu_time * 2

        # 尝试在现有的弹幕通道里插入
        for index, channel in enumerate(self.dammu_channel):
            if dammu.show_st > channel[0] and get_out_st - dammu_time > channel[1]:
                self.dammu_channel[index] = (dammu.show_st + dammu_time, get_out_st)
                return index

        # 没有的话就新建一个通道插入
        self.dammu_channel.append((dammu.show_st + dammu_time, get_out_st))
        return len(self.dammu_channel) - 1

    def render_single_dammu(self, dammu, w, h, st, at, tmp=None):
        if tmp is not None:
            if dammu.text in tmp.keys() and tmp[dammu.text].killed is False:
                return tmp[dammu.text]
            else:
                tmp[dammu.text] = self.render_single_dammu(dammu, w, h, st, at)
                return tmp[dammu.text]
    
        self.dammu_render_text.set_text(dammu.text)
        return self.dammu_render_text.render(w, h, st, at)

    def get_dammu_speed(self, dammu):
        return len(dammu.text) * self.each_char_speed + self.dammu_basic_speed

    def event(self, ev, x, y, st):
        # # 每 0.1 秒刷新一次
        renpy.timeout(0.015)
        self.now_st = st
        renpy.display.render.redraw(self, 0)

    def render(self, width, height, st, at):
        rv = renpy.Render(width, height)

        dead_dammu = list()  # 需要从弹幕池里移除的弹幕

        tmp_render = dict()

        for i in range(len(self.dammu_pool)):  # 从下标遍历弹幕池
            dammu = self.dammu_pool[i]

            text_render = self.render_single_dammu(dammu, width, height, st, at, tmp_render)

            # 获取弹幕所在的位置 x: ( 屏幕宽度 - (弹幕持续时间 * (每个字提供的速度 * 弹幕字数 + 弹幕基础速度)) )
            pos = (width - (st - dammu.show_st) * self.get_dammu_speed(dammu), (dammu.channel * 30) % height)

            if pos[0] < 0 - text_render.get_size()[0]: # 如果 -弹幕的坐标 < 弹幕渲染出来的宽度 (也就是弹幕已经发射到屏幕外了), 则移除
                dead_dammu.append(self.dammu_pool[i])
            else:
                rv.blit(text_render, pos)  # 不然就渲染这条弹幕

        if dead_dammu:
            self.dammu_pool = tuple(i for i in self.dammu_pool if i not in dead_dammu)

        return rv
