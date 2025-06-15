# 自定义 `Live2D` 组件动作的一些思路

---

`Renpy` 官方的 `Live2D` 组件提供了 `blend_parameter` 来混合单个动作却没有提供一个自定义混合动作的接口, 很巧的是我要用到了, 在吃了几个晚上源码的史后(以前受人委托研究过这个模块, 但当时并没有成功), 就有了这篇文章

首先, 先解释一下 `Renpy Live2D` 源码内的重要模块

```python
class Live2DExpression(object)  # 用于合成参数的类

class Live2DCommon(object):  
    """
    让同一个 Live2D 文件使用共同参数的类,
    也就是说, Live2D 文件的信息是保存在这个类里而不是某个全局变量里的
    """
    
    
    # attributes 参数储存了已知的动作参数, 我们需要查询某个动作是否存在是可以来这里查询
    attributes: set[str, ..., ...]
    
    
    """
    motions 参数储存了该 Live2D 文件的动作
    Motion 对象有一个 get 方法, 该方法接收 (st, fade_st, do_fade_in, do_fade_out) 这些参数
    并返回该动作在这些时间下对应的 Paramter 参数
    """
    motions: dict[str: Motion, ...]


class Live2D(renpy.display.displayable.Displayable):
    """
    我愿称之为调用 Live2DCommon 的组件, 同时也是提供接口的组件
    """
    
    # 此 Live2D 的 Common
    common: Live2DCommon
    
    # 更新 common 状态来达到更新组件状态的函数
    def update(self, common, st, st_fade)
    
    # 直接更新组件参数的函数 https://doc.renpy.cn/zh-CN/live2d.html#blend_parameter
    def blend_parameter(self, name, blend, value, weight=1.0):
```

我们先看看 `Renpy` 源码是怎么将动作应用到组件上的吧, 这部分代码在 `class Live2D - update` 函数里

```python
# Apply the motion.

# 获取各个 motion 的 Paramter
motion_data = motion.get(st, st_fade, do_fade_in, do_fade_out)

# 遍历各个参数
for k, v in motion_data.items():

    kind, key = k
    factor, value = v

    if kind == "PartOpacity":
        common.model.set_part_opacity(key, value)
    elif kind == "Parameter":
        # 应用参数到 common 上
        common.model.set_parameter(key, value, factor)
    elif kind == "Model":
        # 应用参数到 common 上
        common.model.set_parameter(key, value, factor)
```

`motion` 参数为一个 `Motion` 对象, `common` 就是该组件自己的 `common`, `common` 对象的 `model` 参数就是 `Live2D` 模型的渲染模型, 这里是把参数逐个应用到该模型上

看懂了上面的内容, 我们就可以自己实现一个改变动作的效果了, 我们可以通过传入 `update_function`(https://doc.renpy.cn/zh-CN/live2d.html#Live2D 下的 `update_function` ) 来修改动作的效果, 这个函数的结算发生在上面的代码之后, 例如:

```python
def update_function(obj, st):
    common = obj.common
    motion = common.motions

    # 获取组件的动作参数
    attributes = obj.common.attributes
    
    # 随机一个表情
    target = attributes[randint(len(attributes))]
    if target == 'null': target = 'still'
    
    # 获取这个表情进行了 3 秒钟的参数
    motion_data = motion[target].get(3.0, 0, 0, 0)

    # 将参数应用到模型上
    for k, v in motion_data.items():

        kind, key = k
        factor, value = v

        if kind == "PartOpacity":
            common.model.set_part_opacity(key, value)
        elif kind == "Parameter":
            # 最好使用 Live2D 对象的 blend_parameter 来应用参数
            # 而不是 update 函数里的 common.model.set_parameter
            obj.blend_parameter(name=key, value=value, weight=0.5, blend="Add")
        elif kind == "Model":
            obj.blend_parameter(name=key, value=value, weight=0.5, blend="Add")

    # 立即更新
    return 0.0
```

将此函数传入组件内, 此时应该看到一个不停切换动作的 `Live2D` 组件. 此外需要注意的是, 每次 `interaction` 后 `st` 轴都会重置, 所以如果考虑一些高级效果的话, 我建议建类或者去研究一下 `Live2DState` 对象, 该对象会保留 `old`, `new` 的 `Live2D` 对象来保证动作连贯