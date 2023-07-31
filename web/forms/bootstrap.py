'''
Author: Misaki
Date: 2023-07-24 09:07:12
LastEditTime: 2023-07-29 01:01:05
LastEditors: Misaki
Description: 
'''
class BootstrapForm(object):
    # 为所有标签加上样式
    bootstrap_class_exclude = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if self.bootstrap_class_exclude and (name in self.bootstrap_class_exclude):
                continue
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入{0}'.format(field.label)
