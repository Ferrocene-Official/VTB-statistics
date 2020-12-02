'''
作者：二茂铁Official
更新时间：2020/12/2
使用的第三方库：matplotlib,wordcloud,jieba
'''

# 参数输入
def getinputs():
    global paths, numpath, num1, num2, num3
    print("注：各次直播的JSON文件请从 https://matsuri.icu/ 获取")
    print("（注意选择合适的弹幕合并函数）")
    input("请在本程序同目录下创建“input”文件夹，将需要分析的一个或多个JSON文件放入其中，完成后按回车键继续")
    paths = os.listdir("input")
    numpath = len(paths)
    num1 = int(input("\n弹幕排行显示条数（默认30）：") or 30)
    num2 = int(input("弹幕发送者排行显示条数（默认20）：") or 20)
    num3 = int(input("打钱排行显示条数（默认10）：") or 10)

# 读取直播信息
def liveinformation():
    global records, vtbname, livename, file2
    file1 = open("input//" + paths[0], 'r', encoding='utf-8')
    text = file1.read().replace('\n', '')
    file1.close()
    dics = json.loads(text, strict=False)
    vtbname = dics["info"]["name"]
    livename = dics["info"]["title"]
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
    # 创建记录输出的文本文档
    file2 = open("output//" + vtbname + '_' + livename + ".txt", 'w', encoding='utf-8')

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
    starttime = objects[0].time

# 读取弹幕及其发送者
def danmustatistic():
    global totallist, danmutotal, nametotal
    danmutotal, nametotal = {}, {}
    totallist = []
    for obj in objects:
        if isinstance(obj, Danmu) or isinstance(obj, SC):
            totallist.append(obj.text)
            if len(obj.text) != 0:
                # 根据统计对象选择需要的合并逻辑
                obj.text = DM.merge_xinke(obj.text)
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
    print("\n弹幕总数：{}条".format(numdanmu))
    file2.write("弹幕总数：{}条\n".format(numdanmu))
    totallist = ','.join(totallist)

# 输出弹幕频次排行和发送者排行
def printdanmus():
    danmunums = list(danmutotal.items())
    danmunums.sort(key=lambda x: x[1], reverse=True)
    print("\n弹幕排行")
    file2.write("\n弹幕排行\n")
    for i in range(num1):
        print("第{}：{}，共{}条".format(i + 1, danmunums[i][0], danmunums[i][1]))
        file2.write("第{}：{}，共{}条\n".format(i + 1, danmunums[i][0], danmunums[i][1]))
    gatlings = list(nametotal.items())
    gatlings.sort(key=lambda x: x[1], reverse=True)
    print("\n弹幕发送者排行")
    file2.write("\n弹幕发送者排行\n")
    for i in range(num2):
        print("第{}：{}，弹幕{}条".format(i + 1, gatlings[i][0], gatlings[i][1]))
        file2.write("第{}：{}，弹幕{}条\n".format(i + 1, gatlings[i][0], gatlings[i][1]))

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
    print("\n打钱排行")
    file2.write("\n打钱排行\n")
    for i in range(num3):
        print("第{}：{}，金额{:.1f}".format(i + 1, tiangous[i][0], tiangous[i][1]))
        file2.write("第{}：{}，金额{:.1f}\n".format(i + 1, tiangous[i][0], tiangous[i][1]))

# 输出其他统计项，需根据统计对象修改
def others():
    specnum1 = totallist.count("?") + totallist.count("？")
    print("\n其他统计项\n共有中英文问号{}个".format(specnum1))
    file2.write("\n其他统计项\n共有中英文问号{}个\n".format(specnum1))
    otherslist = ["憨", "平"]
    for otheritem in otherslist:
        specnum2 = totallist.count(otheritem)
        print("共有{} {}个".format(otheritem, specnum2))
        file2.write("共有{} {}个\n".format(otheritem, specnum2))
    file2.close()
    print("以上输出已保存到txt文件中")

# 制作弹幕密度统计图
def generatechart():
    from datetime import datetime
    from datetime import timedelta
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import matplotlib
    
    for obj in objects:
        obj.time = obj.time % 86400
    # 对象重新排序
    objects.sort(key=lambda x: x.time, reverse=False)
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    delta = float(input("统计图的时间间隔分钟数（默认5）：") or 5)
    arraystart = datetime.fromtimestamp(starttime)
    timearray0 = datetime.fromtimestamp(objects[0].time)
    danmucount = 0
    plt.figure(figsize=(16, 9))
    if numpath == 1:
        plt.title(arraystart.strftime("%Y-%m-%d  ") + livename + "  弹幕密度统计图", fontsize=18)
    else:
        plt.title("弹幕密度统计图", fontsize=18)
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
                pltxs.append(timearray0.strftime("%H:%M"))
                pltys.append(danmucount / delta)
                timearray0 += timedelta(minutes=delta)
                danmucount = 1
    pltxs.append(timearray0.strftime("%H:%M"))
    pltys.append(danmucount / delta)
    # 用x,y坐标列表生成统计图
    plt.bar(pltxs,
            pltys,
            align='edge',
            color='lightblue')
    plt.savefig("output//" + "弹幕密度_" + vtbname + '_' + livename + ".png", dpi=300, bbox_inches='tight')
    print("已生成弹幕密度统计图")

# 制作词云
def generatecloud():
    import wordcloud
    import jieba
    
    print("词云创建中……")
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

# 主函数（迫真）
import json
import os

import DanmuMerge as DM

getinputs()
liveinformation()
generateobjects()
danmustatistic()
printdanmus()
giftstatistic()
printgifts()
others()
sig1 = input("\n是否生成弹幕密度统计图（输入非空值生成）：")
if sig1:
    generatechart()
sig2 = input("\n是否生成词云（输入非空值生成）：")
if sig2:
    generatecloud()
