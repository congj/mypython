import random
import subprocess
import time
import cv2
import numpy as np

def adb_command(cmd):
    """运行adb命令"""
    subprocess.run(f"adb {cmd}", shell=True)

def click(x, y):
    """在指定坐标点击"""
    adb_command(f"shell input tap {x} {y}")

def long_press(x, y, duration=3000):
    """在指定坐标长按"""
    adb_command(f"shell input swipe {x} {y} {x} {y} {duration}")

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
    if max_val > 0.9:  # 阈值可以根据实际情况调整
        return True
    return False

def check_image(image_path):
    """检查图像是否存在"""
    screenshot = adb_screenshot()
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    return match_template(screenshot, template)

# 动作列表及概率
actions = [
    (lambda: [click(806, 424) for _ in range(5)], "攻击", 20),
    (lambda: click(808, 328), "E卸势", 10),
    (lambda: click(875, 315), "R蓄力", 10),
    (lambda: long_press(875, 315, 3000), "R蓄力长按3秒", 10),
    (lambda: click(606, 306), "捡物品", 12.5),
    (lambda: click(753, 368), "1奇术", 10),
    (lambda: click(705, 418), "Q突进技能", 10),
    (lambda: click(693, 493), "tab爆发", 12.5),
    (lambda: click(722, 288), "处决", 12.5)  # 新增的处决动作
]

weights = [action[2] for action in actions]
actions_only = [(action[0], action[1]) for action in actions]

template_path = "D:/mypython/view/adb/clickImage/auto.png"
template = cv2.imread(template_path, cv2.IMREAD_COLOR)

while True:
    if check_image(template_path):
        print("检测到auto.png，等待10秒...")
        time.sleep(10)  # 如果检测到auto.png，则等待10秒后再次检查
    else:
        print("未检测到auto.png，执行随机动作...")
        action_to_do, action_name = random.choices(actions_only, weights=weights, k=1)[0]
        action_to_do()  # 执行选中的动作
        click(303, 499)  # 完成随机动作后点击(303, 499)
        
        # 确保auto.png恢复
        while not check_image(template_path):
            print("尝试恢复auto.png状态...")
            click(303, 499)  # 尝试通过点击恢复auto.png状态
            time.sleep(2)  # 给予一些时间让界面更新
        
        print("auto.png已恢复")
        time.sleep(1)  # 根据实际情况调整等待时间