'''
Author: Misaki
Date: 2023-07-25 15:11:34
LastEditTime: 2023-07-25 15:12:39
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