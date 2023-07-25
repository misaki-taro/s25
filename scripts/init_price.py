'''
Author: Misaki
Date: 2023-07-25 15:12:43
LastEditTime: 2023-07-25 15:17:59
LastEditors: Misaki
Description: 
'''
import base

from web import models


def run():
    # 添加一个条目
    exist = models.PricePolicy.objects.filter(category=1, title='个人免费版').exists()
    if not exist:
        models.PricePolicy.objects.create(
            category=1, 
            title='个人免费版',
            price=0,
            project_num=3,
            project_member=2,
            project_space=20,
            per_file_size=5
        )


if __name__ == '__main__':
    run()