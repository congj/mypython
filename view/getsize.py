import os
import threading
from tkinter import Tk, messagebox, Label, StringVar, Button, Frame, filedialog
from tkinter.ttk import Progressbar, Combobox

def get_sorted_files_by_size(start_path, file_extension, progress_callback):
    files_with_sizes = []
    total_files_count = sum(len(files) for _, _, files in os.walk(start_path))
    processed_files_count = 0
    
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            if file_extension and not f.endswith(file_extension):
                continue
            
            fp = os.path.join(dirpath, f)
            try:
                size = os.path.getsize(fp) / (1024 * 1024)  # 将字节转换为MB
                if size > 1:  # 只有当文件大小大于1MB时，才加入列表
                    files_with_sizes.append((size, fp))
            except OSError as e:
                print(f"无法访问文件 {f} 在 {dirpath}: {e}")
            processed_files_count += 1
            progress_callback(processed_files_count, total_files_count)
                
    sorted_files = sorted(files_with_sizes, key=lambda x: x[0], reverse=True)
    
    return sorted_files

def get_filtered_file_extensions_in_directory(start_path):
    extensions = {}
    for dirpath, dirnames, filenames in os.walk(start_path):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext:  # 忽略没有扩展名的文件
                fp = os.path.join(dirpath, filename)
                try:
                    size = os.path.getsize(fp) / (1024 * 1024)  # 将字节转换为MB
                    if size > 1:  # 只有当文件大小大于1MB时，才考虑该文件
                        extensions[ext] = extensions.get(ext, 0) + 1
                except OSError as e:
                    print(f"无法访问文件 {filename} 在 {dirpath}: {e}")
    
    filtered_extensions = [ext for ext, count in extensions.items() if count > 3]
    return sorted(filtered_extensions)

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_main_menu()
        self.master.geometry('400x200')  # 设置固定窗口大小
        self.master.resizable(False, False)  # 禁止调整窗口大小
        self.master.title("统计大文件")  # 设置窗口标题为"统计大文件"

    def create_main_menu(self):
        self.clear_widgets()
        self.select_path_button = Button(self, text="选择目录并开始", command=self.ask_directory)
        self.select_path_button.pack(side="top", pady=5)

    def ask_directory(self):
        path = filedialog.askdirectory(title="请选择要扫描的目录")
        if not path or not os.path.isdir(path):
            messagebox.showerror("错误", "无效的路径，请检查后重试。")
            return
        
        self.file_extensions = get_filtered_file_extensions_in_directory(path)
        self.file_extensions.insert(0, "")  # 插入空字符串选项表示所有文件
        
        self.clear_widgets()
        self.create_function_selection_widgets(path)

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_function_selection_widgets(self, path):
        self.label = Label(self, text="请选择功能：")
        self.label.pack(pady=5)
        
        self.size_sort_button = Button(self, text="按大小排序文件", command=lambda: self.start_task('size', path))
        self.size_sort_button.pack(pady=5)
        
        self.extension_filter_button = Button(self, text="按后缀筛选文件", command=lambda: self.start_task('extension', path))
        self.extension_filter_button.pack(pady=5)
        
        self.back_button = Button(self, text="返回", command=self.create_main_menu)
        self.back_button.pack(pady=5)

    def start_task(self, task_type, path):
        if task_type == 'size':
            self.perform_size_sort(path)
        elif task_type == 'extension':
            self.perform_extension_filter(path)

    def perform_size_sort(self, path):
        self.clear_widgets()
        self.label = Label(self, text="正在按大小排序文件...")
        self.label.pack(pady=10)
        self.progress = Progressbar(self, orient='horizontal', length=300, mode='determinate')
        self.progress.pack(pady=20)
        
        total_files_count = sum(len(files) for _, _, files in os.walk(path))
        self.progress['maximum'] = total_files_count

        def worker():
            sorted_files = get_sorted_files_by_size(path, None, self.update_progress)
            output_file_path = os.path.join(os.getcwd(), "file_sizes.txt")
            
            if sorted_files:
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    for size, file_path in sorted_files:
                        line = f'{size:.2f} MB: {file_path}\n'
                        f.write(line)
                        print(line.strip())
                print(f"\n文件大小信息已保存到: {output_file_path}")
            else:
                print("所选目录中没有大于1MB的文件，因此输出文件为空。")
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    pass  # 创建或清空文件，不写入内容
            
            self.master.quit()  # 自动退出应用程序

        threading.Thread(target=worker, daemon=True).start()

    def update_progress(self, current, total):
        self.progress['value'] = current
        self.label.config(text=f"已扫描: {current}/{total} 文件")
        self.update_idletasks()

    def perform_extension_filter(self, path):
        self.clear_widgets()
        Label(self, text="请选择文件后缀：").pack(pady=5)
        combo_var = StringVar()
        combobox = Combobox(self, textvariable=combo_var)
        combobox['values'] = self.file_extensions
        combobox.current(0)
        combobox.pack(pady=5)
        
        def proceed():
            selected_extension = combo_var.get()
            self.clear_widgets()
            self.label = Label(self, text="正在筛选文件...")
            self.label.pack(pady=10)
            self.progress = Progressbar(self, orient='horizontal', length=300, mode='determinate')
            self.progress.pack(pady=20)
            
            total_files_count = sum(len(files) for _, _, files in os.walk(path))
            self.progress['maximum'] = total_files_count

            def worker():
                sorted_files = get_sorted_files_by_size(path, selected_extension if selected_extension else None, self.update_progress)
                output_file_path = os.path.join(os.getcwd(), "filtered_files.txt")
                
                if sorted_files:
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        for size, file_path in sorted_files:
                            line = f'{size:.2f} MB: {file_path}\n'
                            f.write(line)
                            print(line.strip())
                    print(f"\n文件大小信息已保存到: {output_file_path}")
                else:
                    print("所选目录中没有大于1MB且符合后缀要求的文件，因此输出文件为空。")
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        pass
                
                self.master.quit()  # 自动退出应用程序

            threading.Thread(target=worker, daemon=True).start()

        Button(self, text="确定", command=proceed).pack(pady=10)

root = Tk()
app = Application(master=root)
app.mainloop()



