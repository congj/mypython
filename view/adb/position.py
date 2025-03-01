import cv2
import numpy as np
import os
import subprocess

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

    # 遍历每个按钮图像文件
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

        # 打印图片名字和位置信息
        print(f"图片 {button_filename} 的位置信息：相对于截图的中心坐标为 ({center_x}, {center_y})，相对于模拟器分辨率的实际中心坐标为 ({actual_x}, {actual_y})")


if __name__ == "__main__":
    # 打印当前工作目录
    current_directory = os.getcwd()
    # print(f"当前工作目录是: {current_directory}")

    # 新增：列出指定目录下的所有文件，并将结果保存到一个变量
    directory_to_list = "D:/mypython/view/adb/images"
    # print(f"目录 {directory_to_list} 下的所有文件:")
    files_in_directory = list_files_in_directory(directory_to_list)

    # 示例：使用相对路径
    screenshot_path = 'images/screenshot.png'
    button_paths = []

    # 将新获取的文件列表添加到 button_paths 中
    button_paths.extend(files_in_directory)

    # 调用函数查找按钮位置
    find_button_locations(screenshot_path, button_paths)