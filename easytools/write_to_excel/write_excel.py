#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lidezheng at 2017/6/12 下午2:29

import xlwt


def write_to_excel(filename, title, out_list):
    """写入excel文件, 后缀名xls"""
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('worksheet')
    for col, t in enumerate(title):
        worksheet.write(0, col, t)

    for row, row_list in enumerate(out_list, start=1):
        for col, v in enumerate(row_list):
            worksheet.write(row, col, v)

    workbook.save(filename)


if __name__ == '__main__':
    # 两点需要注意的问题:
    # 1. 中文需要编码为utf-8
    filename = './out_file.xls'
    title = ['姓名', '手机号', '时长']
    data = [[u'李德政'.encode('utf8'), '\t' + '123123123', 200]]
    write_to_excel(filename, title, data)
