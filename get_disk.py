#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
import socket
from email.mime.text import MIMEText
from email.header import Header
import psutil

# 磁盘阈值
disk_limit = 80
# 监控磁盘的路径
disk_path = "C:"


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('172.16.9.36', 10))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def send_email():
    """
    发送邮件代码
    """

    ip = get_host_ip()

    print(ip)

    # 发送者的邮箱
    sender = 'zhoujia@sunward.com.cn'
    # 接受者的邮箱
    receivers = ['zhoujia@sunward.com.cn']

    message = MIMEText('%s 机器磁盘超出阈值' % ip, 'plain', 'utf-8')
    message['From'] = Header("磁盘容量超出阈值警告", 'utf-8')
    message['To'] = Header("Admin", 'utf-8')
    message['Subject'] = Header('磁盘容量超出阈值警告', 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        # domain指公司域名
        smtpObj.connect("mail.domain.com", 25)
        # smtp的用户登入账号
        smtpObj.login("zhoujia@sunward.com.cn", "142536")
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def monitor_disk():
    """
    disk_usage判断是否超出界限值
    """
    global disk_limit
    global disk_path
    disk_percent = psutil.disk_usage(disk_path).percent
    if disk_percent > disk_limit:
        send_email()
    else:
        print("Disk space usage: {}%".format(disk_percent))


if __name__ == '__main__':
    monitor_disk()