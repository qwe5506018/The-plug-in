import pickle
import json
from django.shortcuts import render

# Create your views here.
import hashlib

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import The_user
import redis
from .tasks import send_active_email
from django_redis import get_redis_connection

r = redis.Redis(host="127.0.0.1", port=6379, db=0)


# Create your views here.

# 客户端注册

def user_get(request):
    # get拿页面
    if request.method == "GET":
        return render(request, "user/index.html")
        # post处理注册
    elif request.method == "POST":

        username = request.POST.get("Username")
        password = request.POST.get("Password")
        email = request.POST.get("Email")
        phone = request.POST.get("Phone")
        # cc=pickle.load("code")
        # print('000000000000000')
        # print(request.POST.get("code"))
        # print(type(request.POST.get("code")))
        # if pickle.dumps(cc) == 'code':
        # if pickle.loads(cc) == 'code':
        # print(json_str["code"] == "code")

        # 用户数据是否没有传到后端
        if not username:
            result = {'code': 10101, 'error': 'Please give me username~'}
            return JsonResponse(result)
            # 查询数据库中是否有该用户数据
        uname = The_user.objects.filter(username=username)

        if not password:
            result = {"code": 20202}
            return JsonResponse(result)

            # 检查账号是否注册
        if uname:
            print(123456)
            # 当前用户名已经注册
            result = {'code': 10102, 'error': 'The username is already registed~'}
            return JsonResponse(result)
    return JsonResponse({"code": 40200})


# 发出 邮件激活码 ?
# 生成随机码
def verify_user(request):
    code = request.POST.get("code")
    username = request.POST.get("Username")
    json_str = json.loads(code)
    email = request.POST.get("Email")
    password = request.POST.get("Password")
    one = request.POST.get("Phone")
    phone = json.loads(one)
    if json_str["code"] == "code":
        # print('程序进来啦')
        import random, base64
        import random, base64
        random_num = random.randint(1000, 9999)
        random_str = username + '_' + str(random_num)
        # 最终链接上的code为
        print(random_str)
        code_str = base64.urlsafe_b64encode(random_str.encode())
        # 随机码存入缓存, 用于激活时,后端进行校验
        print(code_str)
        # 验证码redis中储存时间为5分钟
        r.set("email_%s" % username, random_str, 60 * 5)
        # 执行发送邮件
        send_active_email(email, random_num)
        # #接收到传输过来的验证码
        return JsonResponse({"code": 10200})


# 创建用户数据
def user_data(request):
    username = request.POST.get("Username")
    email = request.POST.get("Email")
    password = request.POST.get("Password")
    one = request.POST.get("Phone")
    phone = json.loads(one)
    C = request.POST.get("Code")
    code = json.loads(C)
    p = r.get("email_%s" % username)
    a = p.decode().split("_")
    print(a[1])
    print(code)
    print(int(a[1]) == int(code))

    # 值为['"username"', 'ramdom_num']

    if int(a[1]) == int(code):
        print('is xing')
        import hashlib
        m = hashlib.md5()
        m.update(password.encode())
        # 如果没有注册 那么就在数据库中放入该数据
        try:
            The_user.objects.create(username=username,
                                    password=m.hexdigest(),
                                    phone=phone,
                                    email=email)
        except Exception as e:
            print('---create user error')
            print(e)
            result = {'code': 10103, 'error': 'The username is already registed !'}
            return JsonResponse(result)
    else:
        print('esle xing')
        result = {"code": 10408}
        return JsonResponse(result)
    result = {"code":20200}
    return JsonResponse(result)


# 修改密码
def modify_user(request):
    if request.method == "GET":
        return render(request, "user/modify.html")
    if request.method == "POST":
        json_str = request.POST.get("uname")
        uname = json.loads(json_str)
        json_str1 = request.POST.get("upwd")
        json_str2 = request.POST.get("upwd1")
        upwd = json.loads(json_str1)
        upwd1 = json.loads(json_str2)
        # 查询输入账号是否和数据库比对
        username = The_user.objects.filter(username=uname)
        password_set = username[0].password
        print(password_set)
        # 判断该用户是否已经注册过
        if not username:
            result = {"code": 40041}
            return JsonResponse(result)
        # 判断两次密码是否输入一致
        if upwd != upwd1:
            result = {"code": 40042}
            return JsonResponse(result)

        else:
            import hashlib
            m = hashlib.md5()
            m.update(upwd.encode())
            username.update(password=m.hexdigest())
            result = {"code": 40020}
            return JsonResponse(result)
    return render(request, "main_interface/interface.html")


