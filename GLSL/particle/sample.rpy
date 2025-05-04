# 带粒子的消失组件
screen sample_particle_dust:
    add ParticleDust(Fixed(Frame("test5.jpg", align=(0.5, 0.5), xysize=(600, 300)), ), "tex1.png")

# 粒子效果
screen sample_particle_easy:  # 简易测试
    add ParticleLayer("tex1.png")

screen sample_particle_left:  # 改变 Center 为左
    add ParticleLayer("tex1.png", center=(0.0, 0.5))

screen sample_particle_mix:  # 多个粒子层的效果
    add ParticleLayer("tex1.png", speed=1.0, color=(1.0, 0.0, 0.0, 0.0))
    add ParticleLayer("tex1.png", speed=1.2, randint=11451, color=(0.0, 1.0, 0.0, 0.0))
    add ParticleLayer("tex1.png", speed=1.3, randint=19198, color=(0.0, 0.0, 1.0, 0.0))

screen sample_particle_from_img:  # 根据某个图片取颜色的效果
    add Transform(Frame("test5.jpg"), alpha=0.25)
    add ParticleLayer("tex1.png", Frame("test5.jpg"), center=(0.5, 0.0), speed=0.2)

# 消失效果
screen sample_dust:
    add DustLayer("test5.jpg")
