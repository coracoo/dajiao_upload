import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import requests
import json
import re

def select_folder():
    folder = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder)
    get_folder_info()

def select_file():
    file = filedialog.askopenfilename()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, os.path.dirname(file))
    get_folder_info()

def get_folder_info():
    folder = folder_entry.get()
    if folder:
        # 获取文件夹名称并保存到数组
        folder_name = os.path.basename(folder)

        # 提取中文标题
        cn_title = re.findall(r'^(.*?[\u4E00-\u9FA5]+)\.', folder_name)
        cn_title = cn_title[0] if cn_title else ''

        # 提取英文标题和剩余的内容
        en_title = re.findall(r'[\u4E00-\u9FA5]+\.(.*?)\.S\d', folder_name)
        en_title = en_title[0].replace('.', ' ') if en_title else ''
        remaining = folder_name.replace(cn_title, '').replace(en_title, '').strip('.').replace('.', ' ')

        print("主标题:", remaining)
        print("副标题:", cn_title)

        # 在主标题和副标题输入框中显示标题
        title_entry.delete(0, tk.END)
        title_entry.insert(0, remaining)
        subtitle_entry.delete(0, tk.END)
        subtitle_entry.insert(0, cn_title)

def get_media_info():
    media_id = id_entry.get()
    if media_id:
        # 使用PTGEN接口获取媒体信息
        url = "https://api.iyuu.cn/index.php?s=App.Movie.Ptgen&url={}".format(media_id)
        response = requests.get(url)
        if response.status_code == 200:
            media_info = json.loads(response.text)
            print(media_info)  # 打印媒体信息，以查看完整的JSON响应
            description_text.delete(1.0, tk.END)
            # 插入媒体描述信息到内容简介文本框
            description_text.insert(tk.END, media_info.get('data', {}).get('format', ''))
            
            # 将媒体信息保存到info.json文件
            with open('info.json', 'w') as f:
                json.dump(media_info, f)
        else:
            print("无法获取媒体信息！")

def create_torrent():
    folder = folder_entry.get()
    folder_name = os.path.basename(folder)
    if folder:
        # 使用mktorrent制作同名种子
        subprocess.run(['mktorrent', '-v', '-p', '-l', '19', '-a', 'https://dajiao.cyou/announce.php', folder, '-o', folder_name + '.torrent'])
        print('种子创建完成！')

def upload_torrent():
    # 调用upload.py并传递info.json文件路径
    subprocess.run(['python', 'upload.py', 'info.json'])
    print('种子发布完成！')

# 创建主窗口
root = tk.Tk()
root.title("PT种子发布工具")

# ID输入
id_label = tk.Label(root, text="豆瓣ID或IMDB ID：")
id_label.pack()
id_entry = tk.Entry(root, width=50)
id_entry.pack()

# 获取媒体信息按钮
info_button = tk.Button(root, text="获取媒体信息", command=get_media_info)
info_button.pack()

# 资源目录选择
folder_label = tk.Label(root, text="资源目录：")
folder_label.pack()
folder_entry = tk.Entry(root, width=50)
folder_entry.pack()

# 选择文件夹按钮
folder_button = tk.Button(root, text="选择文件夹", command=select_folder)
folder_button.pack()

# 选择文件按钮
file_button = tk.Button(root, text="选择文件", command=select_file)
file_button.pack()

# 主标题
title_label = tk.Label(root, text="主标题：")
title_label.pack()
title_entry = tk.Entry(root, width=50)
title_entry.pack()

# 副标题
subtitle_label = tk.Label(root, text="副标题：")
subtitle_label.pack()
subtitle_entry = tk.Entry(root, width=50)
subtitle_entry.pack()

# 内容简介
description_label = tk.Label(root, text="内容简介：")
description_label.pack()
description_text = tk.Text(root, width=50, height=10)
description_text.pack()

# 创建种子按钮
create_button = tk.Button(root, text="创建种子", command=create_torrent)
create_button.pack()

# 发布种子按钮
upload_button = tk.Button(root, text="发布种子", command=upload_torrent)
upload_button.pack()

# 运行主循环
root.mainloop()
