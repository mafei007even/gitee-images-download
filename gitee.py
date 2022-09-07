import requests
import re
import os


# 修改1️⃣ 【你自己的 cookie，去浏览器控制台复制】
headers = {
    'Cookie': '🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪'.encode('utf-8')
}

session = requests.Session()

# 修改2️⃣ 图床仓库的路径前缀，完整路径类似：https://gitee.com/mafei007/images/raw/master/img/image-195520666.png
gitee_repo_url_prefix = "https://gitee.com/mafei007/images/raw/master/img"

# 修改3️⃣ 要保存的本地文件夹名字
local_images_dir_name = "images"

# 正则表达式
links_pat = gitee_repo_url_prefix + '/(.+?)["|\\)]'


def process_md_file(md_file_path):
    img_file_dir =  os.path.dirname(md_file_path) + "/" + local_images_dir_name
    file_content = get_file_content(md_file_path)
    file_names = re.findall(links_pat, file_content)

    idx = 1
    for file_name in file_names:
        url = gitee_repo_url_prefix + "/" + file_name
        download_img_to_disk(url, img_file_dir, file_name)
        print(idx, "下载完成：", url)
        idx = idx + 1

    # 修改 md 图片路径为本地路径
    new_content = file_content.replace(gitee_repo_url_prefix, local_images_dir_name)
    with open(md_file_path,'w') as f:
        f.write(new_content)
    print("已将「gitee 图片路径」替换为「本地路径」")


def get_file_content(md_file_path):
    with open(md_file_path, 'r') as f:
        return f.read()


def download_img_to_disk(url, img_file_dir, img_file_name):
    path = img_file_dir + "/" + img_file_name
    # 已经存在此文件，跳过
    if os.path.exists(path):
        return

    if not os.path.exists(img_file_dir):
        os.makedirs(img_file_dir)

    resp = session.get(url, headers=headers)
    with open(path, 'wb') as f:
      f.write(resp.content)
    

# 修改4️⃣ 【md 文件路径】
process_md_file("/Users/xxx/Java.md")