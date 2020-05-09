#!/usr/bin/python
# -*- coding:utf-8 -*-
# python2环境

import os
import json
import time
import shutil
import re
# import io

import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

# 使用linux系统交互输入信息时，
# 会出现backspace无法删除乱码的情况；
# 导入readline模块可以消除这种乱码情况。
# 需要取消注释即可

# import readline


# 选择项
xuanze = '''对应编号：
             ------------部署准备------------
             1. 机器性能调优(谨慎使用，勿重复使用)
             2. 老集群删除
             ------------部署集群------------
             3. docker安装 
             4. rancher服务端部署
             5. 待定
             6. 待定
             7. 安装harbor
             --------------其它--------------
             h. 显示帮助help
             q. quit/退出选项'''

KernelEdit = '''
net.bridge.bridge-nf-call-ip6tables=1
net.bridge.bridge-nf-call-iptables=1
net.ipv4.ip_forward=1
net.ipv4.conf.all.forwarding=1
net.ipv4.neigh.default.gc_thresh1=4096
net.ipv4.neigh.default.gc_thresh2=6144
net.ipv4.neigh.default.gc_thresh3=8192
net.ipv4.neigh.default.gc_interval=60
net.ipv4.neigh.default.gc_stale_time=120

# 参考 https://github.com/prometheus/node_exporter#disabled-by-default
kernel.perf_event_paranoid=-1

#sysctls for k8s node config
net.ipv4.tcp_slow_start_after_idle=0
net.core.rmem_max=16777216
fs.inotify.max_user_watches=524288
kernel.softlockup_all_cpu_backtrace=1
kernel.softlockup_panic=1
fs.file-max=2097152
fs.inotify.max_user_instances=8192
fs.inotify.max_queued_events=16384
vm.max_map_count=262144
fs.may_detach_mounts=1
net.core.netdev_max_backlog=16384
net.ipv4.tcp_wmem=4096 12582912 16777216
net.core.wmem_max=16777216
net.core.somaxconn=32768
net.ipv4.ip_forward=1
net.ipv4.tcp_max_syn_backlog=8096
net.ipv4.tcp_rmem=4096 12582912 16777216

net.ipv6.conf.all.disable_ipv6=1
net.ipv6.conf.default.disable_ipv6=1
net.ipv6.conf.lo.disable_ipv6=1

kernel.yama.ptrace_scope=0
vm.swappiness=0

# 可以控制core文件的文件名中是否添加pid作为扩展。
kernel.core_uses_pid=1

# Do not accept source routing
net.ipv4.conf.default.accept_source_route=0
net.ipv4.conf.all.accept_source_route=0

# Promote secondary addresses when the primary address is removed
net.ipv4.conf.default.promote_secondaries=1
net.ipv4.conf.all.promote_secondaries=1

# Enable hard and soft link protection
fs.protected_hardlinks=1
fs.protected_symlinks=1

# 源路由验证
# see details in https://help.aliyun.com/knowledge_detail/39428.html
net.ipv4.conf.all.rp_filter=0
net.ipv4.conf.default.rp_filter=0
net.ipv4.conf.default.arp_announce = 2
net.ipv4.conf.lo.arp_announce=2
net.ipv4.conf.all.arp_announce=2

# see details in https://help.aliyun.com/knowledge_detail/41334.html
net.ipv4.tcp_max_tw_buckets=5000
net.ipv4.tcp_syncookies=1
net.ipv4.tcp_fin_timeout=30
net.ipv4.tcp_synack_retries=2
kernel.sysrq=1'''

# COMMON通用方法函数集合
class CommonFun():
    def __init__(self):
        pass  
    # 遍历文件目录，获取路径下所有文件
    def getfilelist(self, filepath):
        filelist = os.listdir(filepath)
        files = []
        for i in range(len(filelist)):
            child = os.path.join('%s/%s' % (filepath, filelist[i]))
            if os.path.isdir(child):
                files.extend(self.getfilelist(child))

            else:
                files.append(child)
        return files

    # sed 替换功能函数
    def alter(self, file, old_str, new_str):
        """
        替换文件中的字符串
        :param file:文件名
        :param old_str:旧字符串
        :param new_str:新字符串
        :return:
        """
        file_data = ""
        with open(file, "r") as f:
            for line in f:
                if old_str in line:
                    line = line.replace(old_str,new_str)
                file_data += line
        with open(file,"w") as f:
            f.write(file_data)


# 使用的选项菜单事项类
class Things():
    def __init__(self, username='none'):
        self.username = username
        self.commonfun = CommonFun()

    # 内核性能调优
    def KernelPerformanceTuning(self):
        print("KernelPerformanceTuning Begin ...")
        print("内核参数调优，请不要重复执行！！！！")
        time.sleep(1)
        print("1、>>>>>>>>>>> Begin sysctl.conf...")
        cmd_sysctl = "echo " + '''"{}"'''.format(KernelEdit) + " >> /etc/sysctl.conf"
        cmd_sysctl_ok = "sysctl -p"
        print(cmd_sysctl.decode("utf-8"))
        print(cmd_sysctl_ok)
        try:
        #    os.popen(cmd_sysctl).read()
        #    os.popen(cmd_sysctl_ok).read()
            print("sysctl.conf is OK")
        except Exception as e:
            print("sysctl error: {}".format(e))

        print("2、>>>>>>>>>>> Begin limits.conf...")
        cmd_limits = '''cat >> /etc/security/limits.conf <<EOF
* soft nofile 65535
* hard nofile 65536
EOF'''
        print(cmd_limits)
        try:
        #    os.popen(cmd_limits).read()
            print("limits.conf is OK")
        except Exception as e:
            print(e)

        print("3、>>>>>>>>>>> Begin selinux disable...")
        try:
            with open(r"/etc/selinux/config", "r") as f:
                readfile = f.read()
                if "SELINUX=disabled" in readfile:
                    print("selinux is disabled before.")
                else:
                #    self.commonfun.alter("/etc/selinux/config","SELINUX=enforcing","SELINUX=disabled")
                #    os.popen("setenforce 0").read()
                    print("selinux disable success")
        except Exception as e:
            print("error: {}".format(e))

        print("4、>>>>>>>>>>> Begin firewalld stop...")
        cmd_firewalld_stop = "systemctl stop firewalld && systemctl disable firewalld"
        try:
        #    os.popen(cmd_firewalld_stop).read()
            print("firewalld stop success")
        except Exception as e:
            print(e)

        print("5、>>>>>>>>>>> Begin NetworkManager stop...")
        cmd_networkmanager_stop = "systemctl stop NetworkManager && systemctl disable NetworkManager"
        try:
        #    os.popen(cmd_networkmanager_stop).read()
            print("NetworkManager stop success")
        except Exception as e:
            print(e)
        
        print(">>>>>>>>>>> Begin base yum install...")
        def YumInstallBase():
            actions = raw_input("是否yum安装基础组件(Y/N):>>> ");
            if actions == "N" or actions == "n":
                print("exit to Menu ing...")
                time.sleep(2)
                Menu().run()
            elif actions == "Y" or actions == "y":
                cmd_yum_install = "yum install -y ntp ntpdate nfs-utils lrzsz zip unzip sshpass dnsmasq vim gcc c++  net-tools cmake lsof"
                print(cmd_yum_install)
                try:
                #    os.popen(cmd_yum_install).read()
                    print("yum base-tools success")
                except Exception as e:
                    print(e)
            else:
                print("Y/N IN again")
                YumInstallBase()
        YumInstallBase()
        print("KernelPerformanceTuning success, To Menu ing...")
        time.sleep(1)
        Menu().run()
        print("reboot??")


    # 老集群删除操作
    def OldKubernetesClusterDel(self):
        try:
            actions = raw_input("请输入操作: ");
            if actions == "h":
                Menu().run()

        except Exception, e:
            print("请确保有项目目录; Error: {}".format(e))

    # DockerInstallOK
    def DockerInstallOK(self):
        print(">>>>>>>>>>> Begin install Docker...")
        cmd_docker_conf = '''cat <<EOF > /etc/docker/daemon.json
{
  "registry-mirrors": ["https://7h0c2lco.mirror.aliyuncs.com"],
  "graph": "/data/docker",
  "insecure-registries": ["xxxx"],
  "selinux-enabled": false,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "30m",
    "max-file": "10"
  }
}
EOF
'''
        try:
            print("输入 h 返回菜单Menu\n 输入 q 退出程序")
            actions = raw_input("安装Docker版本(default: 18.06.1):>>> ");
            if actions == "h":
                Menu().run()
            elif actions == "q":
                Menu().quit()
            elif actions == "":
                commands = ["yum install -y yum-utils device-mapper-persistent-data lvm2",
                            "yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo",
                            "yum install -y docker-ce-18.06.1 --skip-broken",
                            "systemctl enable docker",
                            "systemctl start docker",
                            "{}".format(cmd_docker_conf),
                            "systemctl restart docker"]
                for i in commands:
                    print("begin command: {}".format(i))
                #    os.popen(i).read()
            elif re.findall("\d.\d",actions):
                commands = ["yum install -y yum-utils device-mapper-persistent-data lvm2",
                            "yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo",
                            "yum install -y docker-ce-{} --skip-broken".format(actions),
                            "systemctl enable docker",
                            "systemctl start docker",
                            "{}".format(cmd_docker_conf),
                            "systemctl restart docker"]
                for i in commands:
                    print("begin command: {}".format(i))
                #    os.popen(i).read()
            else:
                print("input err. please input again...")
                self.DockerInstallOK()
            print("Docker Install success, To Menu ing...")
            time.sleep(1)
            Menu().run()
        except Exception, e:
            print("Output Error: {}".format(e))
            # print e

    # RancherInstallOK
    def RancherInstallOK(self):
        print(">>>>>>>>>>> Begin install Rancher...")
        print("请在部署Rancher主机上运行安装..")
        try:
            print("输入 h 返回菜单Menu\n 输入 q 退出程序")
            actions = raw_input("是否安装Rancher服务端(Y/N):>>> ");
            if actions == "h":
                Menu().run()
            elif actions == "q":
                Menu().quit()
            elif actions == "Y" or actions == "y":
                print("请确认映射路径正确！！！")
                PathDir = raw_input("Rancher映射路径(/data/rancher/):>>> ")
                command = '''docker run -d --restart=unless-stopped \
-p 80:80 -p 443:443 \
-v {}:/var/lib/rancher/ \
-v /root/var/log/auditlog:/var/log/auditlog \
-e CATTLE_SYSTEM_CATALOG=bundled \
-e AUDIT_LEVEL=3 \
rancher/rancher:2.4.0'''.format(PathDir)
                print("############################################")
                print("{}".format(command))
                print("############################################")
                if raw_input("请确认映射路径正确！！??正确请按ENTER回车>>>") == "":
                    print("command: {}".format(command))
                #    os.popen(command)
                else:
                    print("input err. please input again...")
                    self.RancherInstallOK()
                
            elif actions == "N" or actions == "n":
                print("exit to Menu ing...")
                time.sleep(1)
                Menu().run()
            else:
                print("input err. please input again...")
                self.RancherInstallOK()
            print("Rancher Install success, To Menu ing...")
            time.sleep(1)
            Menu().run()
        except Exception as e:
            print("Error: {}".format(e))

    # Rancher Api create resource
    def RancherToAPIApplyResource(self):
        pass


# 菜单menu界面化
class Menu():
    def __init__(self):
        self.thing = Things()
        self.choices = {
            "1": self.thing.KernelPerformanceTuning,
            "2": self.thing.OldKubernetesClusterDel,
            "3": self.thing.DockerInstallOK,
            "4": self.thing.RancherInstallOK,
            "q": self.quit
        }

    def display_menu(self):
        # linux命令 clear
        # windows CMD调试请使用 cls
        os.system('clear')
        # os.system('cls')
        # 解码 utf-8 适用于windows调试
        print(xuanze.decode("utf-8"))

    def run(self):
        while True:
            self.display_menu()
            try:
                choice = raw_input("Enter an option >>> ")
            except Exception as e:
                print("Please input a valid option!");
                continue

            choice = str(choice).strip()
            action = self.choices.get(choice)
            if action:
                action()
                stopword = "h"
                print ">>> ",
                for line in iter(raw_input, stopword):  # 输入为"h"，表示输入结束
                    if line == "q":
                        self.quit()
                    print ">>> ",
            else:
                print("{0} is not a valid choice".format(choice))
                #time.sleep(1)

    def quit(self):
        print("--------------\nThank you for using this script!\n--------------")
        sys.exit(0)


if __name__ == '__main__':
    Menu().run()