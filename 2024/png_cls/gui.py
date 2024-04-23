import json
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import subprocess

root = tk.Tk()
root.title("AI图片识别与展示")
root.geometry("1000x650")

# 存储已上传图片的元组 (image_label, file_path)
uploaded_images = []
ai_res_list = []

with open(r'./flower.json',encoding='utf-8') as f:
    flower_mapping = json.load(f)
def open_image():
    # 弹出文件对话框让用户选择图片
    file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.jpeg *.gif')])
    messagebox.askyesno(title="确认操作", message="请点击确认～耐心等待识别返回")
    print('file_path:',file_path)
    if file_path:

        py_path = r'/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/yolov5/classify/predict.py'
        print(py_path)
        command = [
            'python',
            '/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/yolov5/classify/predict.py',
            '--weights',
            '/Users/xfliu/PycharmProjects/taobao/2024/Recipe_web/yolov5/runs/train-cls/flower5/weights/best.pt',
            '--img', '224',
            '--source',
            file_path
        ]

        try:
            completed_process = subprocess.run(command, capture_output=True, text=True, check=True)


        except subprocess.CalledProcessError as e:
            print(f"命令执行失败，退出码：{e.returncode}\n标准输出：{e.stdout}\n标准错误：{e.stderr}")
        else:
            # 获取标准输出
            output = eval(completed_process.stdout)
            ai_label = flower_mapping[output[1]]
            acc =output[0]
            ai_res_list.append((ai_label,acc))
            print(f"命令执行成功，标准输出：\n{output}")

            # 获取返回码
            return_code = completed_process.returncode
            print(f"命令执行的返回码：{return_code}")
        add_and_show_uploaded_image(file_path, ai_label,acc)
def add_and_show_uploaded_image(file_path,ai_label,acc):
    # 使用PIL加载图片
    loaded_image = Image.open(file_path)

    # 将图片转换为Tkinter可以使用的格式
    image_tk = ImageTk.PhotoImage(loaded_image)

    # 创建一个Label用于显示图片，并将图片设置为Label的image属性
    image_label = tk.Label(image_display_frame, image=image_tk)
    image_label.image = image_tk  # 保存引用以防止被垃圾回收
    for label in image_display_frame.winfo_children():
        label.pack_forget()  # 隐藏当前显示的图片
    tk.Label(image_display_frame,text='ai识别：{} acc:{}'.format(ai_label,acc),justify=tk.CENTER).pack(fill=tk.BOTH)

    image_label.pack(fill=tk.BOTH, expand=True)  # 显示所选图片
    # image_label.pack()

    # 将图片标签和文件路径添加到已上传图片列表，并在左侧列表框中显示文件名
    uploaded_images.append((image_label, file_path))
    image_listbox.insert(tk.END, os.path.basename(file_path))

    # 如果上传过多图片，自动滚动到最后一个
    image_listbox.see(tk.END)



def select_image_in_list(event):
    # 当用户点击列表框中的项目时，显示对应图片
    try:
        index = image_listbox.index(tk.ACTIVE)
        image_label, _ = uploaded_images[index]


        for label in image_display_frame.winfo_children():
            label.pack_forget()  # 隐藏当前显示的图片
        tk.Label(image_display_frame, text='ai识别：{} acc:{}'.format(ai_res_list[index][0], ai_res_list[index][1]),
                 justify=tk.CENTER).pack(
            fill=tk.BOTH)

        image_label.pack(fill=tk.BOTH, expand=True)  # 显示所选图片
    except IndexError:
        pass

# 左侧图片列表区域
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# 创建滚动列表框
image_listbox = tk.Listbox(left_frame, width=20, height=10)
scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=image_listbox.yview)
image_listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
image_listbox.bind('<<ListboxSelect>>', select_image_in_list)

# 图片展示区域
image_display_frame = tk.Frame(root)
image_display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# # 创建一个Button用于触发文件对话框
# upload_button = tk.Button(root, text="上传图片 AI识别", command=open_image)
# upload_button.pack(padx=300,pady=20, side=tk.BOTTOM, expand=True)

# 创建一个Frame用于放置按钮，让它位于主窗口底部
bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

# 创建上传按钮，并将其放入bottom_frame中
upload_button = tk.Button(bottom_frame, text="上传图片 AI识别", command=open_image)
upload_button.pack(side=tk.LEFT, padx=10)

root.mainloop()