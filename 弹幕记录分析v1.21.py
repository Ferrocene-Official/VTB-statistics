'''
作者：二茂铁Official
使用的第三方库：matplotlib,wordcloud,jieba
'''

#参数输入
def getinputs():
    print("注：各次直播的JSON文件请从 https://matsuri.icu/ 获取")
    input("请将需要分析的JSON文件放入与此程序同目录下的“input”文件夹中，完成后按回车键继续")
    paths=os.listdir("input")
    numpath=len(paths)
    num1=int(input("\n弹幕排行显示条数（默认20）：") or 20)
    num2=int(input("弹幕发送者排行显示条数（默认20）：") or 20)
    num3=int(input("打钱排行显示条数（默认10）：") or 10)
    return paths,numpath,num1,num2,num3

#数据预处理，逐条转移至新文档中
def jsonprocess():
    for i in range(numpath):
        file0=open(paths[i],'r',encoding='utf-8')
        text=file0.read()
        text=text.replace('\n','')
        file0.close()
        file1=open("弹幕记录总览"+str(i)+".txt",'w',encoding='utf-8')
        for ch in text:
            if ch!='}':
                file1.write(ch)
            else:
                file1.write(ch+'\n')
        file1.close()

#读取直播信息
def liveinformation():
    file1=open("弹幕记录总览0.txt",'r',encoding='utf-8')
    lines=file1.read()
    file1.close()
    dics=json.loads(lines,strict=False)
    vtbname=dics["info"]["name"]
    livename=dics["info"]["title"]
    records=dics["full_comments"]
    numdanmu=dics["info"]["total_danmu"]
    if not os.path.exists("output"):
        os.mkdir("output")
    if numpath==1:
        file2=open("output//"+vtbname+'_'+livename+".csv",'w',encoding='utf-8-sig')
    else:
        file2=open("output//"+vtbname+".csv",'w',encoding='utf-8-sig')
        for i in range(1,numpath):
            file1=open("弹幕记录总览"+str(i)+".txt",'r',encoding='utf-8')
            #弹幕记录合并
            lines=file1.read()
            file1.close()
            dics=json.loads(lines,strict=False)
            numdanmu=numdanmu+dics["info"]["total_danmu"]
            recordnew=dics["full_comments"]
            records.extend(recordnew)
    print("\n弹幕总数：{}条".format(numdanmu))
    file2.write("弹幕总数,{}\n".format(numdanmu))
    return records,vtbname,livename,file2

#读取弹幕及其发送者
def danmustatistic():
    danmutotal,nametotal={},{}
    totalline0=""
    for i in range(len(records)):
        if "text" in records[i]:
            danmu=records[i]["text"].replace(' ','')
            totalline0=totalline0+danmu+' '
            #相似弹幕合并，需根据统计对象修改
            if len(danmu)!=0:
                if "？？" in danmu and danmu[0]=="？" and danmu[-1]=="？":
                    danmu="？？？"
                elif "鹅鹅鹅" in danmu and danmu[0]=="鹅" and danmu[-1]=="鹅":
                    danmu="鹅鹅鹅"
                elif "哈哈哈" in danmu and danmu[0]=="哈" and danmu[-1]=="哈":
                    danmu="哈哈哈"
                elif "土土土" in danmu and danmu[0]=="土" and danmu[-1]=="土":
                    danmu="土土土"
                elif danmu=="好听好听":
                    danmu="好听"
                elif "ohhhh" in danmu:
                    danmu="ohhhhhhh"
                elif "OHHHH" in danmu:
                    danmu="OHHHHHHH"
                elif "\心萪/\心萪/\心萪/" in danmu:
                    danmu="\心萪/\心萪/\心萪/\心萪/\心萪/"
                elif "\妙妙/\妙妙/\妙妙/" in danmu:
                    danmu="\妙妙/\妙妙/\妙妙/\妙妙/\妙妙/"
                elif "\机萪/\机萪/\机萪/" in danmu:
                    danmu="\机萪/\机萪/\机萪/\机萪/\机萪/"
            if danmu not in danmutotal.keys():
                danmutotal[danmu]=1
            else:
                danmutotal[danmu]=danmutotal[danmu]+1
            name=records[i]["username"]
            if name not in nametotal.keys():
                nametotal[name]=1
            else:
                nametotal[name]=nametotal[name]+1
    return totalline0,danmutotal,nametotal

#输出弹幕频次排行和发送者排行
def printdanmus():
    items=list(danmutotal.items())
    items.sort(key=lambda x:x[1],reverse=True)
    print("\n弹幕排行")
    file2.write("\n弹幕排行\n序号,弹幕,数量\n")
    for i in range(num1):
        print("第{}：{}，共{}条".format(i+1,items[i][0],items[i][1]))
        file2.write("{},{},{}\n".format(i+1,items[i][0],items[i][1]))
    DD=list(nametotal.items())
    DD.sort(key=lambda x:x[1],reverse=True)
    print("\n弹幕发送者排行")
    file2.write("\n弹幕发送者排行\n序号,用户名,弹幕数\n")
    for i in range(num2):
        print("第{}：{}，弹幕{}条".format(i+1,DD[i][0],DD[i][1]))
        file2.write("{},{},{}\n".format(i+1,DD[i][0],DD[i][1]))

#读取SC、礼物和舰长
def giftstatistic():
    payertotal={}
    for i in range(len(records)):
        if "superchat_price" in records[i]:
            price=float(records[i]["superchat_price"])
            payer=records[i]["username"]
            if payer not in payertotal.keys():
                payertotal[payer]=0
            payertotal[payer]=payertotal[payer]+price
        elif "gift_price" in records[i]:
            price=float(records[i]["gift_price"])
            payer=records[i]["username"]
            if payer not in payertotal.keys():
                payertotal[payer]=0
            payertotal[payer]=payertotal[payer]+price
    return payertotal

#输出打钱排行
def printgifts():
    tiangou=list(payertotal.items())
    tiangou.sort(key=lambda x:x[1],reverse=True)
    print("\n打钱排行")
    file2.write("\n打钱排行\n序号,用户名,金额\n")
    for i in range(num3):
        print("第{}：{}，金额{:.1f}".format(i+1,tiangou[i][0],tiangou[i][1]))
        file2.write("{},{},{:.1f}\n".format(i+1,tiangou[i][0],tiangou[i][1]))

#输出其他统计项，需根据统计对象修改
def others():
    file1=open("弹幕记录总览0.txt",'r',encoding='utf-8')
    lines=file1.read()
    file1.close()
    if numpath>1:
        for i in range(1,numpath):
            file1=open("弹幕记录总览"+str(i)+".txt",'r',encoding='utf-8')
            lines=lines+file1.read()
            file1.close()
    spechnum1=lines.count("?")+lines.count("？")
    spechnum2=lines.count("鹅")
    spechnum3=lines.count("憨")
    print("\n其他统计项\n共有中英文问号{}个".format(spechnum1))
    print("共有鹅字{}个".format(spechnum2))
    print("共有憨字{}个".format(spechnum3))
    file2.write("\n其他统计项\n项目,数量\n")
    file2.write("中英文问号,{}\n".format(spechnum1))
    file2.write("鹅,{}\n".format(spechnum2))
    file2.write("憨,{}\n".format(spechnum3))
    file2.close()
    print("以上输出已保存到csv文件中")

#制作弹幕密度-时间统计图
def generatechart():
    from datetime import datetime
    from datetime import timedelta
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import matplotlib
    matplotlib.rcParams['font.family']='SimHei'
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    delta=int(input("\n弹幕密度统计图的时间间隔分钟数（默认5）：") or 5)
    timestamp0=(int(records[0]["time"])/1000)
    timearray0=datetime.fromtimestamp(timestamp0)
    danmucount=1
    plt.figure(figsize=(16,8))
    #坐标轴设置
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(20/delta))
    plt.xlabel("时间",fontsize=18)
    plt.ylabel("弹幕数量",fontsize=18)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    for i in range(1,len(records)):
        if "text" in records[i]:
            timestamp=(int(records[i]["time"])/1000)
            timearray=datetime.fromtimestamp(timestamp)
            if timearray.strftime("%H:%M")<(timearray0+timedelta(minutes=delta)).strftime("%H:%M"):
                danmucount=danmucount+1
            else:
                plt.bar(timearray0.strftime("%H:%M"),
                        danmucount,
                        align='edge',
                        color='lightblue')
                timearray0=timearray0+timedelta(minutes=delta)
                danmucount=1
    plt.bar(timearray0.strftime("%H:%M"),
            danmucount,
            align='edge',
            color='lightblue')
    plt.savefig("output//"+"弹幕密度_"+vtbname+'_'+livename+".png",dpi=300,bbox_inches='tight')
    print("已生成弹幕密度统计图")

#制作词云
def generatecloud():
    import wordcloud
    import jieba
    print("词云创建中……")
    w=wordcloud.WordCloud(font_path="msyh.ttc",
                          collocations=False,
                          width=2000,
                          height=2000,
                          background_color="white",
                          max_words=400)
    w.generate(totalline0)
    if numpath==1:
        w.to_file("output//"+"弹幕云_"+vtbname+'_'+livename+".png")
    else:
        w.to_file("output//"+"弹幕云_"+vtbname+".png")
    total=jieba.lcut(totalline0)
    words=' '.join(total)
    w.generate(words)
    if numpath==1:
        w.to_file("output//"+"弹幕词云_"+vtbname+'_'+livename+".png")
    else:
        w.to_file("output//"+"弹幕词云_"+vtbname+".png")
    signal=input("词云创建完成，按回车键结束程序")

#主函数
import json
import os
paths,numpath,num1,num2,num3=getinputs()
spechnum=jsonprocess()
records,vtbname,livename,file2=liveinformation()
totalline0,danmutotal,nametotal=danmustatistic()
printdanmus()
payertotal=giftstatistic()
printgifts()
others()
if numpath==1:
    generatechart()
signal=int(input("\n是否生成词云（1/0）："))
if signal:
    generatecloud()
