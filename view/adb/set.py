import cv2
import numpy as np
import os
import subprocess
import random
import time

def list_files_in_directory(directory_path):
    """列出给定目录下的所有文件名称，并返回一个列表"""
    try:
        return [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if filename.lower().endswith(('.png', '.jpg', '.jpeg'))]
    except Exception as e:
        print(f"无法读取目录 {directory_path}: {e}")
        return []

def get_emulator_resolution():
    try:
        # 执行 ADB 命令获取屏幕分辨率
        result = subprocess.run('adb shell wm size', shell=True, capture_output=True, text=True)
        output = result.stdout.strip()
        if 'Physical size:' in output:
            size_str = output.split('Physical size: ')[1]
            width, height = map(int, size_str.split('x'))
            return width, height
        else:
            print("无法获取模拟器分辨率，请检查 ADB 连接。")
            return None, None
    except Exception as e:
        print(f"获取分辨率时出错: {e}")
        return None, None

def find_button_locations(screenshot_path, button_paths):
    # 获取模拟器分辨率
    width, height = get_emulator_resolution()
    if width is None or height is None:
        return

    # 读取屏幕截图
    screenshot = cv2.imread(screenshot_path)
    if screenshot is None:
        print(f"无法读取屏幕截图: {screenshot_path}")
        return

    # 存储所有按钮的坐标和对应的图片名称
    all_locations = []
    for index, button_path in enumerate(button_paths):
        # 获取按钮图片文件名
        button_filename = os.path.basename(button_path)

        # 读取按钮图像
        button = cv2.imread(button_path)
        if button is None:
            print(f"无法读取按钮图像: {button_path}")
            continue

        # 获取按钮图像的高度和宽度
        h, w = button.shape[:2]

        # 使用模板匹配方法查找按钮位置
        result = cv2.matchTemplate(screenshot, button, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 获取按钮的左上角和右下角坐标
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # 计算按钮的中心坐标
        center_x = (top_left[0] + bottom_right[0]) // 2
        center_y = (top_left[1] + bottom_right[1]) // 2

        # 计算相对于分辨率的坐标比例
        ratio_x = center_x / screenshot.shape[1]
        ratio_y = center_y / screenshot.shape[0]

        # 根据模拟器分辨率计算实际坐标
        actual_x = int(ratio_x * width)
        actual_y = int(ratio_y * height)

        # 存储坐标和图片名称
        all_locations.append((actual_x, actual_y, button_filename))

    # 如果有找到按钮位置
    if all_locations:
        # 50% 概率选择 bt_attack.png
        if random.random() < 0.2:
            attack_locations = [loc for loc in all_locations if loc[2] == 'bt_attack.png']
            if attack_locations:
                random_x, random_y, random_filename = random.choice(attack_locations)
            else:
                random_x, random_y, random_filename = random.choice(all_locations)
        else:
            random_x, random_y, random_filename = random.choice(all_locations)

        # 生成随机等待时间（1 - 5 秒）
        wait_time = random.uniform(1, 5)
        time.sleep(wait_time)

        # 判断是否为需要长按的图片
        long_press_images = ['bt_a.png', 'bt_w.png', 'bt_s.png', 'bt_d.png', 'bt_r.png']
        if random_filename in long_press_images:
            # 持续按住 3 秒
            press_duration = 3000  # 3 秒，单位为毫秒
            adb_command = f'adb shell input swipe {random_x} {random_y} {random_x} {random_y} {press_duration}'
            action = "长按"
        else:
            # 普通点击
            adb_command = f'adb shell input tap {random_x} {random_y}'
            action = "点击"

        try:
            subprocess.run(adb_command, shell=True, check=True)
            print(f"{action} 了图片 {random_filename}，坐标为 ({random_x}, {random_y})")
        except subprocess.CalledProcessError as e:
            print(f"执行 ADB 命令时出错: {e}")
    else:
        print("未找到任何按钮位置。")

if __name__ == "__main__":
    # 打印当前工作目录
    current_directory = os.getcwd()
    # print(f"当前工作目录是: {current_directory}")

    # 新增：列出指定目录下的所有文件，并将结果保存到一个变量
    directory_to_list = "D:/mypython/view/adb/images"
    # print(f"目录 {directory_to_list} 下的所有文件:")
    files_in_directory = list_files_in_directory(directory_to_list)

    # 示例：使用相对路径
    screenshot_path = 'screen/screenshot.png'
    button_paths = []

    # 将新获取的文件列表添加到 button_paths 中
    button_paths.extend(files_in_directory)

    # 先尝试点击 bt_attack.png
    attack_button_paths = [path for path in button_paths if os.path.basename(path) == 'bt_attack.png']
    if attack_button_paths:
        find_button_locations(screenshot_path, attack_button_paths)
    else:
        print("未找到 bt_attack.png 图片。")

    # 循环执行 99 次
    for _ in range(99):
        find_button_locations(screenshot_path, button_paths)