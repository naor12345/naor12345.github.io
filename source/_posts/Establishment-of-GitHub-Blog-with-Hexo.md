---
title: 【Hexo01】GitHub + Hexo 博客搭建
date: 2017-10-02 23:14:51
categories: "Hexo教程"
tags: 
    - "Hexo"
---

## 1. 前言
本文介绍如何用Hexo框架在GitHub上搭建个人独立博客，以及后期的维护和优化工作，包括来自[GitHub Pages + Hexo搭建博客](http://crazymilk.github.io/2015/12/28/GitHub-Pages-Hexo%E6%90%AD%E5%BB%BA%E5%8D%9A%E5%AE%A2/)的部分内容和自己踩到的一些坑。GitHub提供了一个用于建立个人页面的托管空间，而Hexo是一个简介快速的博客框架。博客建立的主要思路是，用Markdown语言进行写作，得到.md文件；然后用Hexo框架把.md文件编译成浏览器可以识别的.html、.js、.css等文件；最后通过Hexo发布到指定的GitHub页面托管库中。本文以macOS为操作系统，一些命令可能与Windows有所不同。
<!-- more -->
预备知识：
* [GitHub](https://github.com)
* [Hexo](https://hexo.io/zh-cn/index.html)
* [Markdown语言](http://wowubuntu.com/markdown/)

## 2. GitHub配置
### 2.1 建立GitHub Pages仓库
注册并登陆GitHub账户，建立新仓库，命名为 username.github.io（username是GitHub账户名）。勾选"Initialize this repository with a README"选项，gitignore和license可以先不用管。

仓库建立后，转到仓库的Settings页面，在GitHub Pages处看到
> ☑️ Your site is published at [https://naor12345.github.io](https://naor12345.github.io)

字样即表示建立成功。

### 2.2 安装与配置Git
下载并安装Git组件和图形窗口，笔者这里安装的是[GitHub Desktop](https://desktop.github.com/)。安装、设置、SSH Key配置过程省略。

## 3. Hexo安装与配置
### 3.1 安装Hexo
安装之前请确保机器中已安装了下列程序：
* Node.js
* Git

可以直接在命令行中通过`--version`命令查看版本，确定是否已经安装。
```bash
$ node --version
$ git --version
```

在已经确定安装好上述程序后，适用npm安装Hexo。
```bash
$ npm install -g hexo-cli
```

### 3.2 Hexo的首次建站
到目前位置，GitHub页面仓库和Hexo均已安装完毕，可以进行博客的首次建站。

#### 3.2.1 拉取GitHub仓库
在`GitHub Desktop`中把刚才建立的页面仓库克隆下来，文件夹默认是`naor12345.github.io`，将其重命名为`GitHubBlog`。克隆完成后，文件夹中应该包含一个`README`文件和git配置文件等。

#### 3.2.2 配置GitHub仓库分支
为了以后博客更好维护，需要在此时配置仓库的分支。一般地，Hexo部署到GitHub上的文件，是.md（博客文件）转化之后的.html（静态网页）。因此，无法在不同电脑上修改博客。为了解决此问题，可以利用GitHub当分支。其实，Hexo生成当网站中包含.gitignore等配置文件，因此本意也是应该将博客文件存放到GitHub上进行管理。可以通过在GitHub仓库中建立一个新分支`hexo`，用于存放博客文件，而`master`分支用于存放静态网页，这样不仅可以在其他电脑上修改博客，也可以对写作进行版本控制。

在还没有建立博客之前，新建分支`hexo`，并且将其设置为默认分支。

#### 3.2.3 Hexo建站初始化
下面开始进行hexo的建站初始化，这个建站是用来建立博客文件写作框架的，所以请确保当前在`hexo`分支上。

打开命令行窗口，进入到`GitHubBlog`目录中。接下来的建站将通过命令行完成。但是Hexo的首次建站要求目录中不能有其他文件，所以点按`Command+shift+.`组合键，显示所有隐藏文件（再次点按可隐藏），把刚刚git clone产生的所有文件移动到其他位置备用（之后还要移动回来）。然而还是不行，如果在命令行中键入`ls -a`命令，将发现还有一个`.DS_Store`文件。这个文件是macOS特有的，用于记录当前目录的属性（文件摆放位置等等），不是很重要，用`rm -f .DS_Store`命令进行删除。

这样，`GitHubBlog`目录已经是空目录了。输入以下命令：
```bash
hexo init
```
该命令会在目录中生成网站需要的所有文件。接下来是安装依赖包：
```bash
$ npm install
```
这样，本地的hexo博客已经初始化完毕，初始化的网站中包含一篇标题为《Hello World》的文章，内容是对Hexo的简单介绍。输入以下命令进行编译，将博客文件转化为静态网页：
```bash
$ hexo generate
```
这时可以看到目录中生成了一些其他的文件夹，这些文件夹包含了转化后的.html、.js、.css等文件。这些文件就是之后要发布到master分支上的静态网页文件。发布前可以先在本地进行浏览，输入命令：
```bash
$ hexo server
```
启动服务器。打开浏览器输入`localhost:4000`进行查看，如果看到了《Hello World》的文章，说明配置成功。下一步，将这个博客进行发布。

### 3.3 设置发布
发布之前，先要对发布进行设置。打开目录中的站点配置文件`_config.yml`。定位到最后部分，对`deploy`处进行修改。
默认的`_config.yml`：
```yaml
# Deployment
## Docs: https://hexo.io/docs/deployment.html
deploy:
  type: git
```
修改后的`_config.yml`：
```yaml
# Deployment
## Docs: https://hexo.io/docs/deployment.html
deploy:
  type: git
  repo: 仓库的SSH地址，在GitHub页面中复制
  branch: master
```
为了能够使Hexo部署到GitHub上，需要安装一个插件：
```bash
$ npm install hexo-deployer-git --save
```
在发布之前，先将目前的改动提交并推送到`hexo`分支上，最后执行以下指令即可完成部署：
```bash
$ hexo generate
$ hexo deploy
```
在浏览器中输入[naor12345.github.io](naor12345.github.io)进行浏览。

### 3.4 日常管理
每当要对博客进行修改或新建文章时，首先确保本地的博客目录在`hexo`分支上，修改结束后提交并推送。然后再执行以下命令
```bash
$ hexo clean    # 清除上次生成时旧的网页文件
$ hexo g -d     # 生成网页并发布
```

## 4 结语
至此，GitHub + Hexo博客的搭建工作就完成了。下一篇文章将介绍一些博客的完善与优化工作。
