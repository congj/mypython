import tkinter as tk
from tkinter import messagebox
import subprocess

def run_script(script_name):
    try:
        # 使用subprocess运行指定的Python脚本
        result = subprocess.run(['python', script_name], capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("成功", f"{script_name} 执行成功")
        else:
            messagebox.showerror("错误", f"执行 {script_name} 时发生错误: {result.stderr}")
    except Exception as e:
        messagebox.showerror("错误", f"无法执行 {script_name}: {str(e)}")

# 创建主窗口
root = tk.Tk()
root.title("功能选择界面")
root.geometry('320x240')  # 设置初始窗口大小
root.resizable(True, True)  # 允许手动调节窗口大小

# 定义脚本名称
scripts = ['analysisjson.py', 'rename.py', 'getsize.py']

# 自定义按钮样式
button_style = {'bg': '#4CAF50', 'fg': 'white', 'width': 25, 'height': 2, 'font': ('Helvetica', 10)}

# 动态创建按钮，每个按钮对应一个脚本
for script in scripts:
    btn = tk.Button(root, text=script, command=lambda s=script: run_script(s), **button_style)
    btn.pack(expand=True, pady=5)

# 添加一些空白占位，使界面看起来更加均衡
tk.Label(root, height=1).pack()

# 进入消息循环
root.mainloop()