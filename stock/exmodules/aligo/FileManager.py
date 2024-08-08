import hashlib

from aligo import Aligo

if __name__ == '__main__':
    ali = Aligo()  # 第一次使用，会弹出二维码，供扫描登录

    user = ali.get_user()  # 获取用户信息
    print(user.user_name, user.nick_name, user.phone)  # 打印用户信息
    parent_file_id = "66b1919fb69d53d2ce1a450589da0f106fea7851"

    update_file_id = "66b1bc44779786a1ffa44e4fa1e8e8a47d29d234"
    filePath = "test.csv"

    ali.upload_file(filePath, parent_file_id, "earnings.csv")

    file_list = ali.get_file_list(parent_file_id)  # 获取网盘根目录文件列表
    for file in file_list:  # 遍历文件列表
        # 注意：print(file) 默认只显示部分信息，但是实际上file有很多的属性
        print(file.file_id, file.name, file.type)  # 打印文件信息