import subprocess
import time
import cv2
import numpy as np
import pyautogui

def adb_screenshot():
    """获取模拟器截图"""
    result = subprocess.run(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
    img_array = np.asarray(bytearray(result.stdout), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def match_template(screenshot, template):
    """在截图中查找模板图片的位置"""
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.7:  # 阈值可以根据实际情况调整
        return max_loc
    return None

def tap_on(x, y, times=1):
    """在指定位置点击鼠标左键"""
    for _ in range(times):
        pyautogui.click(x, y)
        time.sleep(0.5)  # 等待一点时间间隔以便操作生效

template_path = r'D:/mypython/view/adb/clickImage/auto.png'
template = cv2.imread(template_path, cv2.IMREAD_COLOR)

found_target = False  # 标志位，用于判断是否找到了目标图像

while True:
    screenshot = adb_screenshot()
    position = match_template(screenshot, template)
    if position is None:  # 如果没有找到图像
        print("未找到目标图像")
        tap_on(807, 422, 5)  # 在指定位置点击鼠标左键五次
        pyautogui.press('u')  # 按下键盘上的"U"键
        time.sleep(1)  # 给予一些时间让界面更新
    else:
        print(f"已找到目标图像 at {position}")
        found_target = True  # 设置标志位为True，表示找到了目标图像
    
    if found_target:
        # 目标图像找到后，继续监控但不执行任何点击操作
        print("正在监控，确保auto保持打开状态...")
        time.sleep(1)  # 每秒检查一次，防止退出循环
    else:
        time.sleep(1)  # 每秒检查一次