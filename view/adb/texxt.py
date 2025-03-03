import os
import cv2
import numpy as np
import pyautogui
import time

# 定义要检查的图片所在的目录
image_dir = r"D:\mypython\view\adb\clickImage"
# 定义攻击图标的文件路径
attack_image_path = os.path.join(image_dir, "attack.png")
# 定义助手图标的文件路径
assistant_image_path = os.path.join(image_dir, "assistant.png")
# 定义自动图标的文件路径
auto_image_path = os.path.join(image_dir, "auto.png")

def capture_screen_adb():
    """
    使用ADB捕获设备屏幕截图并保存为screenshot.png。
    """
    os.system('adb exec-out screencap -p > screenshot.png')

def is_image_on_screen(image_path):
    """
    该函数用于检查指定的图像是否存在于当前屏幕上，并返回其位置。
    :param image_path: 待检查图像的文件路径
    :return: 如果找到匹配项，则返回位置列表；否则返回空列表。
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
        points = []
        for pt in zip(*loc[::-1]):
            points.append((pt[0], pt[1]))
        return points
    except Exception as e:
        print(f"Error checking image on screen: {e}")
        return []

def click_with_interval(x, y, interval=1):
    """
    在给定坐标上执行点击操作，并在点击后等待一段时间。
    :param x: 点击的x坐标
    :param y: 点击的y坐标
    :param interval: 点击之间的间隔时间（秒）
    """
    pyautogui.click(x, y)
    time.sleep(interval)  # 给系统一点时间反映点击结果

def click_and_retry(x, y, retry_delay=2, max_retries=3, interval=1):
    """
    在给定坐标上执行点击操作，并在必要时重试，每次点击之间有间隔。
    :param x: 点击的x坐标
    :param y: 点击的y坐标
    :param retry_delay: 重试之间的延迟（秒）
    :param max_retries: 最大重试次数
    :param interval: 点击之间的间隔时间（秒）
    """
    retries = 0
    while retries < max_retries:
        click_with_interval(x, y, interval)
        if not is_image_on_screen(attack_image_path):  # 假设我们通过攻击图标的状态来判断点击是否成功
            print("点击成功，检测到状态已更新。")
            break
        else:
            retries += 1
            print(f"点击无效，将在 {retry_delay} 秒后重试 ({retries}/{max_retries})...")
            time.sleep(retry_delay)
    else:
        print("达到最大重试次数，但仍未能确认点击成功。")

if __name__ == "__main__":
    try:
        while True:
            print("开始新一轮的屏幕检测...")
            if is_image_on_screen(auto_image_path):
                print("检测到自动图标，本次不执行任何操作，等待下一次检测。")
                pass
            else:
                attack_exists = len(is_image_on_screen(attack_image_path)) > 0
                assistant_exists = len(is_image_on_screen(assistant_image_path)) > 0

                if not attack_exists:
                    print("未检测到攻击图标，点击坐标 (767, 386)。")
                    click_and_retry(767, 386)
                elif attack_exists and not assistant_exists:
                    print("检测到攻击图标，但未检测到助手图标，点击攻击图标 (767, 386)，然后点击 (767, 386)。")
                    click_and_retry(767, 386)  # 点击攻击图标
                    click_and_retry(767, 386, interval=1)  # 根据需求再次点击
                elif attack_exists and assistant_exists:
                    print("检测到攻击图标和助手图标，点击攻击图标 (767, 386)，然后点击 (289, 484)。")
                    click_and_retry(767, 386)  # 点击攻击图标
                    click_and_retry(289, 484, interval=1)  # 点击助手图标位置

            print("本次检测结束，等待 3 秒后进行下一次检测。")
            time.sleep(3)

    except KeyboardInterrupt:
        print("程序被用户手动终止。")