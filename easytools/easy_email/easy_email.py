#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -*- encoding: gbk -*-
# Created by lidezheng at 2016/10/30 下午12:42

import email, email.header
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr, formatdate
import smtplib

from imapclient import IMAPClient


class EasyEmail:
    """
        邮件发送类: 支持普通邮件和html格式的邮件
        使用Gmail账户或本机smtp服务发送邮件
    """
    def __init__(self):
        pass

    @staticmethod
    def send_by_gmail(from_name, subject, content, email_to):
        """
        :param from_name: 显示的发件人姓名
        :param subject: 邮件主题
        :param content: 邮件正文，支持html文本
        :param email_to: 收件人列表 List
        :return: True 成功， False 失败
        """
        if not from_name or not subject \
                or not content or not email_to:
            return False

        email_from = "xx@xx.com"           # Gmail邮箱账号
        email_from_password = "xx"            # Gmail邮箱密码
        gmail_smtp_server = "smtp.gmail.com"

        try:
            e_object = MIMEText(content, 'html', 'utf-8')
            e_object['From'] = EasyEmail._format_address(from_name + "<%s>" % email_from)
            e_object['To'] = ','.join(email_to).encode('utf-8')
            e_object['Subject'] = Header(subject, 'utf-8').encode()
            e_object['Date'] = formatdate(localtime=True)

            # 发邮件
            server = smtplib.SMTP(gmail_smtp_server, 587)
            # server.set_debuglevel(1)  # 用于打印交互信息
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(email_from, email_from_password)
            server.sendmail(email_from, email_to, e_object.as_string())
            server.quit()

            print "done"
            return True
        except Exception, e:
            print e
            print "error"
            return False

    @staticmethod
    def _format_address(s):
        """
        :param s: 格式化发件人姓名
        :return:
        """
        name, e_address = parseaddr(s)
        e_address = e_address.encode('utf-8') if isinstance(e_address, unicode) else e_address
        return formataddr((Header(name, 'utf-8').encode(), e_address))


    @staticmethod
    def send_by_localhost(from_name, subject, content, email_to):
        """
        :param from_name: 发件人： somebody somebody@somesite.com
        :param subject: 邮件主题
        :param content: 邮件正文
        :param email_to: 收件人列表
        :return:
        """
        if not from_name or not subject \
                or not content or not email_to:
            return False

        try:
            e_object = MIMEText(content, 'html', 'utf-8')
            e_object['From'] = EasyEmail._format_address(from_name)
            e_object['To'] = ','.join(email_to).encode('utf-8')
            e_object['Subject'] = Header(subject, 'utf-8').encode()
            e_object['Date'] = formatdate(localtime=True)

            # 发邮件
            server = smtplib.SMTP(host="localhost", port=25)    # 默认端口25
            # server.set_debuglevel(1)  # 用于打印交互信息
            server.sendmail(from_name, email_to, e_object.as_string())
            server.quit()
            print "done"
            return True
        except Exception, e:
            print e
            return False

    send = send_by_localhost

    @staticmethod
    def get_email(host=None, port=993, ssl=True, username=None, password=None):
        """
            从指定邮箱账号读取未读邮件(默认收件箱INBOX)，并标记为已读
        :param host: imap主机
        :param port: imap端口，Gmail为993
        :param ssl: 是否启用ssl，默认启用
        :param username: 用户名
        :param password: 登录密码
        :return: （迭代器）邮件列表 [{'id': '', 'subject': '', 'from': '', 'content': ''}]
        """
        if not host or not port or not ssl or not username or not password:
            return

        server = IMAPClient(host=host, port=port, use_uid=True, ssl=ssl)
        server.login(username=username, password=password)

        select_info = server.select_folder("INBOX")
        # print ("%d messages in INBOX" % select_info['EXISTS'])

        all_message_ids = server.search(["UNSEEN"])
        print len(all_message_ids)

        start = 0
        size = 1        # 每次取回邮件的个数，请自由配置
        while True:
            message_ids = all_message_ids[start: (start + size)]    # 分批从服务器获取邮件内容
            start += size
            if not message_ids:
                break

            response = server.fetch(message_ids, ['BODY.PEEK[]'])

            for message_id, message in response.iteritems():
                try:
                    e = email.message_from_string(message['BODY[]'])
                    subject = str(email.header.make_header(email.header.decode_header(e.get("SUBJECT"))))
                    mail_from = str(email.header.make_header(email.header.decode_header(e.get("From"))))

                    maintype = e.get_content_maintype()

                    content = ""
                    if maintype == 'multipart':
                        for part in e.get_payload():
                            if part.get_content_maintype() == 'text':
                                content = part.get_payload(decode=True).strip()
                    elif maintype == 'text':
                        content = e.get_payload(decode=True).strip()

                    # 将内容编码为utf8，可以根据需要更改
                    # content = content.decode('gbk')

                    # server.add_flags(messages=message_id, flags=[b'\\SEEN'])  # 标记已读
                    info = {
                        'id': message_id,
                        'subject': subject,
                        'from': mail_from,
                        'content': content
                    }
                except Exception, e:
                    print e
                yield info
        return


def test_send():
    # 使用示例
    # 运行环境 CentOS 7.2， 需要启动smtp服务
    email_from = "脚本 <xx@xx.com>"
    subject = "xx"
    content = "<h1>hello, email.</h1>"
    email_to = ['xx@qq.com']
    EasyEmail.send_by_localhost(email_from, subject, content, email_to)

def test_get_email():
    HOST = "imap.gmail.com"
    PORT = 993
    USERNAME = "xx@xx.com"
    PASSWORD = "xx"
    PASSWORD = "xx"
    SSL = True
    email_info = EasyEmail.get_email(host=HOST, port=PORT, ssl=SSL, username=USERNAME, password=PASSWORD)
    if email_info:
        for info in email_info:
            for key in info:
                print key
                print info.get(key)
                print '-'*20

if __name__ == "__main__":
    test_send()
