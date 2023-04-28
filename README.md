# Bilibili_show_ticket_order

Bilibili会员购抢票助手，通过B站接口抢购目标漫展/演出

## 使用

### 傻瓜式

请先安装[Python](https://www.python.org/downloads/)到目录**D:\Program Files\Python**，除非你打算自己设置cookie，然后安装[Chrome浏览器](https://www.google.com/chrome/)，然后在[Release页面](https://github.com/Hobr/Bilibili_show_ticket_order/releases)下载预载了运行环境的压缩包

解压后进入目录，点击**run.cmd**运行，根据提示输入信息即可

如果要购买多张票，必须提前设置好相应数量的购票人信息，不能多不能少

### 命令行

```bash
git clone https://github.com/Hobr/Bilibili_show_ticket_order.git
cd Bilibili_show_ticket_order
mv config.json.example config.json
pip install -s requests selenium
python script.py
```
