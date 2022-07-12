---
title: 命令行输出重定向
date: 2022-05-16 10:39:17
description: 介绍命令行输出重定向
categories: "Shell"
copyright: false
tags: 
    - "Shell"
---

**三个流，stdin，stdout，stderr，在命令行里对应编号0、1、2。**
```bash
cmd > file.txt    # stdout重定向，新建文件
cmd >> file.txt   # stdout重定向，附加到已有文件结尾
cmd &> file.txt   # stdout和stderr都重定向，此用法不是标准实现，只是某些shell的特殊实现
cmd &>> file.txt  # 没有这种写法
```
<!-- more -->
**例：**`cmd >>file.txt 2>&1 `
Bash executes the redirects from left to right as follows:
- `>>file.txt`: Open file.txt in append mode and redirect stdout there.
- `2>&1`: Redirect stderr to "where stdout is currently going". In this case, that is a file opened in append mode. In other words, the &1 reuses the file descriptor which stdout currently uses. 此处的&符号用于表示文件描述符，&1表示输出到stdout输出的位置上。

**也可以用编号直接拆分输出**
```bash
cmd >log.out 2>log_error.out   # 新建
cmd >>log.out 2>>log_error.out # 追加
You_command 1>output.log  2>&1 # 更明确的区分
```
`Usage: <file_descriptor> > <filename | &file_descriptor>`
`your_command 2>&1 | tee -a file.txt`
It will store all logs in file.txt as well as dump them on terminal.此处|符号表示管道符号（pipe symbol），表示前者命令的stdout作为后者的输入

**互换重定向**
`command 3>&1 1>&2 2>&3`
This creates a new file descriptor (3) and assigns it to the same place as 1 (standard output), then assigns fd 1 (standard output) to the same place as fd 2 (standard error) and finally assigns fd 2 (standard error) to the same place as fd 3 (standard output).
Standard error is now available as standard output and the old standard output is preserved in standard error. This may be overkill, but it hopefully gives more details on Bash file descriptors (there are nine available to each process).
A final tweak would be 3>&- to close the spare descriptor that you created from stdout. 这个方法的前提是3号描述符不能已经被使用。

**python中，可以这样：**
```python
a = Popen(cmd, stdout=pipe, stderr=pipe)
stdout, stderr = a.communicate()
for line in stdout:
    print line
    write_file(line)
```