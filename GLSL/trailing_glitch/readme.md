# TrailingGlitch

<img src="readme.png" height="400" />

---

带拖尾效果的故障效果 transform

此 transform 初始化时可以传入三个参数

| 参数名 | 数据类型 | 描述 | 默认值 |
| -------------------- | ---- | ---- | ---- |
| weight | float | 拖尾故障的强度 | 0.5 |
| color_weight | float | 色散的强度 | 0.5 |
| angle | float | 采样变换的角度 | 0 |

初始化后可以通过对以下参数进行插值达到动画效果

| 参数名 | 数据类型 | 描述 |
| -------------------- | ---- | ---- |
| u_weight | float | 拖尾故障的强度 |
| u_color_weight | float | 色散的强度 |
| u_angle | Iterable[float, float] | 采样的变换 |

其中, 采样的变换传入的两个参数 [a, b] 将组为矩阵进行变换

$$
(a, b) →
\begin{bmatrix}
	b & -a \\
	a & b
	\end{bmatrix}
$$
			
所以, 要对采样进行旋转变换的话, 传入转换角的 sin, cos 值就可以完成变换
在初始化阶段传入的 angle 参数会自动经 sin, cos 运算并设置到 u_angle 里 

相对的, 由于 transform 的插值函数无法模拟出这样的变换, 这边建议用 function 来对 u_angle 这个值进行修改