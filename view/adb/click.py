import subprocess
import time

# 定义一个函数来执行 adb 命令，并添加重试机制
def adb_command(command, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"执行命令失败 (第 {retries + 1} 次尝试): {result.stderr.strip()}")
        except Exception as e:
            print(f"发生错误 (第 {retries + 1} 次尝试): {e}")
        retries += 1
        time.sleep(1)  # 每次重试前等待 1 秒
    print(f"多次尝试后，命令 '{command}' 仍然执行失败。")
    return None

# 检查 ADB 是否连接到模拟器
def check_adb_connection():
    output = adb_command("adb devices")
    if output and "device" in output and "emulator" in output:
        print("ADB 已成功连接到模拟器。")
        return True
    else:
        print("ADB 未连接到模拟器，请检查连接。")
        return False

# 模拟点击屏幕的指定坐标 (x, y)
def tap(x, y):
    adb_command(f"adb shell input tap {x} {y}")

# 模拟滑动屏幕，从 (x1, y1) 滑动到 (x2, y2)，持续时间为 duration 毫秒
def swipe(x1, y1, x2, y2, duration=300):
    adb_command(f"adb shell input swipe {x1} {y1} {x2} {y2} {duration}")

# 示例：模拟点击屏幕坐标
if __name__ == "__main__":
    if check_adb_connection():
        print("程序准备5秒后执行")
        # 等待 5 秒，确保模拟器准备好
        time.sleep(5)
        print("开始点击")
        # tap_coordinates = [(804, 429), (804, 429), (303, 503), (307, 507)]
        tap_coordinates = [(814, 429), (814, 429), (306, 503), (310, 507), (752, 365), (699, 494)]
        for x, y in tap_coordinates:
            tap(x, y)
            time.sleep(2)
        print("点击操作完成。")
    else:
        print("由于 ADB 未连接，程序无法继续执行。")