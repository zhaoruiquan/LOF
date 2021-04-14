# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         SendEMail
# Description:  利用python自带的smtp库发送邮件
# Author:       skymoon9406@gmail.com
# Date:         2020/4/20
# -------------------------------------------------------------------------------
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE
consumer_mail = os.environ.get('mail')
"""
关于发送失败的处理方法
https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp
# 设置低安全性
https://www.google.com/settings/security/lesssecureapps
# 设置未知位置影响
https://accounts.google.com/DisplayUnlockCaptcha
# 使用应用密码登录
https://support.google.com/accounts/answer/185833?hl=en&ctx=ch_DisplayUnlockCaptcha
"""


class SendEmailByGoogleMail:
    def __init__(self, subject, username, password, receivers):
        # 初始化账号信息
        self.user_account = {'username': username, 'password': password}
        # 初始化邮件主题
        self.subject = subject
        # 设置邮箱服务器地址
        self.smtp_server = 'hwsmtp.exmail.qq.com:465'
        # 初始化发件人姓名
        self.sender = consumer_mail
        # 初始化收件人邮箱
        self.receivers = receivers

    def send_mail(self, way, content, files):
        msg_root = MIMEMultipart()
        # 构造附件列表
        if files is not None:
            for file in files:
                file_name = file.split("/")[-1]
                att = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
                att["Content-Disposition"] = 'attachment; filename=%s' % file_name
                msg_root.attach(att)
        # 邮件发送者，主题
        msg_root['From'] = 'Family Notices'
        msg_root['Subject'] = self.subject
        # 接收者的昵称，其实这里也可以随便设置，不一定要是邮箱
        msg_root['To'] = COMMASPACE.join(self.receivers)
        # 邮件正文
        if way == 'common':
            msg_root.attach(MIMEText(content, 'plain', 'utf-8'))
        elif way == 'html':
            msg_root.attach(MIMEText(content, 'html', 'utf-8'))
        try:
            client = smtplib.SMTP_SSL('smtp.qq.com', smtplib.SMTP_SSL_PORT)
            print("连接到邮件服务器成功")
            client.login(self.user_account['username'], self.user_account['password'])
            print("登录成功")
            client.sendmail(self.sender, self.receivers, msg_root.as_string())
            print("发送成功")
        except smtplib.SMTPException as e:
            print("发送邮件异常:",e)
        finally:
            client.quit()

if __name__ == "__main__":
    pass
