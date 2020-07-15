# -*- coding: UTF-8 -*-
# @LastAuthor: TakanashiKoucha
# @Date: 2020-07-11 20:42:39
import os

from PIL import Image


def openAllFiles():
    global name
    count = 0
    for im in os.listdir(r"."):
        if im.endswith(".jpeg"):
            if name == "":
                name = im
            locals()["im" + str(count)] = Image.open(im)
            try:
                if hasattr(locals()["im" + str(count)], '_getexif'):
                    dict_exif = locals()["im" + str(count)]._getexif()
                if dict_exif[274] == 3:
                    locals()["im" + str(count)] = locals()["im" +
                                                           str(count)].rotate(
                                                               180,
                                                               expand=True)
                elif dict_exif[274] == 6:
                    locals()["im" + str(count)] = locals()["im" +
                                                           str(count)].rotate(
                                                               270,
                                                               expand=True)
                elif dict_exif[274] == 8:
                    locals()["im" + str(count)] = locals()["im" +
                                                           str(count)].rotate(
                                                               90, expand=True)
                else:
                    locals()["im" + str(count)] = locals()["im" + str(count)]
            except:
                pass
            im_list.append(locals()["im" + str(count)])
            count = count + 1


def Merge():
    global image
    w_list = []
    h_list = []
    for i in range(len(im_list)):
        im = im_list[i].convert("RGB")
        w, h = im.size
        im_list[i] = im.resize((w // 2, h // 2))
        w_list.append(w // 2)
        h_list.append(h // 2)
    width = 100
    for w in w_list:
        width = width + w + 700
    height = max(h_list) + 300
    image = Image.new("RGB", (width, height), (255, 255, 255))
    box = [100, 100]
    for im in im_list:
        w, h = im.size
        image.paste(im, (box[0], box[1]))
        box[0] = box[0] + w + 700


def Save():
    global image
    global name
    image.save(name.split(".")[0] + "-副本.jpeg", "jpeg")


def run():
    global im_list
    global name
    im_list = []
    name = ""
    openAllFiles()
    Merge()
    Save()


if __name__ == "__main__":
    input("按回车开始进行，目录比较凌乱的话发生错误是正常的")
    path_list = []
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for name in files:
            path_list.append(root)
        for name in dirs:
            pass
    todo_list = set(path_list)
    for todo in todo_list:
        try:
            os.chdir(todo)
            run()
            print("成功生成1次")
        except:
            print("发生了1次错误")
    input("按回车退出嗷")
