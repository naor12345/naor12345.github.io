---
title: GitHub + Hexo 博客搭建（二）
date: 2017-10-03 14:08:21
categories: "Hexo教程"
tags: 
    - "Hexo"
---

## 1. 前言
在上一篇文章{% post_link Establishment-of-GitHub-Blog-with-Hexo GitHub + Hexo 博客搭建（一） %}中已经讲解了如何对GitHub + Hexo博客的初始化建立，这片文章将介绍一些博客完善与优化的方法。

<!-- more -->


## 2. Hexo主题设置
Hexo博客框架目前已经衍生出很多主题和插件，可以任意进行修改更换。也可以直接对框架中的.css文件进行修改来更改样式。初始化网站使用的默认主题是`landscape`。如果对默认主题不满意，可以下载hexo主题进行更换。本文以更换[NexT](http://theme-next.iissnan.com/)主题为例进行说明。

Hexo中有两份主要的配置文件，文件名都是`_config.yml`，其中一份位于博客根目录下，包含博客站点本身的配置；另一份位于主题目录下(`/themes/<theme_name>/`)，由主题作者提供，用于配置主题香瓜你的选项。为了描述方便，在以下说明中，前者称为`站点配置文件`，后者称为`主题配置文件`。

### 2.1 下载新主题
确保在`hexo`分支上，命令行到博客目录，使用`git`命令：
```bash
$ git clone https://github.com/iissnan/hexo-theme-next themes/next
```
操作完成后，将看到新目录`/themes/next/`，这里面就是NexT主题文件。由于此目录是通过git获得，所以其中包含了一个`.git`文件夹，请将其删除。这个文件夹将导致博客目录向`hexo`分支提交更改失败。

### 2.2 启用主题并进行设定
打开站点配置文件，找到`theme`字段，将值更改为`next`，即可启用主题。同时，为了统一风格，定位到`language`字段，把语言更改为简体中文：
```yaml
language: zh-Hans
```

在NexT主题中，包含若干个Scheme。Scheme是NexT提供的一种特性，借助于Scheme，NexT可以提供多种不同的外观。同时，几乎所有的配置都可以在Scheme之间共用。打开主题配置文件，定位到`scheme`字段，启用`Gemini`样式：
```yaml
# Schemes
#scheme: Muse
#scheme: Mist
#scheme: Pisces
scheme: Gemini
```

### 2.3 设置菜单
菜单处默认只显示`home`和`archives`两项，除此之外，hexo包含`about`、`categories`和`tags`等其他菜单项。开启这些菜单项需要编辑主题配置文件，定位到`menu`，将需要开启的菜单项前面的注释去掉：
```yaml
menu:
  home: / || home
  about: /about/ || user
  tags: /tags/ || tags
  categories: /categories/ || th
  archives: /archives/ || archive
  #schedule: /schedule/ || calendar
  #sitemap: /sitemap.xml || sitemap
  #commonweal: /404/ || heartbeat
```

## 3. 页面设置
### 3.1 新建页面
在hexo中，只有`home`和`archives`的页面是自动生成的，上文新开启的`about`、`categories`和`tags`菜单项需要手动新建跳转过去的页面，否则打开会显示404。

创建页面可以使用以下命令：
```bash
$ hexo new page categories # 新建categories页面
$ hexo new page tags       # 新建tags页面
$ hexo new page about      # 新建about页面
$ hexo new "BlogTitle"     # 新建博客页面，文件名是BlogTitle.md
```
这样，可以生成对应的页面。

### 3.2 文章标签与分类
`tags`和`categories`页面建成之后，就可以对博客内文章的标签和分类进行显示了。在每篇博客文章的标题处，有一些文章设置字段，如本篇文章md文件的标题处：
```Markdown
---
title: 【Hexo02】GitHub + Hexo 博客完善与优化
date: 2017-10-03 14:08:21
categories: "Hexo教程"
tags: 
    - "Hexo"
---
```
通过对`tags`和`categories`字段进行设置，即可把文章分类进行组织，显示在菜单的`tags`和`categories`处。
如果文章包含多个标签，可以使用如下语法：
```
tags:
    - "tags1"
    - "tags2"
    - "tags3"
```

### 3.3 页面折断
默认状态下，博客首页将显示博客内的所有文章，而且所有文章的正文都是展开的，很没有条理性。可以通过设置文章折断，让首页内只显示文章标题和一部分文章内容。方法是在md文件内需要折断的位置添加：
```html
<!-- more -->
```
这样，在首页处文章只显示到折断处，然后是`阅读全文`按钮，首页将比原来更有层次和条理性。

### 3.4 博客内页面跳转
为了增加各个文章之间的联系，在一个博客内各个文章之间进行跳转是一个常见的需求。Markdown语法插入的链接是绝对的，不好维护，使用Hexo本身语法可以解决此问题。在md文件需要插入链接的位置写入：
```Markdown
{% post_link 文章文件名（不含后缀） 文章标题（可省略） %}
```
即可。这段代码不符合Markdown语法，所以Markdown编辑器无法解析，但是通过`hexo generate`生成后可以很好地实现链接跳转的功能。

## 4. 结语
至此，本文介绍了一些比较基本的博客完善方法，可以说是一些小trick，当作经验记录下来。本系列文章将持续记录博客搭建的过程。

