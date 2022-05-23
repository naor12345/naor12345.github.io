---
title: PyQt5发送系统通知
date: 2022-05-23 11:12:57
categories: "PyQt5"
tags: 
    - "PyQt5"
---

```python
# 只适用于win10
from win10toast import ToastNotifier

toaster = ToastNotifier()
toaster.show_toast(
    "Demo notification",
    "Hello world",
    duration=5,
    threaded=True
)
```

```python
from plyer import notification
# 有bug，每次通知会在系统托盘处生成一个图标
notification.notify(
    title="test",
    message="sssss",
    timeout=5,
    ticker="sfdfgs",
    app_icon="./icon.ico"
)
```

```python
from notifypy import Notify
# 目前采用这个
notification = Notify()
notification.title = "Cool Title"
notification.message = "Even cooler message."
notification.icon = "path/to/icon.png"
notification.send()
```

https://schedule.readthedocs.io/en/stable/
