# 弹幕合并逻辑

# 新科娘
def merge_xinke(danmu):
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
    elif "/心萪\\/心萪\\/心萪\\" in danmu:
        danmu = "/心萪\\/心萪\\/心萪\\"
    elif "\妙妙/\妙妙/\妙妙/" in danmu:
        danmu = "\妙妙/\妙妙/\妙妙/"
    elif "\机萪/\机萪/\机萪/" in danmu:
        danmu = "\机萪/\机萪/\机萪/"
    elif "\土萪/\土萪/\土萪/" in danmu:
        danmu = "\土萪/\土萪/\土萪/"
    elif "\心萪/\妙妙/\心萪/\妙妙/" in danmu:
        danmu = "\心萪/\妙妙/\心萪/\妙妙/"
    return danmu

# Hiiro
def merge_hiiro(danmu):
    if "？？" in danmu and danmu[0] == "？" and danmu[-1] == "？":
        danmu = "？？？"
    elif "哈哈哈" in danmu and danmu[0] == "哈" and danmu[-1] == "哈":
        danmu = "哈哈哈"
    elif danmu == "好听好听":
        danmu = "好听"
    elif "ohhhh" in danmu:
        danmu = "ohhhhhhh"
    elif "OHHHH" in danmu:
        danmu = "OHHHHHHH"
    elif "888888" in danmu and danmu[0] == "8" and danmu[-1] == "8":
        danmu = "88888888"
    elif "✂️✂️✂️" in danmu:
        danmu = "✂️✂️✂️"
    elif danmu == "⎛⎝≥⏝⏝≤⎛⎝Hiiro⎛⎝≥⏝⏝≤⎛⎝":
        danmu = "⎛⎝≥⏝⏝≤⎛⎝hiiro⎛⎝≥⏝⏝≤⎛"
    elif danmu == "\Hiiro/\Hiiro/":
        danmu = "\hiiro/\hiiro/"
    return danmu

# 小希小桃
def merge_xitao(danmu):
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
    elif "\桃桃/\桃桃/\桃桃/" in danmu:
        danmu = "\桃桃/\桃桃/\桃桃/"
    return danmu

if __name__ == "__main__":
    danmu = input("输入弹幕：")
    print("合并结果：" + merge_xinke(danmu))
