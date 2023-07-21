'''
Author: Misaki
Date: 2023-07-21 09:45:09
LastEditTime: 2023-07-21 10:07:55
LastEditors: Misaki
Description: 
'''

from utils.ali import sms

send_sample = sms.Sample()
phone_numbers = '13713676304'
sign_name = 'mbug平台'
template_code = 'SMS_461960909'
template_param = '{code:12738}'

return_res = send_sample.send_single_message(phone_numbers, sign_name, template_code, template_param)

print(return_res)
