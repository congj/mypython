import os
from tkinter import filedialog, messagebox, ttk
import tkinter as tk
import uuid
from datetime import datetime

def rename_files(folder_path, file_extension, new_file_extension=None, prefix='', suffix='', use_timestamp=False, use_uuid=False):
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(file_extension):
                base_filename = os.path.splitext(filename)[0]
                if use_timestamp:
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    new_name = f"{timestamp}{suffix}"
                elif use_uuid:
                    new_name = f"{uuid.uuid4()}{suffix}"
                else:
                    new_name = f"{prefix}{base_filename}{suffix}"
                
                old_file = os.path.join(folder_path, filename)
                # 如果提供了新的文件后缀，则使用新后缀，否则保留原后缀
                used_file_extension = new_file_extension if new_file_extension else file_extension
                new_file = os.path.join(folder_path, new_name + used_file_extension)

                # Check if the new file already exists
                if os.path.exists(new_file):
                    messagebox.showwarning("警告", f"文件 {new_name} 已经存在，跳过该文件。")
                    continue
                
                os.rename(old_file, new_file)
        return True
    except Exception as e:
        messagebox.showerror("错误", f"重命名文件时出错: {str(e)}")
        return False

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory(title="选择文件夹")
    return folder_selected

def main():
    def on_submit():
        folder_path = folder_var.get()
        file_extension = extension_var.get()
        new_file_extension = new_extension_var.get()
        add_to_front = prefix_entry.get()
        add_to_end = suffix_entry.get()
        use_timestamp = timestamp_var.get()
        use_uuid = uuid_var.get()

        if not folder_path:
            messagebox.showwarning("警告", "请选择文件夹")
            return

        if not file_extension.startswith('.'):
            file_extension = '.' + file_extension

        if new_file_extension and not new_file_extension.startswith('.'):
            new_file_extension = '.' + new_file_extension

        success = rename_files(folder_path, file_extension, new_file_extension, prefix=add_to_front, suffix=add_to_end, use_timestamp=use_timestamp, use_uuid=use_uuid)
        if success:
            messagebox.showinfo("完成", f"文件夹 {folder_path} 中的文件已重命名")

    def on_exit():
        root.destroy()

    root = tk.Tk()
    root.title("批量修改文件名")

    folder_button = tk.Button(root, text="选择文件夹", command=lambda: folder_var.set(select_folder()))
    folder_button.grid(row=0, column=0, padx=10, pady=10)

    folder_var = tk.StringVar()
    folder_label = tk.Label(root, textvariable=folder_var, wraplength=300)
    folder_label.grid(row=0, column=1, padx=10, pady=10)

    extension_label = tk.Label(root, text="文件后缀:")
    extension_label.grid(row=1, column=0, padx=10, pady=10)

    common_extensions = ['.txt', '.jpg', '.png', '.pdf', '.docx', '.xlsx']
    extension_var = tk.StringVar(value=common_extensions[0])
    extension_combobox = ttk.Combobox(root, textvariable=extension_var, values=common_extensions)
    extension_combobox.grid(row=1, column=1, padx=10, pady=10)

    new_extension_label = tk.Label(root, text="新文件后缀(可选):")
    new_extension_label.grid(row=2, column=0, padx=10, pady=10)
    new_extension_var = tk.StringVar()
    new_extension_entry = tk.Entry(root, textvariable=new_extension_var)
    new_extension_entry.grid(row=2, column=1, padx=10, pady=10)

    prefix_label = tk.Label(root, text="前缀:")
    prefix_label.grid(row=3, column=0, padx=10, pady=10)
    prefix_entry = tk.Entry(root)
    prefix_entry.grid(row=3, column=1, padx=10, pady=10)

    suffix_label = tk.Label(root, text="后缀:")
    suffix_label.grid(row=4, column=0, padx=10, pady=10)
    suffix_entry = tk.Entry(root)
    suffix_entry.grid(row=4, column=1, padx=10, pady=10)

    submit_button = tk.Button(root, text="提交", command=on_submit)
    submit_button.grid(row=5, columnspan=2, pady=10)

    exit_button = tk.Button(root, text="退出", command=on_exit)
    exit_button.grid(row=6, columnspan=2, pady=10)

    timestamp_var = tk.BooleanVar(value=False)  # 新增变量用于跟踪是否使用时间戳
    timestamp_button = tk.Checkbutton(root, text="使用时间戳重命名(忽略前缀)", variable=timestamp_var)
    timestamp_button.grid(row=7, columnspan=2, pady=10)

    uuid_var = tk.BooleanVar(value=False)  # 新增变量用于跟踪是否使用UUID
    uuid_button = tk.Checkbutton(root, text="使用UUID重命名(忽略前缀)", variable=uuid_var)
    uuid_button.grid(row=8, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()