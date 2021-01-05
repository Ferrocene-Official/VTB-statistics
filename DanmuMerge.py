# 弹幕合并逻辑，建议程序使用者根据自身经验进行修改

import re

# 通用合并
def merge_general(danmu):
    if "？？" in danmu and danmu[0] == "？" and danmu[-1] == "？":
        danmu = "？？？"
    elif "哈哈哈" in danmu and danmu[0] == "哈" and danmu[-1] == "哈":
        danmu = "哈哈哈"
    elif "ohhhh" in danmu:
        danmu = "ohhhhhhh"
    elif "OHHHH" in danmu:
        danmu = "OHHHHHHH"
    else:
        # 合并常规打call弹幕
        match = re.search("(\\\\\w{1,5}/){3}", danmu)
        if match:
            danmu = match.group()
    return danmu

# 新科娘
def merge_xinke(danmu):
    # 合并重复字符弹幕
    repeatlist = ['哈', '鹅', '土', '痛', '疼', '甜']
    for ch in repeatlist:
        if "{}{}{}".format(ch, ch, ch) in danmu and danmu[0] == ch and danmu[-1] == ch:
            danmu = "{}{}{}".format(ch, ch, ch)
            return danmu
    if "？？" in danmu and danmu[0] == "？" and danmu[-1] == "？":
        danmu = "？？？"
    if danmu == "好听好听":
        danmu = "好听"
    elif "ohhhh" in danmu:
        danmu = "ohhhhhhh"
    elif "OHHHH" in danmu:
        danmu = "OHHHHHHH"
    elif "/心萪\\/心萪\\/心萪\\" in danmu:
        danmu = "/心萪\\/心萪\\/心萪\\"
    elif "\心萪/\妙妙/\心萪/\妙妙/" in danmu:
        danmu = "\心萪/\妙妙/\心萪/\妙妙/"
    elif "\心萪/\机萪/\心萪/\机萪/" in danmu:
        danmu = "\心萪/\机萪/\心萪/\机萪/"
    elif "\憨憨/\小美人/\憨憨/\小美人/" in danmu:
        danmu = "\憨憨/\小美人/\憨憨/\小美人/"
    elif "✂️✂️✂️" in danmu:
        danmu = "✂️✂️✂️"
    else:
        # 合并常规打call弹幕
        match = re.search("(\\\\\w{1,5}/){3}", danmu)
        if match:
            danmu = match.group()
    return danmu

# Hiiro
def merge_hiiro(danmu):
    if "？？" in danmu and danmu[0] == "？" and danmu[-1] == "？":
        danmu = "？？？"
    elif "哈哈哈" in danmu and danmu[0] == "哈" and danmu[-1] == "哈":
        danmu = "哈哈哈"
    elif "ohhhh" in danmu:
        danmu = "ohhhhhhh"
    elif "OHHHH" in danmu:
        danmu = "OHHHHHHH"
    elif "888888" in danmu and danmu[0] == "8" and danmu[-1] == "8":
        danmu = "88888888"
    elif "✂️✂️✂️" in danmu:
        danmu = "✂️✂️✂️"
    return danmu

# 虚研社
def merge_xuyanshe(danmu):
    match = re.search("(\\\\\w{1,5}/){3}", danmu)
    if match:
        danmu = match.group()
    elif "？？" in danmu and danmu[0] == "？" and danmu[-1] == "？":
        danmu = "？？？"
    elif "哈哈哈" in danmu and danmu[0] == "哈" and danmu[-1] == "哈":
        danmu = "哈哈哈"
    elif danmu == "好听好听":
        danmu = "好听"
    elif "888888" in danmu and danmu[0] == "8" and danmu[-1] == "8":
        danmu = "88888888"
    elif "ohhhh" in danmu:
        danmu = "ohhhhhhh"
    elif "OHHHH" in danmu:
        danmu = "OHHHHHHH"
    return danmu

# 歌姬
def merge_geji(danmu):
    match = re.search("(\\\\\w{1,5}/){3}", danmu)
    if match:
        danmu = match.group()
    if "？？" in danmu and danmu[0] == "？" and danmu[-1] == "？":
        danmu = "？？？"
    elif "哈哈哈" in danmu and danmu[0] == "哈" and danmu[-1] == "哈":
        danmu = "哈哈哈"
    elif danmu == "好听好听":
        danmu = "好听"
    elif "888888" in danmu and danmu[0] == "8" and danmu[-1] == "8":
        danmu = "88888888"
    elif "ohhhh" in danmu:
        danmu = "ohhhhhhh"
    elif "OHHHH" in danmu:
        danmu = "OHHHHHHH"
    return danmu

# 测试用
def experiment(danmu):
    match = re.search("(\\\\\w{1,5}/){3}", danmu)
    if match:
        danmu = match.group()
    return danmu

if __name__ == "__main__":
    danmu = input("输入弹幕：")
    print("合并结果：" + merge_general(danmu))
