"""renpy

init python:
"""

def mix(a, b, k):
    return a + (b-a) * k


class ParticleDust(renpy.Displayable):
    def __init__(self, image, mask, speed=1.0, center=None, lock=True):
        super().__init__()
        self.speed = speed
        self.center = center
        self.lock = lock

        # 1层图像层
        self.dust = DustLayer(image)

        # 3层粒子层
        self.particle = tuple(ParticleLayer(mask, image, randint=i, speed=1.0+i/5) for i in range(3))

    def render(self, w, h, st, at):
        # lock 的话超出时间轴的画面不播放
        if self.lock and st * self.speed > 1:
            return renpy.Render(w, h)
            
        t = st * self.speed % 1

        rv = renpy.Render(w, h)

        # 0.2~0.7 内图像以 dust 渐出
        dust_t = (t-0.2) / 0.5 if 0.2 < t < 0.7 else bool(t > 0.5) - (bool(t > 0.5) - 0.5) * 0.01

        dust = renpy.render(self.dust, w, h, dust_t, dust_t)
        pos = self.dust.place(rv, 0, 0, w, h, dust)
        
        # 计算图像的 center
        center = ((pos[0] + dust.get_size()[0] / 2) / w, (pos[1] + dust.get_size()[1] / 2) / h) if self.center is None else self.center

        # 绘制各个粒子层
        for particle in self.particle:
            particle.model.uniform("u_center", center)

            # 0.0~0.6 particle(fadeint) 0.6~0.9 (fadeout)
            during = 0.5
            if(t > 0.6): during = mix(0.5, 1.0, (t - 0.6)/(0.9 - 0.6)) if during < 0.9 else 1.0
            particle.model.uniform("u_anima_during", during)

            particle_rend = renpy.render(particle, w, h, t, t)
            particle.place(rv, 0, 0, w, h, particle_rend)


        return rv
