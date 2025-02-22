import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def count_ht_node(data, target="ht.Node"):
    count = 0
    
    def search(obj):
        nonlocal count
        if isinstance(obj, dict):
            for key, value in obj.items():
                search(key)
                search(value)
        elif isinstance(obj, list):
            for item in obj:
                search(item)
        elif isinstance(obj, str) and obj == target:
            count += 1
            
    search(data)
    return count

def load_and_analyze_json(target_string):
    # 初始化Tkinter
    root = Tk()
    # 不显示主窗口
    root.withdraw()

    # 打开文件选择对话框，允许用户选择一个JSON文件
    file_path = askopenfilename(
        title="选择JSON文件",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )

    if not file_path:
        print("未选择任何文件")
        return
    
    # 读取并解析所选的JSON文件
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("文件不是有效的JSON格式")
            return

    # 数据分析逻辑：统计出现目标字符串的次数
    occurrences = count_ht_node(data, target_string)
    print(f"成功加载文件: {file_path}")
    print(f"字符串 \"{target_string}\" 在JSON文件中出现了 {occurrences} 次.")

# 调用函数并处理返回的数据
load_and_analyze_json("ht.Node")