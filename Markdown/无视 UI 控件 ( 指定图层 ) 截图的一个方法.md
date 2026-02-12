# 无视 UI 控件截图的一个方法

这个文档的内容是通过访问 SceneList 来指定图层进行截图的内容
里面包含了我追踪整个问题的过程, 虽然很啰嗦吧hhhhhh

## 闲话

本人之前因为苦 隐藏UI截图 久矣, 就已经研究出了这个方法. 然而就在我研究出这个妙妙方法后的一个版本, 8.3.0, 我们迎来了 `config.pre_screenshot_actions` 配置项, 此时我以为我刚写的东西下一个版本官方就出了支持而大哭大闹 ( bushi ), 也就没有想着分享思路了.

但是在今天有人来询问相关问题时我发现 `config.pre_screenshot_actions` 配置项...并不是很好用, 至少我是没弄懂, 而且也有其他的没弄懂要怎么用的人, 思来想去. 还是分享我之前的思路, 开启本周的 `Renpy` 大学习吧

---

## 使用方法

代码

```python
class CustomScreenshotAction(Action):
    def __init__(self, target="master"):
        super().__init__()
        # 我们这里默认获取 master 图层
        self.target = screen_target
        
    def __call__(self):
        try:
            print(f"Try to save layer <{self.target}>")
            
            # 获取当前 context 的 scene_list
            # 然后通过 make_layer 函数获取 指定图层 的所有可视化组件
            # 并组合到了同一个可视化组件上, 返回给 tmp 
            tmp = renpy.display.scenelists.scene_lists().make_layer(self.target, renpy.game.interface.layer_properties[self.target])
            
            # 保存到本地, self.target+".png" 就是保存的路径
            renpy.render_to_file(tmp, self.target+".png", 1920, 1080, 0.0, 0.0)
            
            print(f"Layer <{self.target}> Save Success")
        except:
            print(f"Save layer {index} failure")
```

调用

```python
textbutton "尝试保存 master 图层" action CustomScreenshotAction()
```

实际上起作用的也就是 `__call__` 函数里的两句话, 我把他们封装到了一个 `Action` 里方便调用而已 (

`target` 参数是截屏目标的图层 ( https://doc.renpy.cn/zh-CN/displaying_images.html#layer )

---

## 解题思路

由于我解决这个问题的时间实在是有点古早 ( 在 2024/11/1 ), 所以我只能大概的逆推一下思路, 总之就是给各位一个参照了 (

### 截图

>   最开始我是从 `renpy.screenshot` 函数入手的, 它的源码是
>
>   ```python
>   def screenshot(filename):
>       return renpy.game.interface.save_screenshot(filename)
>   ```
>
>   然后查看 `renpy.game.interface.save_screenshot` 的源码
>
>   ```python
>   def save_screenshot(self, filename):
>       window = renpy.display.draw.screenshot(self.surftree)
>       if renpy.config.screenshot_crop:
>           window = renpy.display.scale.smoothscale(window, (renpy.config.screen_width, renpy.config.screen_height))
>           window = window.subsurface(renpy.config.screenshot_crop)
>       try:
>           renpy.display.scale.image_save_unscaled(window, filename)
>           if renpy.emscripten:
>               emscripten.run_script(r'''FSDownload('%s');''' % filename)
>           return True
>       except Exception:
>           if renpy.config.debug:
>               raise
>           return False
>   ```
>
>   阅读代码, 不难发现关键的东西是 `self.surftree`

### surftree

>   要追踪 `surftree`, 我们要先追寻一下 `interface` 这个参数, 在 `renpy.game.py` 里我们可以看到
>
>   ```python
>   # The interface that the game uses to interact with the user.
>   interface = None # type: Optional[renpy.display.core.Interface]
>   ```
>
>   然后去看 `renpy.display.core.py`, 我们可以在里面查到 `Interface` 对象, 也可以查到 `save_screenshot` 函数是 `Interface` 对象的方法. 这个时候我们可以看到 `surftree` 参数的由来了
>
>   ```python
>   surftree = renpy.display.render.render_screen(
>       root_widget,
>       renpy.config.screen_width,
>       renpy.config.screen_height,
>       )
>   ```
>
>   而这里, `surftree` 与 `root_widget` 有关, 然后 `root_widget` 是函数 `draw_screen` 的入参
>
>   所以检索 `draw_screen`, 我们发现这东西和一个叫做 `root_widget` 的变量有关
>
>   然后我们发现这个变量经常通过一个 `add_layer` 函数来修改自己
>
>   ```python
>   def add_layer(where, layer):
>       scene_layer = scene[layer]
>       focus_roots.append(scene_layer)
>       if (self.ongoing_transition.get(layer, None) and
>               not suppress_transition):
>           trans = instantiate_transition(layer, self.transition_from[layer], scene_layer)
>           transition_time = self.transition_time.get(layer, None)
>           where.add(trans, transition_time, transition_time)
>           where.layers[layer] = trans
>       else:
>           where.add(scene_layer)
>           where.layers[layer] = scene_layer
>   ```
>
>   我们不难看出 `add_layer` 函数涉及到了一个叫做 `scene` 的参数

### scene

>   查找 `scene`, 我们可以看到它的代码是 `scene = self.compute_scene(scene_lists)`
>
>   查询调用函数的入参 `scene_lists`, 可以找到 `scene_lists = renpy.game.context().scene_lists`, 打印它, 可以得到 `<renpy.display.scenelists.SceneLists object at 0x00000000078a0070>`, 所以定位这个类是在 `renpy.display.scenelists.py` 里
>
>   查看它的属性后我得出了结论, 这个类就是整个渲染树的大图层管理类, 于是我对这个类进行了研究
>
>   最后发现, 通过 `SceneLists ` 类的 `make_layer` 方法可以直接获取到"指定 `layer` 上的所有可视化组合而成的一个可视化组件"
>
>   上面 `scene` 参数调用的 `compute_scene` 函数里我们也而已找到对 `make_layer` 的引用
>
>   ```python
>   def compute_scene(self, scene_lists):
>       """
>       This converts scene lists into a dictionary mapping layer
>       name to a Fixed containing that layer.
>       """
>       rv = { }
>       
>       for layer in renpy.display.scenelists.layers:
>           d = scene_lists.make_layer(layer, self.layer_properties[layer])
>           rv[layer] = scene_lists.transform_layer(layer, d)
>           
>       root = renpy.display.layout.MultiBox(layout='fixed')
>       root.layers = { }
>       
>       for layer in renpy.config.layers:
>           root.layers[layer] = rv[layer]
>           root.add(rv[layer])
>           
>       rv[None] = root
>       
>       return rv
>   ```

### 最后的实现

>   看完上面的推理, 也就明白该如何获取图层上可视化组件的内容了. 最终的实现就是:
>
>   先通过 `renpy.display.scenelists.scene_lists()` 获取当前界面的 `SceneLists`
>
>   然后通过 `make_layer` 方法生成指定图层的可视化组件
>
>   再通过[`renpy.render_to_file`](https://doc.renpy.cn/zh-CN/screenshot.html#renpy.render_to_file) 将这个可视化组件渲染到本地
>
>   也就实现了 无视 UI 控件 ( 指定图层 ) 截图

### 小 tip

>   首先, 我使用了 inspect 库来快速查阅函数的源码, 这个非常重要, 通过 `getsource` 函数能直接获取未编译的源码, 也就可以省去一些找源文件查源码的时间了
>
>   ```python
>   def show_code(func):
>       import inspect
>       print(inspect.getsource(func))
>   ```

### 

