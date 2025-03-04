import subprocess
import time
import cv2
import numpy as np

def adb_screenshot():
    """获取模拟器截图"""
    result = subprocess.run(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
    img_array = np.asarray(bytearray(result.stdout), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Failed to decode screenshot image.")
    return img

def match_template(screenshot, template):
    """在截图中查找模板图片的位置"""
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.7:  # 阈值可以根据实际情况调整
        return max_loc
    return None

def tap_on(x, y, times=1):
    """在指定位置点击"""
    for i in range(times):
        try:
            subprocess.run(['adb', 'shell', 'input', 'tap', str(x), str(y)], check=True)
            print(f"Clicked at ({x}, {y}) - Attempt {i + 1}/{times}")  # 增加日志输出
        except subprocess.CalledProcessError as e:
            print(f"Tap command failed with return code {e.returncode}")
            raise
        time.sleep(0.5)  # 等待一点时间间隔以便操作生效

template_path = r'D:/mypython/view/adb/clickImage/auto1.png'
template = cv2.imread(template_path, cv2.IMREAD_COLOR)

if template is None:
    raise ValueError(f"Failed to load template image from {template_path}")

while True:
    try:
        screenshot = adb_screenshot()
        position = match_template(screenshot, template)

        if position is None:  # 如果没有找到图像
            print("未找到目标图像")
            tap_on(806, 424, 2)  # 点击806, 424两次
            time.sleep(0.5) 
            tap_on(303, 499)  # 接着点击303, 499一次
            time.sleep(10)  # 等待5秒后重新检查
        else:
            print(f"已找到目标图像 at {position}")
            time.sleep(60)  # 如果找到了目标图像，等待60秒后重新检查
    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(5)  # 发生错误时也等待5秒后重试