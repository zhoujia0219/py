#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import psutil
except ImportError:
    print('错误: psutil模块没有发现!')
    exit()
import platform
import datetime
import time


def get_osinfo():
    '''获取操作系统相关信息'''
    osType = platform.system()
    osVersion = platform.version()
    osArchitecture = platform.architecture()
    hostName = platform.node()
    return osType, osVersion, osArchitecture, hostName


def get_processor():
    '''获取物理CPU个数'''
    return psutil.cpu_count(logical=False)


def get_cores():
    '''获取逻辑CPU个数'''
    return psutil.cpu_count()


def get_boot_time():
    '''获取开机时间'''
    return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")


def get_disk_root():
    '''获取根分区磁盘空间'''
    return psutil.disk_usage('D:')


def get_mem_total():
    '''获取内存容量'''
    return psutil.virtual_memory()[0] / 1024 / 1024


def get_mem_free():
    '''获取可用内存大小'''
    return psutil.virtual_memory()[4] / 1024 / 1024


def get_key():
    '''函数获取各网卡发送、接收字节数'''

    key_info = psutil.net_io_counters(pernic=True).keys()  # 获取网卡名称

    recv = {}
    sent = {}

    for key in key_info:
        recv.setdefault(key, psutil.net_io_counters(
            pernic=True).get(key).bytes_recv)  # 各网卡接收的字节数
        sent.setdefault(key, psutil.net_io_counters(
            pernic=True).get(key).bytes_sent)  # 各网卡发送的字节数

    return key_info, recv, sent


def get_rate(func):
    '''函数计算每1秒网卡速率'''
    key_info, old_recv, old_sent = func()  # 上1秒收集的数据

    time.sleep(1)

    key_info, now_recv, now_sent = func()  # 当前所收集的数据

    net_in = {}
    net_out = {}

    for key in key_info:
        net_in.setdefault(key, (now_recv.get(key) - old_recv.get(key)) / 1024)  # 每秒接收速率
        net_out.setdefault(key, (now_sent.get(key) - old_sent.get(key)) / 1024)  # 每秒发送速率

    return key_info, net_in, net_out


def main():
    '''程序入口函数'''
    ostype, osversion, osarchitecture, hostname = get_osinfo()

    print('操作系统类型:', ostype)
    print('操作系统版本:', osversion)
    print('操作系统位数:', osarchitecture[0])
    print('主机名:', hostname)
    print('物理CPU个数:', get_processor())
    print('逻辑CPU个数:', get_cores())
    print('开机时间:', get_boot_time())
    print('根分区可用空间(单位为MB):', get_disk_root()[2] / 1024 / 1024)
    print('内存总量(单位为MB):', get_mem_total())
    print('可用内存大小(单位为MB):', get_mem_free())

    i = 0
    while i < 3:  # 去获取每秒每块网卡的 速率
        key_info, net_in, net_out = get_rate(get_key)
        for key in key_info:
            print('%s\nInput:\t %-5sKB/s\nOutput:\t %-5sKB/s\n' %
                  (key, net_in.get(key), net_out.get(key)))
        i += 1


if __name__ == '__main__':
    main()
