'''
作者：二茂铁Official
更新时间：2020/10/31
使用的第三方库：matplotlib,wordcloud,jieba
'''

# 参数输入
def getinputs():
    global paths, numpath, num1, num2, num3
    print("注：各次直播的JSON文件请从 https://matsuri.icu/ 获取")
    input("请在本程序同目录下创建“input”文件夹，将需要分析的一个或多个JSON文件放入其中，完成后按回车键继续")
    paths = os.listdir("input")
    numpath = len(paths)
    num1 = int(input("\n弹幕排行显示条数（默认20）：") or 20)
    num2 = int(input("弹幕发送者排行显示条数（默认20）：") or 20)
    num3 = int(input("打钱排行显示条数（默认10）：") or 10)

# 读取直播信息
def liveinformation():
    global records, vtbname, livename, file2
    file1 = open("input//" + paths[0], 'r', encoding='utf-8')
    text = file1.read().replace('\n','')
    file1.close()
    dics = json.loads(text, strict=False)
    vtbname = dics["info"]["name"]
    livename = dics["info"]["title"]
    records = dics["full_comments"]
    numdanmu = dics["info"]["total_danmu"]
    if not os.path.exists("output"):
        os.mkdir("output")
    # 创建记录输出的文本文档
    if numpath == 1:
        file2 = open("output//" + vtbname + '_' + livename + ".txt", 'w', encoding='utf-8')
    else:
        file2 = open("output//" + vtbname + ".txt", 'w', encoding='utf-8')
        for i in range(1, numpath):
            file1 = open("input//" + paths[i], 'r', encoding='utf-8')
            # 弹幕记录合并
            text = file1.read().replace('\n','')
            file1.close()
            dics = json.loads(text, strict=False)
            numdanmu = numdanmu + dics["info"]["total_danmu"]
            recordnew = dics["full_comments"]
            records.extend(recordnew)
    print("\n弹幕总数：{}条".format(numdanmu))
    file2.write("弹幕总数：{}条\n".format(numdanmu))

# 弹幕合并逻辑（需根据统计对象修改）
def merge(danmu):
    if "？？" in danmu and danmu[0] == "？" and danmu[-1] == "？":
        danmu = "？？？"
    elif "鹅鹅鹅" in danmu and danmu[0] == "鹅" and danmu[-1] == "鹅":
        danmu = "鹅鹅鹅"
    elif "哈哈哈" in danmu and danmu[0] == "哈" and danmu[-1] == "哈":
        danmu = "哈哈哈"
    elif "土土土" in danmu and danmu[0] == "土" and danmu[-1] == "土":
        danmu = "土土土"
    elif danmu == "好听好听":
        danmu = "好听"
    elif "ohhhh" in danmu:
        danmu = "ohhhhhhh"
    elif "OHHHH" in danmu:
        danmu = "OHHHHHHH"
    elif "\心萪/\心萪/\心萪/" in danmu:
        danmu = "\心萪/\心萪/\心萪/"
    elif "\妙妙/\妙妙/\妙妙/" in danmu:
        danmu = "\妙妙/\妙妙/\妙妙/"
    elif "\机萪/\机萪/\机萪/" in danmu:
        danmu = "\机萪/\机萪/\机萪/"
    elif "\土萪/\土萪/\土萪/" in danmu:
        danmu = "\土萪/\土萪/\土萪/"
    elif "\心萪/\妙妙/\心萪/\妙妙/" in danmu:
        danmu = "\心萪/\妙妙/\心萪/\妙妙/"
    return danmu

# 读取弹幕及其发送者
def danmustatistic():
    global totallist, danmutotal, nametotal
    danmutotal, nametotal = {}, {}
    totallist = []
    for i in range(len(records)):
        if "text" in records[i]:
            danmu = records[i]["text"].replace(' ', '')
            totallist.append(danmu)
            if len(danmu) != 0:
                danmu = merge(danmu)
            if danmu not in danmutotal.keys():
                danmutotal[danmu] = 1
            else:
                danmutotal[danmu] = danmutotal[danmu] + 1
            name = records[i]["username"]
            if name not in nametotal.keys():
                nametotal[name] = 1
            else:
                nametotal[name] = nametotal[name] + 1
    totallist = str(totallist)
    totallist = totallist.replace("'", "")

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
    for i in range(len(records)):
        if "superchat_price" in records[i]:
            price = float(records[i]["superchat_price"])
            payer = records[i]["username"]
            if payer not in payertotal.keys():
                payertotal[payer] = 0
            payertotal[payer] = payertotal[payer] + price
        elif "gift_price" in records[i]:
            price = float(records[i]["gift_price"])
            payer = records[i]["username"]
            if payer not in payertotal.keys():
                payertotal[payer] = 0
            payertotal[payer] = payertotal[payer] + price

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
    file1 = open("input//" + paths[0], 'r', encoding='utf-8')
    lines = file1.read()
    file1.close()
    if numpath > 1:
        for i in range(1, numpath):
            file1 = open("input//" + paths[i], 'r', encoding='utf-8')
            lines = lines + file1.read()
            file1.close()
    specnum1: int = lines.count("?") + lines.count("？")
    specnum2 = lines.count("鹅")
    specnum3 = lines.count("憨")
    print("\n其他统计项\n共有中英文问号{}个".format(specnum1))
    print("共有鹅字{}个".format(specnum2))
    print("共有憨字{}个".format(specnum3))
    file2.write("\n其他统计项\n共有中英文问号{}个\n".format(specnum1))
    file2.write("共有鹅字{}个\n".format(specnum2))
    file2.write("共有憨字{}个\n".format(specnum3))
    file2.close()
    print("以上输出已保存到txt文件中")

# 制作弹幕密度-时间统计图
def generatechart():
    from datetime import datetime
    from datetime import timedelta
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import matplotlib
    matplotlib.rcParams['font.family'] = 'SimHei'
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    delta = float(input("弹幕密度统计图的时间间隔分钟数（默认5）：") or 5)
    timestart = (int(records[0]["time"]) / 1000)
    arraystart = datetime.fromtimestamp(timestart)
    danmustamps = []
    for i in range(len(records)):
        if "text" in records[i]:
            danmustamps.append(int((int(records[i]["time"]) / 1000)) % 86400)
    danmustamps.sort()
    timearray0 = datetime.fromtimestamp(danmustamps[0])
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
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    pltxs, pltys = [], []
    for i in range(len(danmustamps)):
        timearray = datetime.fromtimestamp(danmustamps[i])
        if timearray.strftime("%H:%M") < (timearray0 + timedelta(minutes=delta)).strftime("%H:%M"):
            danmucount = danmucount + 1
        else:
            pltxs.append(timearray0.strftime("%H:%M"))
            pltys.append(danmucount / delta)
            timearray0 = timearray0 + timedelta(minutes=delta)
            danmucount = 1
    pltxs.append(timearray0.strftime("%H:%M"))
    pltys.append(danmucount / delta)
    # 用x,y坐标列表生成统计图
    plt.bar(pltxs,
            pltys,
            align='edge',
            color='lightblue')
    if numpath == 1:
        plt.savefig("output//" + "弹幕密度_" + vtbname + '_' + livename + ".png", dpi=300, bbox_inches='tight')
    else:
        plt.savefig("output//" + "弹幕密度_" + vtbname + ".png", dpi=300, bbox_inches='tight')
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
    if numpath == 1:
        w.to_file("output//" + "弹幕云_" + vtbname + '_' + livename + ".png")
    else:
        w.to_file("output//" + "弹幕云_" + vtbname + ".png")
    total = jieba.lcut(totallist)
    words = ' '.join(total)
    w.generate(words)
    if numpath == 1:
        w.to_file("output//" + "弹幕词云_" + vtbname + '_' + livename + ".png")
    else:
        w.to_file("output//" + "弹幕词云_" + vtbname + ".png")

# 主函数（迫真）
import json
import os

getinputs()
liveinformation()
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
sig3 = input("\n运行完毕，按回车键结束程序")
