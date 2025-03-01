import subprocess
import xml.etree.ElementTree as ET


def get_text_at_click(x, y):
    try:
        # 执行 ADB 命令获取界面布局信息
        result = subprocess.run('adb shell uiautomator dump /sdcard/window_dump.xml', shell=True, capture_output=True,
                                text=True)
        if result.returncode != 0:
            print("获取界面布局信息失败:", result.stderr)
            return None

        # 将 XML 文件从模拟器复制到本地
        pull_result = subprocess.run('adb pull /sdcard/window_dump.xml', shell=True, capture_output=True, text=True)
        if pull_result.returncode != 0:
            print("拉取 XML 文件失败:", pull_result.stderr)
            return None

        # 解析 XML 文件
        tree = ET.parse('window_dump.xml')
        root = tree.getroot()

        # 遍历 XML 中的所有元素
        for element in root.findall('.//node'):
            bounds = element.get('bounds')
            if bounds:
                # 解析元素的边界信息
                left, top, right, bottom = map(int, bounds.strip('[]').replace('][', ',').split(','))
                # 检查点击坐标是否在元素的边界内
                if left <= x <= right and top <= y <= bottom:
                    text = element.get('text')
                    if text:
                        return text
        return "未找到点击处的文字。"
    except Exception as e:
        print("解析 XML 文件时出错:", e)
        return None


# 示例点击坐标
click_x = 100
click_y = 200
text = get_text_at_click(click_x, click_y)
print("点击处的文字为:", text)