---
title: 一个可以复现已产生结果的伪随机数生成器
date: 2018-07-26 15:32:16
categories: "项目经历"
tags:
    - "随机数"
    - "算法"
mathjax: true
---
由于业务需求，需要实现一个带有记忆功能的随机数生成器，即在生成模式，可以产生大量随机数；在复现模式，可以在已经产生的随机数中随机输出一个。其基本原理是在基于线性同余法的伪随机数生成器上，实现了一个复现的功能。
<!-- more -->

# 伪随机数生成器
一个很经典的伪随机数生成算法是[线性同余法](https://zh.wikipedia.org/wiki/%E7%B7%9A%E6%80%A7%E5%90%8C%E9%A4%98%E6%96%B9%E6%B3%95)。其本质是一个数列的递推方程。
$$
N_{i+1} \equiv a \cdot N_i + b (\mod m)  \tag{1}
\\ N_0 = {\rm seed}
$$
用合理的数给$a$和$b$赋值，并给定其初始值$N_0$，就可以通过递推产生随机数。其中随机数初始值就是随机数种子。C++的`rand()`函数就是这样实现的，此函数可以抽象成
```c++
inline void fast_srand( int seed )
{
    g_seed = seed;
}

inline int fastrand()
{
    g_seed = (214013*g_seed+2531011);
    return (g_seed>>16)&0x7FFF;
}
```
其中$a=214013$，$b=2531011$。

# 实现复现功能
由于业务需求，需要复现已经出现的随机数。比如，随机产生了100个随机数，现在要求随机复现其中50个。这个功能通过求通项公式实现。即，通过递推公式$(1)$产生随机数，并通过递推公式求形如
$$
N_n \equiv f(n) (\mod m) \tag{2}
$$
的通项公式。只要在0~100中间随机取50个数$n_i$，那么$f(n_i)$就可以随机地复现之前已经产生的随机数。

## 由递推公式求通项公式
首先需要由递推公式推导出通项公式。在此之前，要介绍一下模运算的一些主要性质。
- 恒等性
$$(a\mod n)\mod n = a\mod n$$
- 分配律：
$$
(a + b)\mod n = [(a\mod n) + (b\mod n)]\mod n \\
ab\mod n = [(a\mod n)(b\mod n)]\mod n
$$
- 除法定义：仅当式子右侧有定义时，即 b、n 互质时有：
$$
(a / b)\mod n = [(a\mod n)(b^{-1}\mod n)]\mod n
$$
其他情况未定义。

先忽略取模运算，由
$$
N_{i+1} = a \cdot N_i + b \qquad (a \not= 1)
$$
可以得到：
$$
N_{i} = a^i \cdot N_0 + \frac{a^i-1}{a-1}b \overset{def}{=}A + B
$$
下面分别对A$A$和$B$的模运算进行求解。

### 模幂
[模幂](https://en.wikipedia.org/wiki/Modular_exponentiation)是用于求解形如$(a^n)\mod m$的算法。


### 模逆元
