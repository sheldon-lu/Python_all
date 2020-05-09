#!/usr/bin/env python
# -*- coding:utf-8 -*-
## python3 or latest
## 传参用法示例


import requests
import json
import os
import getopt
import sys
# 禁用 InsecureRequestWarning
import urllib3
urllib3.disable_warnings()
#############################

headers = {}
## 本地yaml文件路径，只放yaml文件
yamlfilepath = ""
Namespace = ""


class CommFun():
    def __init__(self):
        pass
    
    # 遍历文件目录，获取路径下所有文件
    def getfilelist(self, filepath):
        fileList = os.listdir(filepath)
        files = []
        for i in range(len(fileList)):
            child = os.path.join('%s/%s' % (filepath, fileList[i]))
            if os.path.isdir(child):
                files.extend(self.getfilelist(child))

            else:
                files.append(child)
        return files

    def usages(self):
        print("python3 Api.py <option><value> <--import or -i>")
        print('-h or --help')
        print('-n or --namespace <namespace>')
        print('-g or --getcluster <none>')
        print('-i or --import <none> PS: -i must add -n <value>')

    # 传参函数。
    def main(self):
        global Namespace
        if not len(sys.argv[1:]): #if len()=null  run usages()
            self.usages()
        try:
            # hgi 没冒号说明不需要传参数只需要option即可，i:说明必须传参数
            opts,args = getopt.getopt(sys.argv[1:],"hg:i",['help',"=get","import"])
            for name, value in opts:
                if name in ("-h", "--help"):
                    self.usages()
                elif name in ("-g", "--get"):
                    print("sorry..{}".format(value))
                elif name in ("-i", "--import"):
                    Rancherz().ImportResourceYaml()
        except getopt.GetoptError as err:
            print(err)
            self.usages()

class Rancherz():
    def __init__(self):
        self.ComList = CommFun().getfilelist(filepath=yamlfilepath)

    ## ImportYaml To Rancher
    def ImportResourceYaml(self):
        print("import ing...")
        print("import end")


if __name__ == '__main__':
    CommFun().main()