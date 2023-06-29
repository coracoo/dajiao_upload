import os
import cloudscraper
import json

def upload_torrent(torrent_file, title, subtitle, description, site_url, ck):
    # 创建一个 CloudScraper 实例
    scraper = cloudscraper.create_scraper()

    # 构建上传文件的元组
    file_tup = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent'))

    # 构建请求头信息
    headers = {
        'User-Agent': 'USER_AGENT',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection':'keep-alive',
        'Host':'dajiao.asia',
        'Referer':'https://dajiao.asia/upload.php',
        'Sec-Ch-Ua':'"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
        'Sec-Ch-Ua-Mobile':'?0',
        'Sec-Ch-Ua-Platform':'"Windows"',
        'Sec-Fetch-Dest':'iframe',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-Site':'same-origin',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51',
        'Cookie': ck
        }

    # 构建其它参数信息
    payload = {
            'name': title,
            'small_descr': subtitle,
            'descr': description,
            'type': 415
        }
    
    # 上传种子文件
    # upload_response = scraper.post(site_url, files=[file_tup], headers=headers)
    upload_response = scraper.post(site_url, headers=headers,data=payload, file=file_tup)
    
    if upload_response.status_code == 200:
        # 获取种子的唯一标识符（ID）
        
        # 打印调试信息
        print("请求 URL:", site_url)
        print("请求头信息:", headers)
        print("响应内容:", upload_response.text)
        print("请求参数:", payload)
        print("种子上传成功！",file_tup)
    else:
        print("种子上传失败！")

        

# 获取main.py所在的根目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 设置种子文件路径为当前根目录下的torrent文件
torrent_file = os.path.join(script_dir, '大頭綠衣鬥殭屍.The.Vampire.Returns.S02.1993.1080i.HDTV.H264.AC3-DJTV.torrent')

# 读取main.py生成的信息
with open(os.path.join(script_dir, 'info.json'), 'r') as f:
    info_data = json.load(f)

# 提取标题、副标题和描述信息
title = 1#info_data['remaining']
subtitle = 1#info_data['cn_title']
description = 1#info_data['media_info']

# 设置PT站点的上传URL
site_url = 'https://dajiao.asia/takeupload.php'

# 从ck.txt文件中读取cookies
with open('ck.txt', 'r') as f:
    ck = f.read().strip()

# 调用函数上传和发布种子
upload_torrent(torrent_file, title, subtitle, description, site_url, ck)
