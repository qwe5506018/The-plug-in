import redis
import json

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic.base import View
from .models import *
from django.conf import settings
from django_redis import get_redis_connection
from user.models import The_user
from .models import The_user_to_collect
from .models import The_antique
from .models import Reward
from .models import For_the_category
from .models import Photo_user
import datetime
from django.shortcuts import render_to_response
from haystack.forms import ModelSearchForm

from tools.logging_check import logging_check

pool = redis.ConnectionPool(host="127.0.0.1")
r = redis.Redis(connection_pool=pool)


# Create your views here

def interface(request):
    if request.method == "GET":
        return render(request, "main_interface/interface.html")


class Phount(View):
    # 用户点击获取个人信息
    # 注 此数据 为基础数据
    @logging_check
    def get(self, request):
        username = request.muser
        if not username:
            result = {"code": 10001}
            return JsonResponse(result)
        user = The_user.objects.get(username=username)
        return JsonResponse({'code': 10200, "data": user.id})

    # 用户要增加一些没有添加的数据
    @logging_check
    def post(self, request):
        username = request.muser
        if not username:
            result = {"code": 10001}
            return JsonResponse(result)

        # 用户想要显示id
        _name = request.POST.get("name")
        name = json.loads(_name)
        # 用户性别
        _gender = request.POST.get("gender")
        gender = json.loads(_gender)
        # 用户照片
        _photo = request.POST.get("photo")
        photo = json.loads(_photo)
        # 将用户数据存入redis和mysql
        # 插入数据前先做一次查询
        if Photo_user.objects.get(name=name):
            result = {"code": 10004}
            return JsonResponse(result)
        try:
            Photo_user.objects.create(name=name,
                                      gender=gender,
                                      photo=photo)
        except Exception as e:
            print(e)
            result = {"code": 10404}
            return JsonResponse(result)
        # 同时  用户数据也要存入redis
        # 一个用户名对应一个列表
        try:
            r.lpush(username, name, gender, photo)
        except Exception as e:
            print(e)

    # 用户想要修改自己的数据 除了账号和密码
    @logging_check
    def put(self, request):
        username = request.muser
        if not username:
            result = {"code": 10001}
            return JsonResponse(result)
        users = The_user.objects.filter(username=username)
        put_ = request.POST.get("put_user")
        put_user = json.loads(put_)
        if put_user == "put_user":
            _name = request.POST.get("name")
            name = json.loads(_name)
            _gender = request.POST.get("gender")
            gender = json.loads(_gender)
            _photo = request.POST.get("photo")
            photo = json.loads(_photo)
            # 接收到用户传过来的数据 先做一次查询
            if Photo_user.objects.get(name=name):
                if Photo_user.objects.get(gender=gender):
                    if Photo_user.objects.get(photo=photo):
                        result = {"code": 10040}
                        return JsonResponse(result)
                    # 表示用户修改了photo中的数据
                    if not Photo_user.objects.get(username=username):
                        result = {"code": 10044}
                        return JsonResponse(result)
                    else:
                        p = Photo_user.objects.filter(username=username)
                        p.update(photo=photo)

                if not Photo_user.objects.get(username=username):
                    result = {"code": 10044}
                    return JsonResponse(result)
                else:
                    p = Photo_user.objects.filter(username=username)
                    p.update(gender=gender)


def antique(request):
    if request.method == "GET":
        return render(request, "main_interface/antique.html")


def information(request):
    if request.method == "GET":
        return render(request, "main_interface/information.html")


def today(request):
    if request.method == "GET":
        return render(request, "main_interface/today.html")


# 用户消息创建
class Add_information(View):
    # 增加用户消息
    @logging_check
    def post(self, request):
        username = request.muser
        user = The_user.objects.get(username=username)
        if not user:
            result = {"code": 10053}
            return JsonResponse(result)
        # JSON数据格式
        in_ = request.POST.get("悬赏消息类别")  # 比如古风类限制字数不能超过10个字
        in_t = json.loads(in_)
        in_to = json.loads(in_t)
        # 判断长度
        #悬赏类别长度不能大于10
        if len(in_to) < 0 and len(in_to) > 10:
            result = {"code": 10004}
            return JsonResponse(result)
        # 把该数据插入进去
        The_antique.objects.create(name=in_to)
        picture__ = request.POST.get("悬赏图片格式")
        picture_ = json.loads(picture__)
        picture = json.loads(picture_)
        # 将图片存入数据库
        Reward.objects.create(logo=picture)
        # 获取悬赏内容 JSON字符串
        fomat = request.POST.get("悬赏消息内容")
        fomation = json.loads(json.loads(fomat))
        For_the_category.objects.create(name=fomation)
        return JsonResponse({"code":10200})


    # 获取点赞系统  消息存入redis
    def put(self,request):
        username = request.muser
        user = The_user.objects.get(username=username)
        if not user:
            result = {"code": 10053}
            return JsonResponse(result)
        praise_ = request.POST.get("praise")
        praise = json.loads(json.loads(praise_))
        if praise == "praise":
            import redis
            pool = redis.ConnectionPool(host='localhost', port=6379, db=1)
            r = redis.Redis(connection_pool=pool)
            while True:
                try:
                    with r.lock('key', timeout=5, blocking_timeout=3) as lock:
                        u = The_user.objects.get(username='创建具体的数据库')
                        u.praise += 1
                        u.save()
                    break
                except Exception as e:
                    print('lock is failed')

            return HttpResponse({'code': 200})

class GoodsSearchView(View):
    #查询[es版]
    def post(self,request):
        #官方要求 触发搜索es 需要在POST提交时 使用表单提交,且提交内容中格式如下  q="搜索内容"
        #<input  type=text name="q">
        form = ModelSearchForm(request.POST,load_all=True)

        if form.is_valid():
            results = form.search()
        else:
            return JsonResponse({"code":999,"error":"Your POST is valid"})

        #将结果进行分页
        page_size = settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE
        paginator = Paginator(results,page_size)

        #如果当前非第一页,前端传输具体页码 前端 page
        #前端在form 提交里 若有page字段 则代表用户当前想去往的具体页码
        try:
            page = paginator.page(int(request.POST.get("page",1)))
        except Exception as e:
            print(e)
            return JsonResponse({"code":9999,"error":"page is wrong"})

        #拼接返回值
        sku_list = []
        #拿出当前页的数据
        for res in page.object_list:
            sku = {
                "id":res.object.id,
                "name":res.object.name,
                "brand":res.object.brand,
            }
            sku_list.append(sku)

        result = {"code":200,"data":sku_list,"paginator":
            {"pagesize":page_size,"total":len(results)},
            "base_url":settings.PIC_URL}

        return JsonResponse(result)


#兴趣作品（浏览过的消息）
class Interest(View):
    @logging_check
    def post(self,request):
        username = request.muser
        user = The_user.objects.get(username=username)
        if not user:
            result = {"code": 10050}
            return JsonResponse(result)

        #获取到用户点击收藏的具体数据
        _count = request.POST.get("用户点击收藏后数据加")
        count = json.loads(_count)
        if count == "xxxxx":
            import redis
            pool = redis.ConnectionPool(host='localhost', port=6379, db=1)
            r = redis.Redis(connection_pool=pool)
            data = request.POST.get("传输上来的数据")
            connt = The_user.objects.create(connt=data)
            r.set("key", data, 60 * 60 * 24 * 30)  # 收藏数据存在mysql和redis30天
            try:
                with r.lock('key', timeout=5, blocking_timeout=3) as lock:
                    u = The_user.objects.get(username='创建具体的数据库')
                    u.praise += 1
                    u.save()
            except Exception as e:
                print('lock is failed')

        #数据存完后前段页面弹框显示
        result = {"code":10400}
        return JsonResponse(result)

    @logging_check
    def delete(self,request):
        username = request.muser
        try:
            user = The_user.objects.get(username=username)
        except:
            print("请登录")

        #如果用户需要删除收藏的数据
        _count = request.POST.get("用户点击收藏后数据加")
        count = json.loads(_count)
        _data = request.POST.get("获取用户传输上来的对应数据")
        data = json.loads(_data)
        if count == "xxxxx":
            import redis
            pool = redis.ConnectionPool(host='localhost', port=6379, db=1)
            r = redis.Redis(connection_pool=pool)
            #删除用户对应数据
            r.DEL("key")
            The_user.objects.delete(connt=data)
            try:
                with r.lock('key', timeout=5, blocking_timeout=3) as lock:
                    u = The_user.objects.get(username='创建具体的数据库')
                    u.praise -= 1
                    u.save()
            except Exception as e:
                print('lock is failed')



#用户私密消息
class Private(View):
    @logging_check
    def post(self,request):
        username = request.muser
        user = The_user.objects.get(username=username)
        if not user:
            result = {"code":10051}
            return JsonResponse(result)

        data = request.POST.get("官方消息")
        #获取官方发送的邮件
        email = user.email
        #执行发送邮件
        send_active_email(email, data)
        #获取用户好友列表
        friends = user.friends
        _friends_count = request.POST.get("friends_count")
        friends_count  = json.loads(_friends_count)
        result = {"code":90999,"data":friends_count}
        return JsonResponse(result)


#我发布的/我收藏的
class History(View):
    @logging_check
    def post(self,request):
        username = request.muser
        user = The_user.objects.get(username=username)
        if not user:
            result = {"code": 10052}
            return JsonResponse(result)
        #判断成功 是否收藏
        count__ = request.POST.get("count")
        count = json.loads(json.loads(count__))
        a = request.POST.get("collection")
        collection = json.loads(json.loads(a))
        #判断是否触发该收藏
        try:
            The_user_to_collect.objects.get(username = username)
        except Exception as e:
            print(e)
        if collection == "collection":
            #将该链接放入数据库
            The_user_to_collect.objects.create(count = count)

    #删除我的收藏
    def  delete(self,request):
        username = request.muser
        user = The_user.objects.get(username=username)
        if not user:
            result = {"code": 10052}
            return JsonResponse(result)
        # 判断成功 是否收藏
        count__ = request.POST.get("count")
        count = json.loads(json.loads(count__))
        a = request.POST.get("collection")
        collection = json.loads(json.loads(a))
        if collection == "collection":
            try:
                user_ = The_user_to_collect.objects.get(count = count)
            except Exception as e:
                print(e)
                The_user_to_collect.objects.delete(count = user_)



#好友列表
class Friends_List(View):
    @logging_check
    def post(self,request):
        username = request.muser
        user = The_user.objects.get(username=username)
        if not user:
            result = {"code": 10053}
            return JsonResponse(result)
        _add = request.POST.get("add")
        add = json.loads(_add)
        #获取对方的账号信息
        _ = request.POST.get("对方点击加好友给服务器发消息")
        ent = json.loads(_)
        if ent == "xxx":
            #服务器收到消息
            others = The_user.objects.get("username=username")
        if add == "add":
            add_user = The_user.objects.create(friend=others)




#显示本周最佳/作品展示/榜首详细信息
class This_week_the_best(View):
    pass
