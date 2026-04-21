说在前面
---

这, 是一个高三走读生; 这, 是广西三月三的四天假期(2天自修2天放假但是我决定2天自修宅家). 在高三学期闷太久了以及心情很不好后以及浪费了一天的时间后, 这个人决定研究点以前的课题解解闷. 这个课题就是很久以前就研究过的, 如何把 renpy 的 py 脚本编译成 pyd 格式. 然后研究了两天后, 在各种神秘直觉的作用下, 误打误撞的编译成功了. 然后在最后一天里确定了编译的最少需要的依赖和环境后, 又花了一个工作日的晚上把这篇文档写了出来

需要说明的是, 这份编译方案是希望给一些因为引用了 C 模块或者预编译了标准 Python 环境的模块无法在 Renpy Python 上运行提供一个可能的解决方案, 例如 numpy 等. 理论上在弄懂了为什么标准库是怎么无法和 Renpy 兼容后再去做那样的事情就已经很简单了, 但是因为我已经没有时间继续做这件事了, 我也只好先写这篇方案出来供大家参考. 去编译 numpy 中的那些库的工作就先搁浅或者大家来干

需要注意的是, 有些库并不只是需要从 py 编译成 pyd 那么简单, 还需从 c 编译到 pyd ( 这个我还没有进行探索 ), 例如 numpy 就是, 但是在我实验着去调用的时候已经确定了就是那些预编译的 pyd 库导致的问题, 理论上使用下文提到的提取库的方案拿提取出来的源文件去替换掉编译时使用的源文件就可以完全做到兼容 numpy 以及任意第三方库了

**注: 转载, 引用以及使用都请务必表明出处, 如果这对你有所帮助请给我一个 Star ( )  这对一个没有什么精神支柱的高三生来说真的很重要**


系统环境
---

## 一个与你使用的 `Renpy` 版本匹配的 `Python`

需要注意的是, 最好不要使用 `Renpy` 的 `Python` 进行编译工作, 而是使用 `Python` 官网下载的 `Python`. 此外, 这个下载下来的 `Python` 也会被进行一定程度的修改, 所以请不要用作系统环境, 推荐安装一个后 `Ctrl CV` 到一个独立的目录里面供编译使用. 以及记得安装 Cython 库
*下文对这份 `Python` 简称 '`Python` 环境'*

## 一份发行版状态下的工程文件

也就是把你的工程打包好了先再做后面的工作. 另外, 在构建时最好使用的是 `Windows` 选项而不是 `PC: Windows and Linux` 选项, 因为后者会带有不止一个 `Python` 版本的 `dll`
*下文对这份工程文件简称'工程'*

## `Windows` 环境下的 `Microsoft C++ Build Tools` 工具

这是为了编译提供一个基础的编译环境, 该工具属于 `Visual Studio` 开发组件的一部分, 虽然大可以选择 `Python` 构建时必须的几个包体就好, 但是这边仍然建议使用 `Visual Studio Installer` 直接安装一个最新的 `Community` 版本

---
准备工作
---

## 获取 Renpy Python 对应的库文件

如果你不希望自己提取这份文件而是速成的话, 可以下载我提取的版本(在 Markdown 的目录里面), 但是如果你希望自己提取一份, 请参照此处的教程  

> 提取所需要的额外系统环境:
> 
> - `Linux` 环境下的 `gendef`[^why_linux_gendef] 工具, 以及相应的系统环境. 我个人推荐在 `Windows` 下安装 `MSYS2`[^msys_install] 作为一个轻量的 `Linux` 环境来调用 `gendef` 工具[^why_msys]
> - `x64 Native Tools Command Prompt for VS 2026` - 提供 `lib` 工具 ( 这里的 `2026` 对应的是版本号 ), 如果你在上面安装过一个完整的 `Visual Studio` 的话, 这个命令行工具会一同携带有

首先, 在你的工程文件里可以找到 `lib\py3-windows-x86_64\libpython3.12.dll` 这个文件 ( 老版本的 `Renpy` 为 `lib\py3-windows-x86_64\libpython3.9.dll` ), 将这个文件复制到任意地方, 使用 `gendef` 工具提取出 `.def` 文件
```powershell
> gendef libpython3.12.dll
* [libpython3.12.dll] Found PE+ image
```

然后使用 `x64 Native Tools Command Prompt for VS 2026` 的 `lib`[^lib_tool] 工具生成对应的 `.lib` 文件
```powershell
> lib /def:librenpython.def /out:librenpython.lib
Microsoft (R) Library Manager Version 14.51.36231.0
Copyright (C) Microsoft Corporation.  All rights reserved.

  正在创建库 librenpython.lib 和对象 librenpython.exp
```

## 使编译时使用的库文件是 Renpy 的文件

我们都知道 `Renpy Python` 是被魔改过的, 这个魔改甚至能让正常的 `Python` 打包出来的 `PYD` 没法被` Renpy Python` 正常的调用. 所以我们需要做的就是, 让正常的 `Python` 变成 ` Renpy Python` 的样子, 这样就可以打包出适配 `Renpy` 的 `pyd` 了 ( NTR啊 )

首先, 在你的 `Python` 环境里, 删掉 `libs` 里的所有文件, 将 `libpython3.12.lib` 拷贝进去, 并重命名为 `python312.lib`. 这样就可以保证在编译的时候调用的是 `Renpy` 的库文件而不是正常 `Python` 库的文件了

然后在你编译的目录下, 新建一个 `include` 文件夹, 在里面也扔一份 `python312.lib`, 这样可以确保该库被引用 

---
编译
---

首先是编写一个 `setup.py` 文件, 基础的内容如下, 编译的目标是 `aaa.py`
```python
from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        "aaa.py",
        language_level=3,
    )
)
```

编译指令
```powershell
> .\lib\py3-windows-x86_64\python.exe .\setup.py build_ext --inplace
```

运行顺利的话, 会生成 `aaa.xxx.pyd` 的文件

- 调用编译好的文件的话, 去 `Renpy` 对应目录里面把源文件改个名什么的, 将编译出的文件拷贝进去, 并去除掉中间的版本号信息, 留下类似 `audio.pyd` 的文件即可


[^why_linux_gendef]: 在早期使用 `VS` 命令行工具的 `dumpbin` 导出 `def` 文件时, 会不停的出现警告信息, 最后导出来的 `.def` 和 `.lib` 文件都极其的小, 基本不可用, 所以最终还是使用了 `linux` 的 `gendef` 工具生成 `.def` 文件

[^why_msys]: 为什么使用 MSYS? 一方面, 是我在 Renpy Depend List 中与编译有关的文档里面发现那时的 Pytom 使用了 MSYS: https://renpy.org/dl/lgpl/README.txt, 另一方面是 MSYS 这样调用很方便

[^lib_tool]: [如何从dll文件导出对应的lib文件?](https://www.cnblogs.com/tocy/p/export-lib-from-dll-in-windows.html "发布于 2016-05-22 11:31")

[^msys_install]: [Windows 上用 MSYS2 安装 GCC/G++（MinGW-w64）保姆级指南](https://blog.csdn.net/2301_79692223/article/details/154347519)