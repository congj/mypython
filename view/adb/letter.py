import uiautomator2 as u2

def get_screen_size():
    try:
        # 连接到安卓设备（模拟器）
        d = u2.connect()
        # 获取屏幕大小
        screen_width, screen_height = d.window_size()
        print(f"模拟器屏幕大小: 宽度 {screen_width} 像素，高度 {screen_height} 像素")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    get_screen_size()