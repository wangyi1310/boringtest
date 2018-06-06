import cv2 as cv
import math
import random
import os
import time
"""
参考网上的思路具体这样做通过
ADB 对手机进行操作，每次通过调用ADB提供的截图获取当前游戏的状态，
采用open_cv 进行获取坐标，确定相应的坐标之间距离
然后进行时间的计算，最后通过ADB提供模拟点击进行跳跃。
每次跳完之后都延迟1.*s  防止数据不稳定或者其他情况
"""
def get_instance():
    """
    获取距离
    """
    img = cv.imread("1.png")
    player_template = cv.imread('player.png')
    player = cv.matchTemplate(img, player_template, cv.TM_CCOEFF_NORMED)#匹配位置最后一个是采用何种匹配算法进行匹配

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(player)
    corner_loc = (max_loc[0] + 90, max_loc[1] + 230) #对角线
    player_spot = (max_loc[0] + 45,max_loc[1] + 230)
    cv.circle(img, player_spot, 10, (0, 255, 255), -1)
    cv.rectangle(img, max_loc, corner_loc, (0, 0, 255), 5)


    img_blur = cv.GaussianBlur(img, (5, 5), 0) #高斯模糊
    canny_img = cv.Canny(img_blur, 1, 10) #边缘检测

    height, width = canny_img.shape
    crop_img = canny_img[300:int(height/2), 0:width] #将图片切到自己想要的位置
    cv.namedWindow('img', cv.WINDOW_KEEPRATIO)
    for x in range(max_loc[0], max_loc[0]+90):  #屏蔽掉不需要的部分。
        for y in range(max_loc[1],max_loc[1]+230):
            canny_img[y][x] = 0
    crop_h, crop_w = crop_img.shape
    center_x, center_y = 0, 0

    max_x = 0
    for y in range(crop_h):
        for x in range(crop_w):
            if crop_img[y, x] == 255:
                if center_x == 0:
                    center_x = x
                if x > max_x:
                    center_y = y
                    max_x = x

    cv.circle(img, (center_x, center_y+300), 10, 255, -1)
    len =math.sqrt((center_x-(max_loc[0] + 45))*(center_x-(max_loc[0] + 45))+(center_y+300-(max_loc[1] + 230))*(center_y+300-(max_loc[1] + 230)))
    return len


def jump(distance):
    """
    获取跳跃距离算出跳跃时间并且执行
    :param distance:
    """
    press_time = int(distance * 1.5)
    press_time=max(200,press_time)
    print (press_time)
    cmd = 'adb shell input swipe 240 837 240 837 ' + str(press_time)
    try:
        os.system(cmd)
    except Exception:
        pass

def pull_screenshot():
    """
    获取屏幕截图
    将截图拷贝到本目录下
    :return:
    """
    os.system('adb shell screencap -p /sdcard/1.png')
    os.system('adb pull /sdcard/1.png .')

def check_screenshot():
    """
    检查是否存在原来的截图
    检查获取截图的方式如果存在移除重新打开进行。
    """
    if os.path.isfile('1.png'):
        os.remove('1.png')
    pull_screenshot()
if __name__=="__main__":
    #yes_or_no=input("请确定你已经打开ADB：")
    #if yes_or_no == "no":
    #    exit(0)
    while True:
 
        check_screenshot()
        jump(get_instance())
        a = random.randint(15, 50)
        sleeptime=a/10.0
        print (sleeptime)
        time.sleep(sleeptime)



