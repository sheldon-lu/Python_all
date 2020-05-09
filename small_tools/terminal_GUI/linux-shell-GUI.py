# /usr/bin/python
# -*- coding:utf-8 -*-
# python3环境
# linux终端界面化菜单简单实现
################
# sheldon-lu   #
################

import os
import sys
import json
import time

# 使用linux系统交互输入信息时，
# 会出现backspace无法删除乱码的情况；
# 导入readline模块可以消除这种乱码情况。
# 需要取消注释即可

# import readline


# Menu选择项
xuanze = '''对应编号： 
             1. xx
             2. 2
             3. 3
             4. 4
             5. 5
             h. 显示编号帮助help
             q. quit/退出选项'''


# Use func Class things
class Things():
    def __init__(self, username='none'):
        self.username = username

    # demo test func
    def clean_disk(self):
        print("cleaning disk ... ...")
        time.sleep(1)
        print("clean disk done!")
        
        
    # demo test func
    def clean_disk1(self):
        print("cleaning disk ... ...")
        time.sleep(1)
        print("clean disk done!")
        
    # demo test func
    def clean_disk2(self):
        print("cleaning disk ... ...")
        time.sleep(1)
        print("clean disk done!")
        
    # demo test func
    def clean_disk3(self):
        print("cleaning disk ... ...")
        time.sleep(1)
        print("clean disk done!")
        
        
        
        
# Menu界面化
class Menu():
    def __init__(self):
        self.thing = Things()
        self.choices = {
            "1": self.thing.clean_disk,
            "2": self.thing.clean_disk1,
            "3": self.thing.clean_disk2,
            "4": self.thing.clean_disk3,
            "5": self.thing.clean_disk,
            "q": self.quit
        }

    def display_menu(self):
        # linux命令 clear
        # windows CMD调试请使用 cls
        os.system('clear')
        # os.system('cls')
        # 解码 utf-8 适用于windows调试
        print(xuanze)

    def run(self):
        while True:
            self.display_menu()
            try:
                choice = input("Enter an option >>> ")
            except Exception as e:
                print("Please input a valid option!");
                continue

            choice = str(choice).strip()
            action = self.choices.get(choice)
            if action:
                action()
                stopword = "h"
                print(">>> ", end="")
                for line in iter(input, stopword):  # 输入为"h"，表示输入结束
                    if line == "q":
                        self.quit()
                    print(">>> ",end="")
            else:
                print("{0} is not a valid choice".format(choice))

    def quit(self):
        print("\nThank you for using this script!\n")
        sys.exit(0)


if __name__ == '__main__':
    Menu().run()
