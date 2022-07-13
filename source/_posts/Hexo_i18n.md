---
title: Hexo multi-lingual blog i18n
date: 2022-07-12 09:29:15
categories: "Hexo"

tags: 
    - "Hexo"
---

**Some Hexo themes have multi-language support, and `Mintos` is one of them.**

## Download
Github: https://github.com/ppoffice/hexo-theme-minos

## Configuration
After downloading, explore `themes\minos\languages` to check out all supported languages. Assuming that there are two languages (Chinese and English) to apply, and the main language is English.

Rename `_config.yml.example` to `_config.yml`. This file is the default configuration of `Mintos`, which is also the configuration of the main language.
Then create a new config `_config.zh-cn.yml` copying from `_config.yml`, which is the configuration when applying Chinese.

Change `menu` config on `config.zh-cn.yml`, and add prefix `zh-cn` to each folder.
```yaml
menu:
  Archives: /zh-cn/archives
  Lifestyle: /zh-cn/categories/LifeStyle
  Music: /zh-cn/categories/Music
  Technology: /zh-cn/categories/Technology
  About: /zh-cn/about
```

Come to the `_config.yml` at the root of the blog. Change `language`:
```yaml
language:
 - en # First one should be the main language.
 - zh-cn
```

Modify `permalink` and change theme to `Mintos`:
```yaml
permalink: :title/
theme: minos
```

## Change file structure
The default file structure below is used for the main language:
 - (Main posts) source/_post/`<English post>.md`
 - (Other fo lders) source/about/index.md
 - source/archives/index.md

Create `zh-cn` folder for second languages:
 - source/_post/zh-cn/`<Chinese post>.md`
 - source/zh-cn/about/index.md
 - source/zh-cn/archives/index.md

The final source folder structure is something like that:
 - source/_post/`<English post>.md`
 - source/about/index.md
 - source/archives/index.md
 - source/_post/zh-cn/`<Chinese post>.md`
 - source/zh-cn/about/index.md
 - source/zh-cn/archives/index.md

## Modify layout
The widget changing language is at the page footer by default. It would be better to put it on the page header.

Open file `themes/minos/layout/common/footer.ejs`, search for `<%- partial('common/languages') %>` and move this code to the end of `themes/minos/layout/common/navbar.ejs`:
```html
            <% } %>
            <%- partial('common/languages') %>
        </div>
    </div>
</nav>
```

Open file `themes/minos/layout/common/languages.ejs`, search for `<div class="dropdown-menu has-text-left" role="menu"`, and change it to `<div class="dropdown-menu has-text-left" role="menu" style="top:100%">`

## That's all
Enjoy your coding.

## Reference
 - https://github.com/ppoffice/hexo-theme-minos
 - http://ppoffice.github.io/hexo-theme-minos/Configuring-Minos/
 - https://blog.learn-or-die.com/buildABilingualBlog/