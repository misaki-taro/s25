from django.shortcuts import render, HttpResponse
from web.forms import account

def register(request):
    form = account.RegisterModelForm()
    return render(request, 'register.html', {'form': form}) 

def send_sms(request):
    form = account.SendSmsForm(request)
    if form.is_valid():
        pass
    return HttpResponse('成功')