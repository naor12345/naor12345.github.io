---
title: 配置Hexo多语言博客
date: 2022-05-17 09:29:15
categories: "Hexo"

tags: 
    - "Hexo"
---

**Minos主题是一款支持多语言的Hexo主题。**

## 安装主题Minos
Github：https://github.com/ppoffice/hexo-theme-minos/

## 配置
下载主题后，到`themes\minos\languages`可以看到所有支持的语言。假设博客需要两种语言（中英文），而且主语言是英语。

将`_config.yml.example`重命名为`_config.yml`。该文件是`Mintos`的默认配置文件，也是主语言的配置文件。然后复制一份`_config.yml`，改名为`_config.zh-cn.yml`，这是中文的配置文件。

打开`config.zh-cn.yml`，修改`menu`配置，在路径处添加`zh-cn`的前缀：
```yaml
menu:
  Archives: /zh-cn/archives
  Lifestyle: /zh-cn/categories/LifeStyle
  Music: /zh-cn/categories/Music
  Technology: /zh-cn/categories/Technology
  About: /zh-cn/about
```

修改根目录的`_config.yml`（hexo的配置，非主题配置），修改语言：
```yaml
language:
 - en # 第一个是主语言
 - zh-cn
```

修改`permalink`熟悉，更改主题为`Mintos`:
```yaml
permalink: :title/
theme: minos
```

## 修改文件结构
默认的目录里，生成的文档都是用于主语言的：
 - (文章) source/_post/`<English post>.md`
 - (其他文件夹) source/about/index.md
 - source/archives/index.md

按如下方式创建`zh-cn`，用于中文：
 - source/_post/zh-cn/`<Chinese post>.md`
 - source/zh-cn/about/index.md
 - source/zh-cn/archives/index.md

修改完毕后，文件目录如下所示：
 - source/_post/`<English post>.md`
 - source/about/index.md
 - source/archives/index.md
 - source/_post/zh-cn/`<Chinese post>.md`
 - source/zh-cn/about/index.md
 - source/zh-cn/archives/index.md

## 修改主题布局
`Minos`切换语言的小部件默认在页脚，放到页眉会更好一些。

打开文件`themes/minos/layout/common/footer.ejs`, 搜索`<%- partial('common/languages') %>`，将搜到这一行代码移动到`themes/minos/layout/common/navbar.ejs`的如下位置:
```html
            <% } %>
            <%- partial('common/languages') %>
        </div>
    </div>
</nav>
```

打开文件`themes/minos/layout/common/languages.ejs`, 搜索`<div class="dropdown-menu has-text-left" role="menu"`, 将该句修改为`<div class="dropdown-menu has-text-left" role="menu" style="top:100%">`

## 完结
Enjoy your coding.

## 参考
 - https://github.com/ppoffice/hexo-theme-minos
 - http://ppoffice.github.io/hexo-theme-minos/Configuring-Minos/
 - http://t.zoukankan.com/ballwql-p-hexo.html
 - https://blog.learn-or-die.com/zh-tw/buildABilingualBlog/