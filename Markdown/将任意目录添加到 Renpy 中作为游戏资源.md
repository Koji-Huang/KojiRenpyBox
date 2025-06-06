# 将固定的外部目录添加到 `Renpy` 中作为游戏资源

---

## 使用方法

>   在打包好游戏内 `renpy` 文件夹下的 `loader.py` 里添加如下代码 ( 也就是修改 `SDK` )
>
>   ```python
>   def scan_outer_resource(add, seen):
>   
>     files = game_files
>   
>     outer = "xxx"
>   
>     for each in walkdir(outer):
>         add(outer, each, files, seen)
>   
>   scandirfiles_callbacks.append(scan_outer_resource)
>   ```
>
>   这部分代码应该添加在 `scandirfiles_callbacks` 被定义后( VS Code 随手一搜就知道了 ), `xxx` 为外部目录的路径
>
>   例如:
>
>   我们在游戏外有一个 `D:\\resource\\` 文件夹, 这个文件夹里有如下文件
>
>   ```
>   | resource
>   |--- image_aaa.png
>   |--- clone_script.rpy
>   ```
>
>   在游戏启动后
>
>   ```
>   | resource
>   |--- image_aaa.png
>   |--- clone_script.rpy
>   |--- clone_script.rpyc
>   ```
>
>   此时该文件夹下的所有内容都被 `Renpy` 扫描并存入了索引, `clone_script.rpy`也生成了`rpyc`缓存
>
>   此时 `resource` 文件夹中 `image` 的引用为 `image aaa = "image_aaa.png"` 而不是 `image aaa = "resource\image_aaa.png"`

## 原理

>   我们来逐行解读代码中的各个参数

### game_files

>   所有的游戏文件的索引, 保存在 `game_files` 里的索引等效于该文件存放在 `game` 文件夹下, 所以我们将外部资源载入到此文件里就可以保证资源被正常加载
>
>   一个新项目的 `game_files` 参数:
>
>   ```python
>   (
>       ("xxx\NewProject\game", "gui/bar/bottom.png")
>       ("xxx\NewProject\game", "gui/bar/left.png")
>       ("xxx\NewProject\game", "gui/bar/right.png")
>       ("xxx\NewProject\game", "gui/bar/top.png")
>       ("xxx\NewProject\game", "gui/bubble.png")
>       ...
>       ("xxx\NewProject\game", "screens.rpy")
>       ("xxx\NewProject\game", "screens.rpyc")
>       ("xxx\NewProject\game", "script.rpy")
>       ("xxx\NewProject\game", "script.rpyc")
>       ("xxx\NewProject\game", "SourceHanSansLite.ttf")
>       ("xxx\NewProject\game", "tl/None/common.rpym")
>       ("xxx\NewProject\game", "tl/None/common.rpymc")
>   )
>   ```
>
>   与之相对的是 `common_files`, 这里面的索引为 `Renpy`  引擎内 `common` 文件的索引, 启动优先级会更高
>
>   *一开始我定义了一个 `outer_files`, 但是发现定义在 `outer_files` 里的文件即使使用了自己写的 `file_open_callbacks` 也无法被正常加载, 然后联想到了 `Renpy` 里各个模块那极高的耦合性后我试着改成 game_files, 嗯, 果然成了 ( )*

### walkdir

>   `walkdir` 函数为定义在 `loader.py` 的一个函数, 具体作用就是遍历文件夹获取相对于传入目录的所有子文件的路径, 比如下面有这么个文件夹:
>
>   ```
>   D:
>   |--- image
>   |----|--- a.png
>   |----|--- gui
>   |----|----|--- b.png
>   ```
>
>   如果我们使用 `walkdir("D:\image")` 那么该函数传回的参数就为
>
>   ```
>   (
>   	("D:\image", "a.png")
>   	("D:\image", "gui\b.png")
>   )
>   ```
>
>   这些参数会存到对应的 files 里

### add 和 seen

>   这两个参数都被定义在 `loader.py` 的 `scandirfiles` 函数里, 这个函数是扫描所有文件的函数, 在调用时, 他会调用各个回调函数来扫描文件
>
>   ```python
>   def scandirfiles():
>       """
>       Scans directories, archives, and apks and fills out game_files and
>       common_files.
>       """
>   
>       seen = set()
>   
>       def add(dn, fn, files, seen):
>   
>           fn = unicode(fn)
>   
>           if fn in seen:
>               return
>   
>           if fn.startswith("cache/"):
>               return
>   
>           if fn.startswith("saves/"):
>               return
>   
>           files.append((dn, fn))
>           seen.add(fn)
>           loadable_cache[unicodedata.normalize('NFC', fn.lower())] = True
>   
>       for i in scandirfiles_callbacks:
>           i(add, seen)
>   ```
>
>   理解他们并不难, 总之 `add` 就是用于给搜索 `callback` 一个接口将 `dn`(父路径), `fn`(子路径) 添加到 `files`(比如`game_files`) 里的接口, 而 `seen` 是用于查重的一个集合

### scandirfiles_callbacks

>   这个参数在上面客串过了, 也就是用于系统检索所有文件的函数的列表, 查看 `loader.py` 文件里可以发现存在四个 `callback` 被添加到了这个列表里
>
>   >   `scandirfiles_from_apk`: 在安卓下检索 `APK` 包内
>   >
>   >   `scandirfiles_from_remote_file`: 如果提供的话, 检索可下载的文件
>   >
>   >   `scandirfiles_from_filesystem`: 检索文件系统下的文件
>   >
>   >   `scandirfiles_from_archives`: 检索归档文件 (`rpa`等) 的索引
>
>   此外还有一个 `file_open_callbacks`, 这个 `callback` 是用于读取文件并返回读取后文件信息的回调函数, 也就是对各个文件读取的 `I` 接口, 返回的是字节流对象, 它也有对应的四个回调函数, 但因为上面的代码兼容其中的 `load_from_filesystem`, 所以不需要编写一个额外的 `callback` 了
>
>   *其实我一开始就是编写了一个 callback 来支持读取的, 但是在我调试半天一个 I\O 错误后发现问题不出在这里并且根本不用写这个回调的时候, 气笑了*

### 重新看源码

>   ```python
>   # 定义函数
>   def scan_outer_resource(add, seen):
>   
>      # 定义 files 为 game_files 的引用
>      # 我们需要将外部资源载入到游戏资源索引里
>      files = game_files
>   
>      # 外部资源路径
>      outer = "xxx"
>   
>      # 获取外部资源下的所有子文件的路径
>      for each in walkdir(outer):
>   
>          # 将外部资源文件添加到 game_file 里
>          add(outer, each, files, seen)
>   
>   
>   # 向检索文件回调函数队列中添加我们定义的函数
>   scandirfiles_callbacks.append(scan_outer_resource)
>   ```

----

## 最后

>   本周的 `Renpy` 大学习已完成 ( )
>
>   在安卓下该方法也可用, 也就是说, 对于安卓的 `Renpy` 应用, 我们可以把拓展的包体放置在游戏包体外的地方引用, 一开始就是有人找我想办法在安卓实现这个功能, 好在找出路子了 ( )
>
>   虽说我这里说是固定, 但我们可以编写一个 `config` 什么的在 `loader.py` 里面读取来实现动态获取, 但需要注意的是, 载入包体的时间发生在引擎启动阶段, 进入游戏后不可修改 ( 不过 `Shift+R` 刷新缓存倒是可以, 总之就是让 `loader.py` 重新跑一遍的就行 ).
>
>   另外, 打包好的包体里的文件是拷贝自 `renpy-xxx-sdk\renpy` 里的, 如果你改动 `SDK` 里 `loader.py` 的源码的话, 可以省去每次打包后重新修改 `loader.py` 的时间, 但同时你使用此 `SDK` 运行, 生成的所有代码都会带有这个语句, 我自己为了测试这个代码新下载了一个 `Renpy` 和一整套的安卓套件 ( 心疼我的机场流量 )
>
>   `loader.py` 这个文件非常有趣, 通过修改他就可以轻松达到加密游戏文件, 支持新的存档格式, 以及这次添加外部资源路径的效果, 但很多人都不喜欢看源码....包括这次写的加载也是不喜欢看源码导致的后果, 这就是所谓的"脏活累活"吗. 唉, 真麻烦呐---