'''
Author: Misaki
Date: 2023-08-06 15:41:59
LastEditTime: 2023-08-06 15:50:15
LastEditors: Misaki
Description: 
'''
import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "s25.settings")
django.setup()  # os.environ['DJANGO_SETTINGS_MODULE']

from django.conf import settings
from utils.tencent.cos import delete_file, delete_file_list

# 删除单个

# delete_file(
#     bucket='13713676304-1690769465-1302722017',
#     region='ap-guangzhou',
#     key='42677d7a1547566ec391fd33403d0c34.jpg'
# )

# 批量删除
# 参数不会传可以点进去看函数
delete_file_list(
    bucket='13713676304-1690769465-1302722017',
    region='ap-guangzhou',
    key_list=[
        {'Key': '96ce7e5a504f19abeeda61ad5d3c7032.jpg'},
        {'Key': '9b616ff286e9f75a0337afee2ab7cad0.jpg'}
    ]
)

