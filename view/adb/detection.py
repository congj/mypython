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

# 统一的等待时间间隔
WAIT_INTERVAL = 0.25

# 缓存图像
try:
    attack_template = cv2.imread(attack_image_path, 0)
    assistant_template = cv2.imread(assistant_image_path, 0)
    auto_template = cv2.imread(auto_image_path, 0)
    if attack_template is None or assistant_template is None or auto_template is None:
        raise ValueError("无法读取图像文件")
except Exception as e:
    print(f"图像加载错误: {e}")
    exit(1)

def capture_screen_adb():
    """
    使用ADB捕获设备屏幕截图并保存为screenshot.png。
    """
    try:
        os.system('adb exec-out screencap -p > screenshot.png')
        time.sleep(WAIT_INTERVAL * 4)  # 增加等待时间以确保截图完成
    except Exception as e:
        print(f"截图失败: {e}")

def is_image_on_screen(template):
    """
    该函数用于检查指定的图像是否存在于当前屏幕上，并返回其位置。
    :param template: 待检查的图像模板
    :return: 如果找到匹配项，则返回位置列表；否则返回空列表。
    """
    try:
        w, h = template.shape[::-1]
        # 使用ADB获取屏幕截图
        capture_screen_adb()
        screenshot = cv2.imread('screenshot.png', 0)
        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        points = [(pt[0] + w//2, pt[1] + h//2) for pt in zip(*loc[::-1]) if res[pt[1], pt[0]] >= threshold]  # 直接计算中心点
        return points
    except Exception as e:
        print(f"图像检测错误: {e}")
        return []

def perform_click(x, y, interval=WAIT_INTERVAL, times=1, use_adb=False):
    """
    在给定坐标上执行多次点击操作，并在每次点击后等待一段时间。
    :param x: 点击的x坐标
    :param y: 点击的y坐标
    :param interval: 点击之间的间隔时间（秒）
    :param times: 点击次数
    :param use_adb: 是否使用ADB命令点击
    """
    for _ in range(times):
        if use_adb:
            print(f"准备使用ADB命令点击坐标: ({x}, {y})")
            try:
                os.system(f'adb shell input tap {x} {y}')
            except Exception as e:
                print(f"ADB点击失败: {e}")
        else:
            print(f"准备使用pyautogui点击坐标: ({x}, {y})")
            pyautogui.click(x, y)
        time.sleep(interval)  # 给系统一点时间反映点击结果

def handle_click_with_fault_tolerance(template, positions, click_times=5):
    """
    处理点击操作并添加容错机制
    :param template: 图像模板
    :param positions: 图像位置列表
    :param click_times: 初始点击次数
    """
    max_attempts = 3  # 最大尝试次数
    attempt = 0
    for pos in positions:
        center_x, center_y = pos
        while attempt < max_attempts:
            perform_click(center_x, center_y, times=click_times)
            # 点击后检查图片是否仍然存在
            if not is_image_on_screen(template):
                print(f"点击成功，图片已消失。")
                break
            else:
                print(f"第 {attempt + 1} 次点击无效，尝试增加点击次数或使用ADB点击。")
                if attempt == 1:  # 第二次尝试使用ADB点击
                    perform_click(center_x, center_y, times=click_times * 2, use_adb=True)
                elif attempt == 2:  # 第三次尝试增加ADB点击次数
                    perform_click(center_x, center_y, times=click_times * 3, use_adb=True)
                attempt += 1
        if attempt == max_attempts:
            print("达到最大尝试次数，点击仍然无效。")
        break  # 假设只需要点击一个匹配项

if __name__ == "__main__":
    screen_width, screen_height = pyautogui.size()  # 获取屏幕分辨率
    print(f"屏幕分辨率为: {screen_width}x{screen_height}")

    while True:
        print("开始新一轮的屏幕检测...")
        if is_image_on_screen(auto_template):
            print("检测到自动图标，本次不执行任何操作，等待下一次检测。")
            time.sleep(WAIT_INTERVAL)
            continue

        attack_positions = is_image_on_screen(attack_template)
        assistant_positions = is_image_on_screen(assistant_template)

        if not attack_positions:
            print("未检测到攻击图标，点击屏幕中间。")
            perform_click(screen_width // 2, screen_height // 2)
        elif attack_positions and not assistant_positions:
            print("检测到攻击图标，但未检测到助手图标，点击攻击图标。")
            handle_click_with_fault_tolerance(attack_template, attack_positions)
        elif attack_positions and assistant_positions:
            print("检测到攻击图标和助手图标，先点击攻击图标，再点击助手图标。")
            handle_click_with_fault_tolerance(attack_template, attack_positions)
            handle_click_with_fault_tolerance(assistant_template, assistant_positions)
        elif not attack_positions and assistant_positions:
            print("未检测到攻击图标，但检测到助手图标，点击助手图标。")
            handle_click_with_fault_tolerance(assistant_template, assistant_positions)

        print("本次检测结束，等待 0.25 秒后进行下一次检测。")
        time.sleep(WAIT_INTERVAL)