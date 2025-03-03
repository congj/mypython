import subprocess
import cv2
import numpy as np
import os

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
        img = cv2.imread(image_path)
        if img is not None:
            return True
        return False
    except Exception:
        return False


def detect_circles(image_path):
    """
    对截图进行圆形检测
    """
    # 检查图像文件是否有效
    if not os.path.exists(image_path) or not is_valid_image(image_path):
        print(f"图像文件 {image_path} 无效或不存在，无法进行圆形检测。")
        return 0

    print(f"开始对图像 {image_path} 进行圆形检测...")
    # 读取图像
    image = cv2.imread(image_path)
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 高斯模糊
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # 使用霍夫圆变换检测圆形
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1,
                               minDist=20,
                               param1=50,
                               param2=30,
                               minRadius=10,
                               maxRadius=50)

    circle_count = 0
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            circle_count += 1
            # 打印圆形的信息
            print(f"第 {circle_count} 个圆形 - 圆心坐标: ({x}, {y}), 半径: {r}")
            # 在原始图像上绘制圆形
            cv2.circle(image, (x, y), r, (0, 255, 0), 2)
            # 绘制圆心
            cv2.rectangle(image, (x - 2, y - 2), (x + 2, y + 2), (0, 128, 255), -1)

        print(f"共检测到 {circle_count} 个圆形。")
    else:
        print("未检测到圆形。")

    # 显示带有圆形标记的图像
    cv2.imshow('Circle Detection Result', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return circle_count


if __name__ == "__main__":
    # 捕获屏幕截图
    screenshot_path = capture_screenshot()
    if screenshot_path:
        # 进行圆形检测
        circle_count = detect_circles(screenshot_path)
        print(f"最终检测到的圆形数量: {circle_count}")



