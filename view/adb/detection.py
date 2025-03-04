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
    """
    加载图像模板，若加载失败则输出错误信息并终止程序。
    :return: 攻击图标、助手图标、自动图标的图像模板
    """
    try:
        attack_template = cv2.imread(ATTACK_IMAGE_PATH, 0)
        assistant_template = cv2.imread(ASSISTANT_IMAGE_PATH, 0)
        auto_template = cv2.imread(AUTO_IMAGE_PATH, 0)

        # 检查图像是否成功加载
        if attack_template is None or assistant_template is None or auto_template is None:
            raise ValueError("无法读取图像文件，请检查文件路径和文件是否存在。")
        return attack_template, assistant_template, auto_template
    except Exception as e:
        print(f"图像加载错误: {e}")
        exit(1)

def capture_screen_adb():
    """
    使用ADB命令捕获设备屏幕截图，并保存为screenshot.png。
    为确保截图完成，添加了短暂的等待时间。
    """
    try:
        os.system('adb exec-out screencap -p > screenshot.png')
        # 增加等待时间以确保截图完成
        time.sleep(WAIT_INTERVAL * 10)
    except Exception as e:
        print(f"截图失败: {e}")

def is_image_on_screen(template):
    """
    检查指定的图像模板是否存在于当前屏幕截图中。
    :param template: 待检查的图像模板
    :return: 若找到匹配项，返回匹配位置的中心点列表；否则返回空列表
    """
    try:
        # 获取模板的宽度和高度
        w, h = template.shape[::-1]
        # 每次都重新截图以获取最新屏幕状态
        capture_screen_adb()
        # 读取屏幕截图
        screenshot = cv2.imread('screenshot.png', 0)
        # 使用模板匹配方法查找匹配位置
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        # 设定匹配阈值
        threshold = 0.7
        # 找出匹配度大于等于阈值的位置
        loc = np.where(res >= threshold)
        # 计算匹配位置的中心点坐标
        points = [(pt[0] + w // 2, pt[1] + h // 2) for pt in zip(*loc[::-1]) if res[pt[1], pt[0]] >= threshold]
        return points
    except Exception as e:
        print(f"图像检测错误: {e}")
        return []

def perform_click(x, y, interval=WAIT_INTERVAL, times=1, use_adb=False):
    """
    在指定坐标上执行多次点击操作，并在每次点击后等待一段时间。
    :param x: 点击的x坐标
    :param y: 点击的y坐标
    :param interval: 点击之间的间隔时间（秒）
    :param times: 点击次数
    :param use_adb: 是否使用ADB命令进行点击
    """
    for _ in range(times):
        if use_adb:
            os.system(f'adb shell input tap {x} {y}')
        else:
            pyautogui.click(x, y)
        # 每次点击后等待一段时间
        time.sleep(interval / 2)

def handle_click_with_fault_tolerance(template, positions, click_times=1, is_attack=False, is_assistant=False, auto_template=None):
    """
    处理点击操作，并具备容错机制。
    若点击后图像仍存在，则尝试增加点击次数或使用ADB点击。
    :param template: 待点击图标的图像模板
    :param positions: 图标匹配位置的中心点列表
    :param click_times: 初始点击次数
    :param is_attack: 是否为攻击图标
    :param is_assistant: 是否为助手图标
    :param auto_template: 自动图标的图像模板
    """
    max_attempts = 2  # 最大尝试次数
    for pos in positions:
        center_x, center_y = pos
        attempt = 0
        while attempt < max_attempts:
            if is_assistant:
                pyautogui.press('u')
            else:
                perform_click(center_x, center_y, times=click_times)
            # 点击后检查图片是否仍然存在
            if not is_image_on_screen(template):
                if is_attack:
                    pyautogui.press('u')
                # 检查自动图标是否存在
                auto_positions = is_image_on_screen(auto_template)
                if auto_positions:
                    print("操作后，自动图标已打开。")
                else:
                    print("操作后，自动图标仍未打开。")
                break
            else:
                if attempt == 0 and not is_assistant:  # 第一次尝试失败，第二次使用ADB点击（助手图标不适用）
                    perform_click(center_x, center_y, times=click_times * 2, use_adb=True)
                attempt += 1
        if attempt == max_attempts:
            print("达到最大尝试次数，操作仍然无效。")
        # 假设只需要处理一个匹配项，处理完一个位置后跳出循环
        break

if __name__ == "__main__":
    # 加载图像模板
    attack_template, assistant_template, auto_template = load_images()
    # 获取屏幕分辨率
    screen_width, screen_height = pyautogui.size()

    while True:
        # 检查自动图标是否存在
        auto_positions = is_image_on_screen(auto_template)
        if auto_positions:
            print("自动图标已打开，持续监测...")
        else:
            print("自动图标未打开，尝试恢复...")
            # 检查攻击图标和助手图标是否存在
            attack_positions = is_image_on_screen(attack_template)
            assistant_positions = is_image_on_screen(assistant_template)

            if not attack_positions:
                print("未检测到攻击图标，点击屏幕中间。")
                perform_click(screen_width // 2, screen_height // 2)
            elif attack_positions and not assistant_positions:
                print("检测到攻击图标，但未检测到助手图标，点击攻击图标。")
                handle_click_with_fault_tolerance(attack_template, attack_positions, is_attack=True, auto_template=auto_template)
            elif attack_positions and assistant_positions:
                print("检测到助手图标，按下U键。")
                handle_click_with_fault_tolerance(assistant_template, assistant_positions, is_assistant=True, auto_template=auto_template)

        # 每次检测结束后等待一段时间，再进行下一次检测
        time.sleep(WAIT_INTERVAL * 30)