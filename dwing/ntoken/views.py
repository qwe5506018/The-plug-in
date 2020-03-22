from django.shortcuts import render

# Create your views here.


import json

from django.http import JsonResponse
from django.shortcuts import render
from user.models import The_user
from django.conf import settings

# 该应用下 状态码  10201 - 10299

# Create your views here.
def token_view(request):
    #login.html
    if request.method != 'POST':
        result = {'code':10201, 'error':'Please use POST'}
        return JsonResponse(result)

    uname = request.POST.get("uname")
    upwd = request.POST.get("upwd")
    username = json.loads(uname)
    print(username)
    password = json.loads(upwd)
    #TODO
    #获取用户
    users = The_user.objects.filter(username=username)
    print(users)
    if not users:
        result = {'code':10203, 'error':'The username or password is wrong'}
        return JsonResponse(result)
    user = users[0]
    print(user)
    #比对密码
    import hashlib
    m = hashlib.md5()
    m.update(password.encode())
    if m.hexdigest() != user.password:
        result = {'code':10204, 'error': 'The username or password is wrong !!'}
        return JsonResponse(result)
    #make token
    token = make_token(username)
    result = {'code':200, 'username':username, 'data':{'token':token.decode()}}
    return JsonResponse(result)

def make_token(username, exp=3600*24):
    import jwt, time
    payload = {'username':username, 'exp': time.time()+exp}
    key = settings.JWT_TOKEN_KEY
    return jwt.encode(payload, key, algorithm='HS256')