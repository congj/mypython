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

templates = [
    ('auto', r'D:/mypython/view/adb/clickImage/auto.png'),
    ('assistant', r'D:/mypython/view/adb/clickImage/assistant.png'),
    ('attack2', r'D:/mypython/view/adb/clickImage/attack2.png'),  # 修正路径
    ('attack0', r'D:/mypython/view/adb/clickImage/attack0.png'),
    ('attack1', r'D:/mypython/view/adb/clickImage/attack1.png'),
]

while True:
    try:
        screenshot = adb_screenshot()
        found_any = False
        
        for button_name, template_path in templates:
            try:
                template = cv2.imread(template_path, cv2.IMREAD_COLOR)
                if template is None:
                    print(f"无法加载模板图像 {template_path}")
                    continue
                
                position = match_template(screenshot, template)
                if position is not None:
                    x, y = position
                    print(f"找到了 {button_name} 按钮，在位置 {position}")
                    click_position(x, y)
                    found_any = True
                    break
            except cv2.error as cv_err:
                print(f"OpenCV 错误: {cv_err}")
        
        if not found_any:
            print("未找到任何目标图像")
        
        # 等待一段时间后继续下一次检查
        time.sleep(5)  # 根据需要调整等待时间
        
    except subprocess.CalledProcessError as sub_err:
        print(f"ADB 命令执行错误: {sub_err}")
        time.sleep(5)  # 发生错误时也等待5秒后重试
    except Exception as e:
        print(f"发生未知错误: {e}")
        time.sleep(5)  # 发生错误时也等待5秒后重试