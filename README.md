# VTB-statistics
对 https://matsuri.icu/ 网站上的直播记录进行分析，得到弹幕排行、弹幕发送者排行和打钱排行，并制作弹幕云和弹幕密度统计图。

仓库包含了两个类型的图形用户界面：
1. 运行`弹幕记录分析v2.11.py`,可以打开由tkinter库绘制的窗口程序。
2. 运行`app.py`,可以根据提示用浏览器访问形如`http://127.0.0.1:8060`的地址，这是由Gradio库绘制的界面。特别的，在huggingface已经部署了一个实例，你可以无需部署，直接访问 https://tumuyan-danmuanalyse.hf.space 来分析弹幕。


感谢matsuri.icu的开发者使DD们可以不需要自己编写和运行爬虫。

贴吧@天启Hammer对空

B站@二茂铁Official
