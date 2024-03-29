from DanmuMerge import merge_xinke as merge
import os
import json
import plotly.express as px
import gradio as gr
from datetime import timedelta
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import font_manager
import matplotlib
import wordcloud
import jieba

matplotlib.use("Agg")

fontname = ["SourceHanSansSC-Normal.otf", "楷体"]
font_manager.fontManager.addfont(fontname[0])
for font in font_manager.fontManager.ttflist:
    print(font.name, " - ",font.fname)

弹幕内容排行榜 = "弹幕内容排行榜"
水友弹幕互动排行榜 = "水友弹幕互动排行榜"
直播付费金额排行榜 = "直播付费金额排行榜"
弹幕密度统计图 = "弹幕密度统计图"
# 读取直播信息


class Live():
    def __init__(self, records, vtbname, livename, starttime, endtime):
        self.records = records
        self.vtbname = vtbname
        self.livename = livename
        self.endtime = endtime
        self.starttime = starttime

    def __init__(self, path):
        print("load file:", path)
        file1 = open(path, 'r', encoding='utf-8')
        text = file1.read().replace('\n', '')
        file1.close()
        dics = json.loads(text, strict=False)
        self.vtbname = dics["info"]["name"]
        self.livename = dics["info"]["title"]
        self.starttime = dics["info"]["start_time"]
        self.endtime = dics["info"]["end_time"]
        self.records = dics["full_comments"]

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


# 二维数组转换为label显示的内容
def array2label(data, num=0):
    result = {}
    lenth = len(data)
    if (lenth < 1):
        return result
    if (num < 1):
        num = lenth
    base = data[0][1]
    for i in range(min(num, lenth)):
        result[data[i][0] + " - " + str(data[i][1])] = data[i][1]/base
    return result

# 二维数组转换为打印的内容


def printData(title, content, data, num=0):
    text = "\n" + title+"\n"

    lenth = len(data)
    if (lenth < 1):
        text += "无\n"
        return text
    if (num < 1):
        num = lenth

    for i in range(min(num, lenth)):
        text += (content.format(
            i + 1, data[i][0], data[i][1]))
    return text

# 输出其他统计项，需根据统计对象修改


def others(totallist):
    specnum1 = totallist.count("?") + totallist.count("？")
    text = ("\n其他统计项\n共有中英文问号{}个\n".format(specnum1))
    otherslist = ["憨", "平", "✂️"]
    for otheritem in otherslist:
        specnum2 = totallist.count(otheritem)
        text += ("共有{} {}个\n".format(otheritem, specnum2))
    return text

# 制作弹幕密度统计图所需的数据


def generatechartData(objects, ref_time, starttime, dtime):

    # 消去日期
    for obj in objects:
        obj.time = obj.time % 86400
    # 对象重新排序
    objects.sort(key=lambda x: x.time, reverse=False)
    timearray0 = datetime.fromtimestamp(objects[0].time)
    danmucount = 0

    time_8hour = timedelta(hours=8)
    time_offset = datetime.fromtimestamp(0)
    if ref_time:
        time_offset = datetime.fromtimestamp(
            starttime / 1000) - time_offset + time_8hour
    else:
        time_offset = time_offset - time_offset

    pltxs, pltys = [], []
    for obj in objects:
        if isinstance(obj, Danmu) or isinstance(obj, SC):
            timearray = datetime.fromtimestamp(obj.time)
            if timearray < timearray0 + timedelta(minutes=dtime):
                danmucount += 1
            else:
                pltxs.append((timearray0-time_offset).strftime("%H:%M"))
                pltys.append(danmucount / dtime)
                timearray0 += timedelta(minutes=dtime)
                danmucount = 1
                # 补充无弹幕时段数据
                while timearray0 + timedelta(minutes=dtime) < timearray:
                    pltxs.append((timearray0-time_offset).strftime("%H:%M"))
                    pltys.append(0)
                    timearray0 += timedelta(minutes=dtime)
    pltxs.append((timearray0-time_offset).strftime("%H:%M"))
    pltys.append(danmucount / dtime)
    return pltxs, pltys

# 绘制弹幕密度统计图

def generatechart(pltxs, pltys, dtime, title):
    matplotlib.rcParams['font.sans-serif'] = ['Source Han Sans SC']
    plt.figure(figsize=(16, 9))
    plt.title(title, fontsize=18)

    # 设置坐标轴
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(20 / dtime))
    plt.xlabel("时间", fontsize=18)
    plt.ylabel("弹幕密度（条/分钟）", fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.bar(pltxs,
            pltys,
            # align='edge',
            color='lightblue')
    return plt

# 制作词云


def generatecloud(totallist, cloud):
    result = []
    w = wordcloud.WordCloud(
                            font_path=fontname[0],
                            collocations=False,
                            width=2000,
                            height=2000,
                            background_color="white",
                            max_words=400)
    if len(cloud[0]) > 0:
        w.generate(totallist)
        w.to_file(cloud[0])
        result.append(cloud[0])
    if len(cloud[1]) > 0:
        total = jieba.lcut(totallist)
        words = ','.join(total)
        w.generate(words)
        w.to_file(cloud[1])
        result.append(cloud[1])

    return result

# 程序选项
 # files 待分析的文件（目前只分析一个）, works 输出内容 ["文本框内容", "弹幕密度统计图", "弹幕云", "词云" ]
 # num1=30 弹幕内容排行榜, num2=20 水友弹幕互动排行榜, num3=10 直播付费金额排行榜,
 # ref_time=True 弹幕密度统计图使用相对时间, dtime=2 统计图时间间隔(分钟)


def runanalysis(files, works=[弹幕密度统计图], plot_type="Matplotlib", num1=30, num2=20, num3=10, dtime=2, ref_time=True):
    os.makedirs('/tmp/output', exist_ok=True)
    log_text = "分析开始时间：{}\n".format(datetime.now())
    # print(files)
    # for idx, file in enumerate(files):
    #     print("idx=",idx)
    #     print("file=" ,file)
    #     print("name=",file.name)
    #     break

    file_output = []
    if (files == None):
        return None, [], {}, {}, {}, file_output,  "请输入文件"

    file0 = files[0].name
    print("file0:", file0)
    if not file0.endswith(".json"):
        return None, [], {}, {}, {}, file_output, "文件格式错误，请输入json文件"

    live = Live(file0)
    # time.sleep(10)

    log_text += "已读取全部JSON文件，正在解析数据\n"

    # 来自generateobjects()
    objects = []
    for record in live.records:
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

    # 读取弹幕及其发送者,来自 danmustatistic()
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
    text = "弹幕总数：{}条\n".format(numdanmu)
    text_summary = text

    # 将原始弹幕列表转为字符串，用于制作词云
    totallist = ','.join(totallist)

    danmunums = list(danmutotal.items())
    danmunums.sort(key=lambda x: x[1], reverse=True)
    danmunums = danmunums[0:num1]
    text += printData(弹幕内容排行榜, "第{}：{}，共{}条\n", danmunums)
    danmunums = array2label(danmunums)

    gatlings = list(nametotal.items())
    gatlings.sort(key=lambda x: x[1], reverse=True)
    gatlings = gatlings[0:num2]
    text += printData(水友弹幕互动排行榜, "第{}：{}，弹幕{}条\n", gatlings)
    gatlings = array2label(gatlings)

    # 读取SC、礼物和舰长 giftstatistic():
    payertotal = {}
    for obj in objects:
        if isinstance(obj, Gift) or isinstance(obj, SC):
            if obj.uname not in payertotal.keys():
                payertotal[obj.uname] = 0
            payertotal[obj.uname] += float(obj.price)

    tiangous = list(payertotal.items())
    tiangous.sort(key=lambda x: x[1], reverse=True)
    tiangous = tiangous[0:num3]
    text += printData(直播付费金额排行榜, "第{}：{}，金额{:.1f}\n", tiangous)
    tiangous = array2label(tiangous)
    text += others(totallist)

    cloud = ["", ""]

    cloud_visiable = "弹幕云" in works
    if cloud_visiable:
        cloud[0] = "/tmp/output/" + "弹幕云_" + \
            live.vtbname + '_' + live.livename + ".png"

    if "词云" in works:
        cloud_visiable = True
        cloud[1] = "/tmp/output/" + "词云_" + \
            live.vtbname + '_' + live.livename + ".png"

    # print("cloud=", cloud)
    cloud = generatecloud(totallist, cloud)
    file_output.extend(cloud)

    if (len(text) > 0):
        text_path = "/tmp/output/" + live.vtbname + '_' + live.livename + ".txt"
        file2 = open(text_path, 'w', encoding='utf-8')
        file2.write(text)
        file2.close()
        file_output.append(text_path)

    if "文本框内容" not in works:
        text = text_summary

    sigfigure = 弹幕密度统计图 in works
    if sigfigure:
        figure_title = 弹幕密度统计图
        figure_path = "/tmp/output/" + 弹幕密度统计图 + "_" + \
            live.vtbname + '_' + live.livename + ".png"
        if len(files) == 1:
            arraystart = datetime.fromtimestamp(live.starttime / 1000)
            figure_title = arraystart.strftime(
                "%Y-%m-%d %H:%M ") + live.vtbname + " " + live.livename + " " + 弹幕密度统计图
        plt = None
        pltxs, pltys = generatechartData(objects, ref_time, live.starttime,
                                         dtime)
        if plot_type == "Plotly":
            fig = px.line(y=pltys, x=pltxs)
            fig.update_layout(
                title=figure_title,
                xaxis_title="时间",
                yaxis_title="弹幕密度（条/分钟）",
            )
            plt = fig
        else:
            plt = generatechart(pltxs, pltys, dtime, figure_title)
            plt.savefig(figure_path, dpi=300, bbox_inches='tight')
            file_output.append(figure_path)

    return gr.Plot.update(visible=sigfigure, value=plt), gr.Gallery.update(visible=cloud_visiable, value=cloud), danmunums, gatlings, tiangous, file_output, text


inputs = [
    gr.File(label="待分析的文件", file_count="multiple"
            ),
    gr.CheckboxGroup(
        ["文本框内容", "弹幕密度统计图", "弹幕云", "词云", ], label="输出内容(输出弹幕云&词云会消耗较多时间)", value=[弹幕密度统计图]
    ),
    gr.Dropdown(["Matplotlib", "Plotly"], label="绘图模式", value="Matplotlib"),
    gr.Slider(0, 500, value=30, label=弹幕内容排行榜),
    gr.Slider(0, 500, value=20, label=水友弹幕互动排行榜),
    gr.Slider(0, 500, value=10, label=直播付费金额排行榜),
    gr.Slider(0, 60, value=2, label="统计图时间间隔(分钟)"),
    gr.Checkbox(label="弹幕密度统计图使用相对时间", value=True),
]


outputs = [gr.Plot(label=弹幕密度统计图, visible=False),
           gr.Gallery(type="filepath", label="弹幕云&词云", visible=False).style(
               grid=[1, 1, 2, 2, 3], height="auto", container=False),
           gr.Label(label=弹幕内容排行榜),
           gr.Label(label=水友弹幕互动排行榜),
           gr.Label(label=直播付费金额排行榜),
           gr.File(label="输出文件", file_count="multiple"),
           gr.TextArea(label="分析结果"),
           ]
demo = gr.Interface(
    title="弹幕数据分析器",
    fn=runanalysis,
    inputs=inputs,
    outputs=outputs,
    examples=[
        [[os.path.join(os.path.dirname(__file__), "sample/弥希Miki_弥希MIKI的ACG广播部_1668257873478.json")],
            ["弹幕密度统计图", "弹幕云", "词云"]],
        [[os.path.join(os.path.dirname(__file__), "sample/小柔Channel_唱会儿__1669112994818.json")],
            ["文本框内容", "弹幕密度统计图"]],
    ],
    cache_examples=False,
    description="本程序用于分析 https://matsuri.icu/ 网站上JSON格式的直播数据记录，基于 https://github.com/Ferrocene-Official/VTB-statistics"
)

if __name__ == "__main__":
    demo.launch()
