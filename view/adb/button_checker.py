import subprocess
import time
import cv2
import numpy as np
# 这个是好用的
def adb_screenshot():
    """获取模拟器截图"""
    result = subprocess.run(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
    img_array = np.asarray(bytearray(result.stdout), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("无法解码屏幕截图图像。")
    return img

def match_template(screenshot, template):
    """在截图中查找模板图片的位置"""
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.7:  # 阈值可以根据实际情况调整
        return max_loc
    return None

def click_position(x, y):
    """模拟点击指定位置"""
    subprocess.run(['adb', 'shell', 'input', 'tap', str(x), str(y)])

auto_template_path = r'D:/mypython/view/adb/clickImage/auto.png'

while True:
    try:
        screenshot = adb_screenshot()
        
        try:
            auto_template = cv2.imread(auto_template_path, cv2.IMREAD_COLOR)
            if auto_template is None:
                print(f"无法加载模板图像 {auto_template_path}")
            else:
                position = match_template(screenshot, auto_template)
                if position is None:
                    # 屏幕上没找到 auto 按钮
                    print("未找到 auto 按钮，执行点击操作")
                    # 点击两下 806,424
                    for _ in range(2):
                        click_position(806, 424)
                    time.sleep(0.1)
                    click_position(753,368) #奇术
                    time.sleep(0.1)
                    click_position(303, 499) #自动
                else:
                    print("找到了 auto 按钮，不进行操作")
        
        except cv2.error as cv_err:
            print(f"OpenCV 错误: {cv_err}")
        
        # 等待一段时间后继续下一次检查
        time.sleep(5)  # 根据需要调整等待时间
        
    except subprocess.CalledProcessError as sub_err:
        print(f"ADB 命令执行错误: {sub_err}")
        time.sleep(5)  # 发生错误时也等待5秒后重试
    except Exception as e:
        print(f"发生未知错误: {e}")
        time.sleep(5)  # 发生错误时也等待5秒后重试