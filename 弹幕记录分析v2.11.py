'''
作者：二茂铁Official
更新时间：2022/10/30
使用的第三方库：matplotlib,wordcloud,jieba
'''
import json
import os
import tkinter as tk
import ctypes
import threading
from datetime import datetime
# 根据统计对象选择需要的合并逻辑
from DanmuMerge import merge_xinke as merge

fontname = ["黑体", "楷体"]

# 接收输入信息


def getinputs():
    global paths, numpath, num1, num2, num3, delta, sigfigure, sigfiguretime, sigcloud
    paths = os.listdir("input")
    numpath = len(paths)
    num1, num2, num3 = var1.get(), var2.get(), var3.get()
    delta = var4.get()
    sigfigure, sigfiguretime, sigcloud = sig1.get(), sig2.get(), sig3.get()

# 读取直播信息


def liveinformation():
    global records, vtbname, livename, starttime, endtime
    file1 = open("input//" + paths[0], 'r', encoding='utf-8')
    text = file1.read().replace('\n', '')
    file1.close()
    dics = json.loads(text, strict=False)
    vtbname = dics["info"]["name"]
    livename = dics["info"]["title"]
    starttime = dics["info"]["start_time"]
    endtime = dics["info"]["end_time"]
    records = dics["full_comments"]
    if not os.path.exists("output"):
        os.mkdir("output")
    if numpath > 1:
        livename = ""
        for i in range(1, numpath):
            file1 = open("input//" + paths[i], 'r', encoding='utf-8')
            # 弹幕记录合并
            text = file1.read().replace('\n', '')
            file1.close()
            dics = json.loads(text, strict=False)
            recordnew = dics["full_comments"]
            records.extend(recordnew)
    text2.insert('end', "已读取全部JSON文件，正在解析数据\n")

# 定义类


class Danmu():
    def __init__(self, time, text, uname, uid):
        self.time = time
        self.text = text
        self.uname = uname
        self.uid = uid


class SC():
    def __init__(self, time, text, uname, uid, price):
        self.time = time
        self.text = text
        self.uname = uname
        self.uid = uid
        self.price = price


class Gift():
    def __init__(self, time, uname, uid, price):
        self.time = time
        self.uname = uname
        self.uid = uid
        self.price = price

# 生成对象


def generateobjects():
    global objects, starttime
    objects = []
    for record in records:
        if "superchat_price" in record:
            obj = SC(int(record["time"] / 1000),
                     record["text"],
                     record["username"],
                     record["user_id"],
                     record["superchat_price"])
        elif "gift_price" in record:
            obj = Gift(int(record["time"] / 1000),
                       record["username"],
                       record["user_id"],
                       record["gift_price"])
        else:
            obj = Danmu(int(record["time"] / 1000),
                        record["text"].replace(' ', ''),
                        record["username"],
                        record["user_id"], )
        objects.append(obj)
    # 对象按时间排序
    objects.sort(key=lambda x: x.time, reverse=False)
    #starttime = objects[0].time

# 读取弹幕及其发送者


def danmustatistic():
    global totallist, danmutotal, nametotal
    danmutotal, nametotal = {}, {}
    totallist = []
    for obj in objects:
        if isinstance(obj, Danmu) or isinstance(obj, SC):
            totallist.append(obj.text)
            if len(obj.text) != 0:
                obj.text = merge(obj.text)
            if obj.text not in danmutotal.keys():
                danmutotal[obj.text] = 1
            else:
                danmutotal[obj.text] += 1
            if obj.uname not in nametotal.keys():
                nametotal[obj.uname] = 1
            else:
                nametotal[obj.uname] += 1
    # 计算弹幕总数
    numdanmu = len(totallist)
    text1.insert('end', "弹幕总数：{}条\n".format(numdanmu))
    file2.write("弹幕总数：{}条\n".format(numdanmu))
    # 将原始弹幕列表转为字符串，用于制作词云
    totallist = ','.join(totallist)

# 输出弹幕频次排行和发送者排行


def printdanmus():
    danmunums = list(danmutotal.items())
    danmunums.sort(key=lambda x: x[1], reverse=True)
    text1.insert('end', "\n弹幕排行\n")
    file2.write("\n弹幕排行\n")
    for i in range(min(num1, len(danmunums))):
        text1.insert('end', "第{}：{}，共{}条\n".format(
            i + 1, danmunums[i][0], danmunums[i][1]))
        file2.write("第{}：{}，共{}条\n".format(
            i + 1, danmunums[i][0], danmunums[i][1]))
    gatlings = list(nametotal.items())
    gatlings.sort(key=lambda x: x[1], reverse=True)
    text1.insert('end', "\n弹幕发送者排行\n")
    file2.write("\n弹幕发送者排行\n")
    for i in range(min(num2, len(gatlings))):
        text1.insert('end', "第{}：{}，弹幕{}条\n".format(
            i + 1, gatlings[i][0], gatlings[i][1]))
        file2.write("第{}：{}，弹幕{}条\n".format(
            i + 1, gatlings[i][0], gatlings[i][1]))

# 读取SC、礼物和舰长


def giftstatistic():
    global payertotal
    payertotal = {}
    for obj in objects:
        if isinstance(obj, Gift) or isinstance(obj, SC):
            if obj.uname not in payertotal.keys():
                payertotal[obj.uname] = 0
            payertotal[obj.uname] += float(obj.price)

# 输出打钱排行


def printgifts():
    tiangous = list(payertotal.items())
    tiangous.sort(key=lambda x: x[1], reverse=True)
    text1.insert('end', "\n打钱排行\n")
    file2.write("\n打钱排行\n")
    for i in range(min(num3, len(tiangous))):
        text1.insert('end', "第{}：{}，金额{:.1f}\n".format(
            i + 1, tiangous[i][0], tiangous[i][1]))
        file2.write("第{}：{}，金额{:.1f}\n".format(
            i + 1, tiangous[i][0], tiangous[i][1]))

# 输出其他统计项，需根据统计对象修改


def others():
    specnum1 = totallist.count("?") + totallist.count("？")
    text1.insert('end', "\n其他统计项\n共有中英文问号{}个\n".format(specnum1))
    file2.write("\n其他统计项\n共有中英文问号{}个\n".format(specnum1))
    otherslist = ["憨", "平", "✂️"]
    for otheritem in otherslist:
        specnum2 = totallist.count(otheritem)
        text1.insert('end', "共有{} {}个\n".format(otheritem, specnum2))
        file2.write("共有{} {}个\n".format(otheritem, specnum2))
    text2.insert('end', "文字输出已保存到txt文件中\n")

# 制作弹幕密度统计图


def generatechart(checkbox_time_offset):
    from datetime import timedelta
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import matplotlib

    # 消去日期
    for obj in objects:
        obj.time = obj.time % 86400
    # 对象重新排序
    objects.sort(key=lambda x: x.time, reverse=False)
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    arraystart = datetime.fromtimestamp(starttime / 1000)
    timearray0 = datetime.fromtimestamp(objects[0].time)
    danmucount = 0
    plt.figure(figsize=(16, 9))
    if numpath == 1:
        plt.title(arraystart.strftime("%Y-%m-%d %H:%M ") +
                  livename + "  弹幕密度统计图", fontsize=18)
    else:
        plt.title("弹幕密度统计图", fontsize=18)

    time_8hour = timedelta(hours=8)
    time_offset = datetime.fromtimestamp(0)
    if checkbox_time_offset == 1:
        time_offset = datetime.fromtimestamp(
            starttime / 1000) - time_offset + time_8hour
    else:
        time_offset = time_offset - time_offset

    # 设置坐标轴
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(20 / delta))
    plt.xlabel("时间", fontsize=18)
    plt.ylabel("弹幕密度（个/分钟）", fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    pltxs, pltys = [], []
    for obj in objects:
        if isinstance(obj, Danmu) or isinstance(obj, SC):
            timearray = datetime.fromtimestamp(obj.time)
            if timearray < timearray0 + timedelta(minutes=delta):
                danmucount += 1
            else:
                pltxs.append((timearray0-time_offset).strftime("%H:%M"))
                pltys.append(danmucount / delta)
                timearray0 += timedelta(minutes=delta)
                danmucount = 1
                # 补充无弹幕时段数据
                while timearray0 + timedelta(minutes=delta) < timearray:
                    pltxs.append((timearray0-time_offset).strftime("%H:%M"))
                    pltys.append(0)
                    timearray0 += timedelta(minutes=delta)
    pltxs.append((timearray0-time_offset).strftime("%H:%M"))
    pltys.append(danmucount / delta)
    # 用x,y坐标列表生成统计图
    plt.bar(pltxs,
            pltys,
            align='edge',
            color='lightblue')
    plt.savefig("output//" + "弹幕密度_" + vtbname + '_' +
                livename + ".png", dpi=300, bbox_inches='tight')
    text2.insert('end', "已生成弹幕密度统计图\n")

# 制作词云


def generatecloud():
    import wordcloud
    import jieba

    text2.insert('end', "词云生成中……\n")
    w = wordcloud.WordCloud(font_path="msyh.ttc",
                            collocations=False,
                            width=2000,
                            height=2000,
                            background_color="white",
                            max_words=400)
    w.generate(totallist)
    w.to_file("output//" + "弹幕云_" + vtbname + '_' + livename + ".png")
    total = jieba.lcut(totallist)
    words = ','.join(total)
    w.generate(words)
    w.to_file("output//" + "弹幕词云_" + vtbname + '_' + livename + ".png")
    text2.insert('end', "已生成词云\n")

# 程序分析步骤


def runanalysis():
    global file2
    getinputs()
    text2.insert('end', "分析开始时间：{}\n".format(datetime.now()))
    liveinformation()
    # 创建文本文件记录文字输出
    file2 = open("output//" + vtbname + '_' +
                 livename + ".txt", 'w', encoding='utf-8')
    # 清空输出窗口
    text1.delete('1.0', 'end')
    text2.insert('end', "右侧文字结果输出窗口已清空\n")
    generateobjects()
    danmustatistic()
    printdanmus()
    giftstatistic()
    printgifts()
    others()
    file2.close()
    # 文本框显示区域移到最后
    text1.see(tk.END)
    if sigfigure:
        generatechart(sigfiguretime)
    if sigcloud:
        generatecloud()
    text2.insert('end', "数据分析完成\n\n")
    text2.see(tk.END)

# 参数重置函数


def resetparameters():
    var1.set(30)
    var2.set(20)
    var3.set(10)
    var4.set(2)
    sig1.set(1)
    sig2.set(1)
    sig3.set(0)

# 设置线程，减轻程序卡顿


def thread_it(func):
    t = threading.Thread(target=func)
    t.setDaemon(True)
    t.start()


# 制作图形界面
window = tk.Tk()
# 设置分辨率
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
window.tk.call('tk', 'scaling', ScaleFactor / 75)
window.title("弹幕记录分析 by 二茂铁")
window.geometry('1400x800')
fontdefault = (fontname[0], 12)
font1 = (fontname[1], 12)
# 添加程序说明
label0 = tk.Label(window, text="本程序用于分析：\nhttps://matsuri.icu/ 网站上JSON格式的直播数据记录",
                  font=(fontname[0], 14), width=60, height=3)
label0.pack()
# 添加数值输入栏
label1 = tk.Label(window, text="弹幕排行显示数", font=fontdefault)
label1.place(x=0, y=80)
var1 = tk.IntVar()
entry1 = tk.Entry(window, textvariable=var1, font=fontdefault, width=6)
entry1.place(x=200, y=80)
label2 = tk.Label(window, text="弹幕发送排行显示数", font=fontdefault)
label2.place(x=0, y=110)
var2 = tk.IntVar()
entry2 = tk.Entry(window, textvariable=var2, font=fontdefault, width=6)
entry2.place(x=200, y=110)
label3 = tk.Label(window, text="打钱排行显示数", font=fontdefault)
label3.place(x=0, y=140)
var3 = tk.IntVar()
entry3 = tk.Entry(window, textvariable=var3, font=fontdefault, width=6)
entry3.place(x=200, y=140)
# 添加功能勾选栏
sig1 = tk.IntVar()
sig2 = tk.IntVar()
sig3 = tk.IntVar()
checkbutton1 = tk.Checkbutton(window, text="生成弹幕密度统计图",
                              font=fontdefault, variable=sig1, onvalue=1, offvalue=0)
checkbutton2 = tk.Checkbutton(window, text="弹幕密度统计图使用相对时间",
                              font=fontdefault, variable=sig2, onvalue=1, offvalue=0)
checkbutton3 = tk.Checkbutton(window, text="生成词云",
                              font=fontdefault, variable=sig3, onvalue=1, offvalue=0)
checkbutton1.place(x=0, y=230)
checkbutton2.place(x=0, y=260)
checkbutton3.place(x=0, y=290)
# 添加时间间隔输入栏
label4 = tk.Label(window, text="统计图时间间隔/分钟", font=fontdefault)
label4.place(x=0, y=170)
var4 = tk.DoubleVar()
entry4 = tk.Entry(window, textvariable=var4, font=fontdefault, width=6)
entry4.place(x=200, y=170)
# 添加运行按钮
button0 = tk.Button(window, text="开始分析",
                    bg='white', font=fontdefault, width=15, height=3,
                    command=lambda: thread_it(runanalysis))
button0.place(x=400, y=230)
# 添加参数重置按钮
button1 = tk.Button(window, text="重置参数",
                    bg='white', font=fontdefault, width=15, height=3,
                    command=resetparameters)
button1.place(x=400, y=110)
# 添加文字结果输出窗口
scroll = tk.Scrollbar()
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text1 = tk.Text(window, width=70, height=20, font=font1)
text1.pack(side=tk.RIGHT, fill=tk.Y)
scroll.config(command=text1.yview)
text1.config(yscrollcommand=scroll.set)
# 添加运行信息输出窗口
label4 = tk.Label(window, text="运行信息窗口", font=fontdefault)
label4.place(x=0, y=350)
text2 = tk.Text(window, width=60, height=15, font=font1)
text2.place(x=0, y=380)
# 显示提示信息
text2.insert('end', "注意在代码import部分选择合适的弹幕合并函数\n")
if not os.path.exists("input"):
    os.mkdir("input")
    text2.insert('end', "已创建文件夹“input”\n")
text2.insert('end', "请将需要分析的一个或多个JSON文件放入“input”文件夹中，设置完上方的参数后点击“开始分析”键\n\n")
# 填入默认参数
resetparameters()
# 运行GUI程序
window.mainloop()
