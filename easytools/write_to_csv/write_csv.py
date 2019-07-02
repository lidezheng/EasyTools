#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lidezheng at 2017/6/12 下午2:29

import csv


def write_csv(filename, title, out_list):
    """写入csv文件"""
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        csvfile.write('\xEF\xBB\xBF')  # 写入BOM，解决中文显示乱码
        writer.writerow(title)
        writer.writerows(out_list)

if __name__ == '__main__':
    # 两点需要注意的问题:
    # 1. 中文需要编码为utf-8
    # 2. 长数字想要完整显示需要在前面加 '\t'
    filename = './out_file.csv'
    title = ['姓名', '手机号', '时长']
    data = [[u'李德政'.encode('utf8'), '\t' + '123123123', 200]]
    write_csv(filename, title, data)
