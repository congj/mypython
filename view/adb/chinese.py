import subprocess
import cv2
import pytesseract
from PIL import Image
import numpy as np
import os

# 设置 pytesseract 的路径
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_screenshot():
    """
    使用 adb 命令获取模拟器屏幕截图
    """
    try:
        subprocess.run(['adb', 'exec-out', 'screencap', '-p'], stdout=open('screenshot.png', 'wb'))
        print("截图已保存为 screenshot.png")
        return 'screenshot.png'
    except Exception as e:
        print(f"截图失败: {e}")
        return None

def is_valid_image(image_path):
    """
    检查文件是否为有效的图像文件
    """
    try:
        img = Image.open(image_path)
        img.verify()
        return True
    except (IOError, SyntaxError):
        return False

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    # 灰度化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 高斯模糊降噪
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # 自适应阈值二值化
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # 形态学操作：膨胀和腐蚀
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    return eroded

def ocr_with_coordinates(image_path):
    """
    对截图进行 OCR 识别，并提取文字及其坐标
    """
    # 检查图像文件是否有效
    if not os.path.exists(image_path) or not is_valid_image(image_path):
        print(f"图像文件 {image_path} 无效或不存在，无法进行识别。")
        return
    print(f"开始对图像 {image_path} 进行 OCR 识别...")
    # 图像预处理
    preprocessed_image = preprocess_image(image_path)
    # 进行 OCR 识别并获取数据，设置 lang 参数为 'chi_sim'，并调整配置
    config = '--psm 3 --oem 1'
    data = pytesseract.image_to_data(preprocessed_image, output_type=pytesseract.Output.DICT, lang='chi_sim', config=config)

    # 读取原始图像用于绘制矩形框
    original_image = cv2.imread(image_path)
    # 遍历识别结果
    text_count = 0
    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        if text:
            text_count = text_count + 1
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]

            # 打印文字和坐标
            print(f"第 {text_count} 个识别结果 - 文字: {text}, 坐标: ({x}, {y}), 宽度: {w}, 高度: {h}")

            # 在原始图像上绘制矩形框
            cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if text_count == 0:
        print("未识别到有效文字。")
    else:
        print(f"共识别到 {text_count} 个文字区域。")

    # 显示带有矩形框的图像
    cv2.imshow('OCR Result', original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # 捕获屏幕截图
    screenshot_path = capture_screenshot()
    if screenshot_path:
        # 进行 OCR 识别并提取坐标
        ocr_with_coordinates(screenshot_path)