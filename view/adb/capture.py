import subprocess
import cv2
import os

def capture_and_crop_screenshot(left, top, width, height, save_folder):
    try:
        # 执行 ADB 命令截取屏幕截图并保存到模拟器的 /sdcard/screenshot.png
        subprocess.run('adb shell screencap -p /sdcard/screenshot.png', shell=True)
        # 将截图从模拟器复制到本地
        subprocess.run('adb pull /sdcard/screenshot.png', shell=True)
        print("屏幕截图已保存到本地的 screenshot.png 文件中。")

        # 读取截图
        image = cv2.imread('screenshot.png')
        if image is None:
            print("无法读取截图文件。")
            return

        # 计算裁剪区域的边界
        right = left + width
        bottom = top + height

        # 裁剪指定区域的图片
        cropped_image = image[top:bottom, left:right]

        # 确保保存文件夹存在
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # 保存裁剪后的图片到指定文件夹
        cropped_image_path = os.path.join(save_folder, "cropped_screenshot.png")
        cv2.imwrite(cropped_image_path, cropped_image)
        print(f"指定区域的图片已保存到本地的 {cropped_image_path} 文件中。")

    except Exception as e:
        print(f"操作过程中出现错误: {e}")

if __name__ == "__main__":
    # 指定截图区域的左上角坐标和宽高
    left =699
    top = 494
    width = 240
    height = 240

    # 指定保存图片的本地文件夹路径
    save_folder = r"D:\mypython\view\adb\screenshot"  # 请根据实际情况修改

    capture_and_crop_screenshot(left, top, width, height, save_folder)