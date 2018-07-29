---
title: GitHub + Hexo 博客搭建（三）
date: 2017-10-03 14:08:21
categories: "Hexo教程"
tags: 
    - "Hexo"
---

<script type="text/javascript" src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

## 1. 前言
本文讲述一些文章中其他要素的搭建，比如插入图片、插入数学公式、统计访问量、加入评论系统等等。本文的参考资料有：
* [Markdown中插入数学公式的方法](http://blog.csdn.net/xiahouzuoxin/article/details/26478179)

<!-- more -->

## 2. 插入图片
在GitHub博客插入图片的方法有很多，大家根据自己的情况进行选择。笔者这里一般记录一些项目，把与其有关的图片放到对应的GitHub仓库中，然后在GitHub网页版上访问对应的图片，即可获得图片链接。

## 3. 插入数学公式
插入数学公式的痛点在于Markdown语言不支持Latex的公式语法。网上可以找到的一般有三种方法。
### 3.1 使用Google Chart的服务器
在要插入公式的位置插入代码：
```html
<img src="http://chart.googleapis.com/chart?cht=tx&chl= 在此插入Latex公式" style="border:none;">
```
示例：
```html
<img src="http://chart.googleapis.com/chart?cht=tx&chl=\Large x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}" style="border:none;">
```
但笔者尝试后发现Google服务器时常处于“断线”状态。

### 3.2 使用forkosh服务器
使用forkosh插入公式的方法是
```html
<img src="http://www.forkosh.com/mathtex.cgi? 在此处插入Latex公式">
```
示例：

<img src="http://www.forkosh.com/mathtex.cgi? \Large x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}">


### 3.3 使用MathJax引擎
在Markdown中使用MathJax引擎需要在正文之前插入以下代码：
```html
<script type="text/javascript" src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>
```

然后，再使用Tex写公式。`$$公式$$`表示行间公式，`\\(公式\\)`表示行内公式。示例如下：

行间公式：

$$x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$$

行内公式：\\(x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}\\)

npm uninstall hexo-renderer-marked --save
npm install hexo-renderer-kramed --save
首页显示的位置只能放文字，不要放代码