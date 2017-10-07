---
title: 光线追踪方法实现全局光照
date: 2017-10-07 11:29:36
categories: "项目经历"
tags: 
    - "RayTracing"
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

## 1. 前言
本文介绍的是一个用光线追踪算法实现全局光照的代码。源代码已托管到[GitHub](https://github.com/naor12345/RayTracing)中。本程序参考了[Kevin Beason](http://kevinbeason.com/)的[smallpt项目](http://www.kevinbeason.com/smallpt/)，在此基础上增加了其他几何体（smallpt只有球体）。程序运行效果如图所示。
<img src="https://github.com/naor12345/RayTracing/blob/master/image.JPG?raw=true" width = "400" height = "300" alt="运行效果" align=center />

<!-- more -->

## 2. 算法介绍
### 2.1 算法概述
常见的全局光照算法包括光线追踪和辐射度算法。本工程中使用的是光线追踪算法。光线追踪算法于1979年由Turner whitted提出。光线追踪的算法是模拟人眼看到物体的过程，物体引起人眼的视觉需要满足以下条件：
* 场景中有光源或物体本身是光源
* 光线照射到物体上反射到人眼或光源直接发射光线到人眼
基于这种思想，可以从光源开始追踪光源发射出的每一束光，计算它们与物体的交点，同时计算反射光和折射光。如果最终有光线射到人眼，那么将形成一条从光源到人眼的完整光路。回溯此光线，计算第一交点的颜色，即是人眼视觉所察觉的颜色。
然而，以上方法计算两很大，尤其如果光源是点光源，发射光将有无数条。一种方法是将光路逆转，从眼睛开始追踪，如果最终这条光线与光源有交点，则光路打通。追踪光线数目与最终渲染图的像素数目相同。
![Ray Tracing](https://github.com/naor12345/RayTracing/blob/master/Tracing.png?raw=true)

### 2.2 材质定义
本代码中用一下属性定义材质：
* 发射光颜色：物体本身发光的颜色，若本身不是光源，则为黑色
* 反射光颜色：白光照射在物体上时物体反射的颜色
* 反射属性：控制物体表面发射状态，有三种：
    - 不透光，漫反射
    - 不透光，镜面反射
    - 透光， 镜面反射

### 2.3 递归算法 
由于每当光线与物体产生交点时，要继续追踪产生的折射光和反射光，所以用递归算法很合适。函数返回值为当前光线在入射点处贡献（产生）的颜色。 伪代码如下：
```c++
Color trace(ray)
{
    if(ray与场景物体有交点)
    {
        计算入射点
        计算反射光
        计算折射光
        if(物体不同材质)
        {
            返回 物体本身发光 + 物体本身颜色与trace(反射光)的混合
        }
        else
        {
            返回 物体本身发光 + 物体本身颜色与(trace(反射光) + trace(折射光))的混合
        }
    }
    else
    {
        返回黑色光
    }
}
```
## 3. 实现过程
### 3.1 光和色
代码中的基本量（类）有`Vec`和`Ray`。
#### 3.1.1 `Vec`类
`Vec`即Vector（向量），包含三个成员变量：
```c++
class Vec
{
    double x, y, z;
};
```
在本代码中，`Vec`是一个广泛使用的类，有以下用法：
* 表示位置
* 表示光线发射朝向
* 表示法向量
* 表示颜色

当`Vec`表示颜色时，其`x`、`y`、`z`分别表示RGB，且规定取值范围在[0, 1]区间内。全0表示黑色，全1表示白色。当光线与物体产生交点时，交点的颜色为光线颜色与物体颜色的直接混合，即各个分量对应相乘，定义为：
```c++
Vec Vec::mult(const Vec &b) const
{
    return Vec(x*b.x, y*b.y, z*b.z);
};
```

#### 3.1.2 `Ray`类
`Ray`类用于表示光线。光线在数学上可以抽象为射线，包含顶点和方向，定义为：
```c++
class Ray
{
    Vec o, d;
};
```
其中`o`表示光线起点，`d`表示光照方向的单位向量。

### 3.2 几何体
#### 3.2.1 几何体`Geometry`基类
为了发挥C++的多态机制，首先建立`Geometry`基类，用于储存物体的基本属性：
```c++
class Geometry
{
public:
    //本身发射光颜色
    Vec emit; 
    //本身反射白光时的颜色
    Vec color; 
    // 判断点P是否在物体上
    virtural bool isOn(const Vec &P) = 0; 
    // 光线ray与物体的求交运算，结果以IntersecResult类的实例保存
    virtual IntersecResult isintersected(Ray &ray) = 0;  
    // 求入射光ray在入射点hitpoint处的反射光
    virtual Ray getReflection(Ray ray, Vec hitpoint) const = 0;  
    // 求入射光ray在入射点hitpoint处的折射光
    virtual Ray getRefraction(Ray ray, Vec hitpoint, double &Re) const = 0;  
};
```
`Geometry`中的所有虚函数将在各自几何体中实现。

#### 3.2.2 球体`Sphere`
球体用圆心和半径定义：
```c++
class Sphere: public Geometry
{
    Vec center;
    double radius;
};
```

#### 3.2.3 平面`Plane`
平面由平面上一点和法向量确定。
```c++
class Plane: public Geometry
{
    Vec p;
    Vec normV;
};
```

#### 3.2.3 无限长圆柱`CylinderInf`
为了更好地表示圆柱体，首先定义一个无限长圆柱，由两个点（确定圆柱中轴线）和半径确定：
```c++
class CylinderInf: public Geometry
{
    Vec p1, p2;    
    double radius;
};
```

#### 3.2.4 圆柱体`Cylinder`
圆柱体由两个点（确定圆柱中轴线）、半径和高确定：
```c++
class Cylinder: public Geometry
{
    Vec p1, p2;    
    double radius;
    double h;
};
```

#### 3.2.5 长方体的表面`RecPlane`
为了更好地表示长方体，首先定义一个“长方体的表面”类`RecPlane`，这个类用于表示长方体的某一侧面。成员变量为该侧面的四个顶点的空间坐标：
```c++
class RecPlane: public Plane
{
    Vec p1, p2, p3, p4;
};
```

#### 3.2.6 长方体`Hexahedron`
由于有`RecPlane`类的铺垫，长方体类的成员变量为6个`RecPlane`的实例：
```c++
class Hexahedron: public Geometry
{
    RecPlane r1, r2, r3, r4, r5, r6;
public:
    Hexahedron(Vec p1, Vec p2, Vec n, Vec p);
};
```
然而，为了在空间中确定一个长方体，不能通过输入6个面来确定，这样各个变量之间的耦合性太高。`Hexahedron`的构造函数的输入参数为三个点和一个向量。其中，$p1$和$p2$是正方体底面矩形的对角两个顶点，设$p3$、$p4$是另外对角的两个顶点，矩形中心为$o$。$\vec{n}$是从$o$指向$p3$或$p4$的单位向量。这样，底面就可以被唯一确定。$p$则用于确定长方体的另一面，$p$到这个底面的距离即是长方体的高。

### 3.3 辅助数据结构
#### 3.3.1 `IntersectResult`结构体
当光线与场景中当某物体产生交点时，其“入射点”、“法向量”、光线发射点与入射点的距离等一些变量将通过`InersectResult`类来保存。
```c++
struct IntersecResult
{
    // 光发射点与入射点的距离
	double distance;
    // 光线是否与物体有交点
    bool isHit;
    // 入射点位置
    Vec position;
    // 入射点法向量
    Vec normal;
    // 物体属性（用于调用相应的函数求反射光和折射光）
	Geometry *_object;
};
```

#### 3.3.2 场景类`Union`
场景类用于储存场景中的所有物体，当给出一个光线时，场景类的成员函数可以求出该光线与场景中物体的交点。类中一些比较重要的成员函数和变量如下：
```c++
class Union:public Geometry
{
public:
    // 用于判定光线ray是否与场景中的物体有交点
	virtual IntersecResult isIntersected(Ray &ray);
private:
    // 保存场景中的所有物体
	std::vector<Geometry*> gobjects;
};
```

### 3.4 各物体入射光与反射光的计算
此部分入射光与反射光的计算纯属空间向量数学问题，这里从简。计算光路时一个比较简单的方法是把光线用参数方程的方法表示。

$$\vec{p} = \vec{o}+t\vec{d}$$

其中$\vec{o}$表示光线原点，$\vec{d}$表示光照方向的单位向量，$t$表示光照距离，$p$表示$t$距离之后的光点。

#### 3.4.1 平面与球
平面与球的光线物理计算相对简单。最重要的是法向量方向不要搞错。

#### 3.4.2 圆柱体
圆柱体可以抽象成一个无限长圆柱面和上下两个地面。在柱面上的反射折射与球上的一致，在上下两个平面上的反射折射与平面的一致。需要注意的是计算好距离，和入射点的范围。

#### 3.4.3 长方体
长方体在计算反射折射时可以直接用6个平面来计算。

## 4. 总结
本程序可以作为光线追踪的入门程序。基本原理如本文所阐述。此外涉及到的一些其他细节比如漫反射的多次随机反射、光线反射一定次数后将有一定概率消散掉、每个像素点进行多次采样以达到更好的渲染效果等等，可以参考源代码。