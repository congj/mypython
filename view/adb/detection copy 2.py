import os
import cv2
import numpy as np
import pyautogui
import time

# 定义图片所在目录
IMAGE_DIR = r"D:/mypython/view/adb/clickImage"

# 定义各图标的文件路径 0 剑 1枪 2扇
ATTACK_IMAGE_PATH = os.path.join(IMAGE_DIR, "attack2.png")
ASSISTANT_IMAGE_PATH = os.path.join(IMAGE_DIR, "assistant.png")
AUTO_IMAGE_PATH = os.path.join(IMAGE_DIR, "auto.png")

# 统一的等待时间间隔，可根据实际情况调整
WAIT_INTERVAL = 0.1

def load_images():
    try:
        attack_template = cv2.imread(ATTACK_IMAGE_PATH, 0)
        assistant_template = cv2.imread(ASSISTANT_IMAGE_PATH, 0)
        auto_template = cv2.imread(AUTO_IMAGE_PATH, 0)

        if attack_template is None or assistant_template is None or auto_template is None:
            raise ValueError("无法读取图像文件，请检查文件路径和文件是否存在。")
        return attack_template, assistant_template, auto_template
    except Exception as e:
        print(f"图像加载错误: {e}")
        exit(1)

def capture_screen_adb():
    try:
        os.system('adb exec-out screencap -p > screenshot.png')
        time.sleep(WAIT_INTERVAL * 10)
    except Exception as e:
        print(f"截图失败: {e}")

def is_image_on_screen(template):
    try:
        w, h = template.shape[::-1]
        capture_screen_adb()
        screenshot = cv2.imread('screenshot.png', 0)
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(res >= threshold)
        points = [(pt[0] + w // 2, pt[1] + h // 2) for pt in zip(*loc[::-1]) if res[pt[1], pt[0]] >= threshold]
        return points
    except Exception as e:
        print(f"图像检测错误: {e}")
        return []

def perform_click(x, y, interval=WAIT_INTERVAL, times=1, use_adb=False):
    for _ in range(times):
        if use_adb:
            os.system(f'adb shell input tap {x} {y}')
        else:
            pyautogui.click(x, y)
        time.sleep(interval / 2)

def handle_click_with_fault_tolerance(template, positions, click_times=1, auto_template=None):
    max_attempts = 2
    for pos in positions:
        center_x, center_y = pos
        attempt = 0
        while attempt < max_attempts:
            perform_click(center_x, center_y, times=click_times)
            if not is_image_on_screen(template):
                auto_positions = is_image_on_screen(auto_template)
                if auto_positions:
                    print("操作后，自动图标已打开。")
                else:
                    print("操作后，自动图标仍未打开。")
                break
            else:
                if attempt == 0:
                    perform_click(center_x, center_y, times=click_times * 2, use_adb=True)
                attempt += 1
        if attempt == max_attempts:
            print("达到最大尝试次数，操作仍然无效。")
        break

if __name__ == "__main__":
    attack_template, assistant_template, auto_template = load_images()
    screen_width, screen_height = pyautogui.size()

    while True:
        auto_positions = is_image_on_screen(auto_template)
        if auto_positions:
            print("自动图标已打开，一切正常...")
        else:
            print("自动图标未打开，尝试恢复...")
            attack_positions = is_image_on_screen(attack_template)
            assistant_positions = is_image_on_screen(assistant_template)

            if not attack_positions:
                print("未检测到攻击图标，点击屏幕中间。")
                perform_click(screen_width // 2, screen_height // 2)
            elif attack_positions and not assistant_positions:
                print("检测到攻击图标，但未检测到助手图标，点击攻击图标后点击助手图标。")
                # 点击攻击图标
                handle_click_with_fault_tolerance(attack_template, attack_positions, auto_template=auto_template)
                # 接着点击助手图标
                handle_click_with_fault_tolerance(assistant_template, assistant_positions, auto_template=auto_template)
            elif attack_positions and assistant_positions:
                print("检测到助手图标，点击助手图标。")
                handle_click_with_fault_tolerance(assistant_template, assistant_positions, auto_template=auto_template)

        time.sleep(WAIT_INTERVAL * 30)