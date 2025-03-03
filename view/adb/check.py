import os
import time
import cv2
import numpy as np
import pyautogui

# 定义助手图标的文件路径，该图标用于后续屏幕匹配检测
assistant_image_path = r"D:\mypython\view\adb\clickImage\assistant.png"
# 定义攻击图标的文件路径，同样用于屏幕匹配检测
attack_image_path = r"D:\mypython\view\adb\clickImage\attack.png"
# 定义自动图标的文件路径，用于判断是否需要跳过后续操作
auto_image_path = r"D:\mypython\view\adb\clickImage\auto.png"

def check_adb_connection():
    """
    检查ADB设备是否连接正常。
    :return: 如果至少有一个设备连接，则返回True；否则返回False。
    """
    response = os.popen('adb devices').read()
    if 'device' in response and '\tdevice' in response:
        return True
    else:
        print("未检测到ADB设备连接，请确保设备已正确连接并启用了ADB调试。")
        return False

def capture_screen_adb():
    """
    使用ADB捕获设备屏幕截图并保存为screenshot.png。
    """
    os.system('adb exec-out screencap -p > screenshot.png')

def is_image_on_screen(image_path):
    """
    该函数用于检查指定的图像是否存在于当前屏幕上。
    :param image_path: 待检查图像的文件路径
    :return: 如果图像在屏幕上返回 True，否则返回 False
    """
    try:
        template = cv2.imread(image_path, 0)
        w, h = template.shape[::-1]
        # 使用ADB获取屏幕截图
        capture_screen_adb()
        screenshot = cv2.imread('screenshot.png', 0)
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            return True
        return False
    except Exception as e:
        print(f"Error checking image on screen: {e}")
        return False

if check_adb_connection():
    try:
        while True:
            print("开始新一轮的屏幕检测...")
            if is_image_on_screen(auto_image_path):
                print("检测到自动图标，本次不执行任何操作，等待下一次检测。")
                pass
            else:
                print("未检测到自动图标，继续进行其他图标检测。")
                attack_exists = is_image_on_screen(attack_image_path)
                assistant_exists = is_image_on_screen(assistant_image_path)

                if not attack_exists:
                    print("未检测到攻击图标，点击坐标 (809, 426)。")
                    pyautogui.click(809, 426)
                elif attack_exists and not assistant_exists:
                    print("检测到攻击图标，但未检测到助手图标，点击坐标 (809, 426)。")
                    pyautogui.click(809, 426)
                if assistant_exists:
                    print("检测到助手图标，点击坐标 (304, 502)。")
                    pyautogui.click(304, 502)

            print("本次检测结束，等待 3 秒后进行下一次检测。")
            time.sleep(3)

    except KeyboardInterrupt:
        print("程序被用户手动终止。")