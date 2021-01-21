# P02 批量读取文件名（不带后缀）

import os

file_path = "./data"
path_list = os.listdir(file_path)  # os.listdir(file)会历遍文件夹内的文件并返回一个列表
print(path_list)
path_name = []  # 把文件列表写入save.txt中


def saveList(pathName):
    for file_name in pathName:
        with open("./val.txt", "a") as f:
            f.write(file_name.split(".")[0] + "\n")
            # print(file_name.split(".")[0] + "\n")


def dirList(path_list):
    # 将文件路径从列表中获取出来
    for i in range(0, len(path_list)):
        path = os.path.join(file_path, path_list[i])

    if os.path.isdir(path):
        print(path)
        saveList(os.listdir(path))
        # print(os.listdir(path))


if __name__ == '__main__':
    dirList(path_list)
    saveList(path_list)
