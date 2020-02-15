from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
import requests
import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import datetime
import random
from .models import product
from .models import subuser
from .models import order
from .forms import UserForm, RegisterForm

# Create your views here.
def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return HttpResponseRedirect("/asmr/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = subuser.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_email_user = subuser.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = subuser.objects.create()
                new_user.username = username
                new_user.password = password1
                new_user.email = email
                new_user.save()
                return render(request, 'login.html', locals())
    register_form = RegisterForm()
    return render(request, 'register.html', locals())


def login(request):
    sort = request.GET.get('sort')
    if sort:
        product_list = product.objects.order_by(sort).reverse()
    else:
        product_list = product.objects.order_by('add_date').reverse()
    paginator = Paginator(product_list, 3)
    page = request.GET.get('page')
    dis_range = range(1, paginator.num_pages + 1)
    try:
        products = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)
    if request.method == "POST":
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = subuser.objects.get(username=username)
                if user.password == password:
                    purchased = order.objects.filter(order_uid=username)
                    purchasedlist = list(purchased)
                    namelist = []
                    for item in purchasedlist:
                        namelist.append(item.name)
                    return render(request, 'index.html', {'products': products, 'purchased': namelist, 'username': user.username, 'dis_range': dis_range})

                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())

    login_form = UserForm()
    return render(request, 'login.html', locals())


def index(request):
    sort = request.GET.get('sort')
    username = request.GET.get('username')
    purchased = order.objects.filter(order_uid=username)
    purchasedlist = list(purchased)
    namelist = []
    for item in purchasedlist:
        namelist.append(item.name)
    if sort:
        product_list = product.objects.order_by(sort).reverse()
    else:
        product_list = product.objects.order_by('add_date').reverse()
    paginator = Paginator(product_list, 3)
    page = request.GET.get('page')
    dis_range = range(1, paginator.num_pages + 1)
    try:
        products = paginator.page(page)  # contacts为Page对象！
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'products': products, 'purchased': namelist, 'username': username, 'dis_range': dis_range})


def makepay(request):
    name = ""
    price = ""
    order_uid = ""
    if request.method == "GET":
        name = request.GET.get("name")
        price = request.GET.get("price")
        order_uid = request.GET.get("username")

    def getUnique():
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
        randomNum = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)  # 16位
        return uniqueNum

    def makeSign(*p):
        return hashlib.md5(u''.join(p).encode('utf8')).hexdigest().lower()
    order_id = name + getUnique() # lesson52019062509491150
    pay_data = {
        'name': name, # product.name
        'pay_type': 'wechat',
        'price': price,
        'order_id': order_id, # name + purchase time
        'order_uid': order_uid, # username
        'notify_url': 'http://akiqiushui.com/handler/', #必填， 支付成功后回调地址
        'return_url': 'http://akiqiushui.com/success/' #选填， 支付城后前台跳转地址
    }
    pay_data['sign'] = makeSign(
        pay_data['name'],
        pay_data['pay_type'],
        pay_data['price'],
        pay_data['order_id'],
        pay_data['order_uid'],
        pay_data['notify_url'],
        pay_data['return_url'],
        '6d57e7c1d19a46418eb42c63dd699900'  #app secret, 这里需要修改为自己的
    )
    resp = requests.post('https://bufpay.com/api/pay/97008', data=pay_data)
    # redirect to payment page
    # def modify_text():
    #     with open('asmr/templates/pay.html', "r+") as f:
    #         f.seek(0)
    #         f.truncate()  # 清空文件
    #         f.write(resp.text)
    # modify_text()
    return HttpResponse(resp)
    # return render(request, 'pay.html')


@csrf_exempt
def handler(request):
    if request.method == 'POST':
        order_id = request.POST.get("order_id")
        order_uid = request.POST.get("order_uid")
        price = request.POST.get("price")
        pay_price = request.POST.get("pay_price")
        sign = request.POST.get("sign")
        print(order_id)
        print(order_uid)
        print(price)
        print(pay_price)
        print(sign)
        name = order_id[:-16]
        neworder = order(name=name, order_id=order_id, order_uid=order_uid, price=price, pay_price=price, sign=sign)
        neworder.save()
        # update visit times
        visited = product.objects.get(name=name)
        visited.vtimes += 1
        visited.save()
        return HttpResponse("received a post.")
    if request.method == 'GET':
        return HttpResponse("received a get.")
    return HttpResponse("received something else.")


def play(request):
    song = request.GET.get("song")
    img = request.GET.get("img")
    name = request.GET.get("name")
    price = request.GET.get("price")
    username = request.GET.get("username")
    if name:
        return render(request, 'play.html', {'song': song, 'img': img, 'name': name, 'price': price, 'username': username})
    return render(request, 'play.html', {'song': song, 'img': img, 'username': username})


@csrf_exempt
def success(request):
    return render(request, 'success.html')


def personal(request):
    username = request.GET.get("username")
    product_list = product.objects.order_by('add_date')
    # paginator = Paginator(product_list, 3)
    # page = request.GET.get('page')
    # try:
    #     products = paginator.page(page)  # contacts为Page对象！
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     products = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver last page of results.
    #     products = paginator.page(paginator.num_pages)
    purchased = order.objects.filter(order_uid=username)
    purchasedlist = list(purchased)
    namelist = []
    for item in purchasedlist:
        namelist.append(item.name)
    return render(request, 'personal.html', {'products': product_list, 'purchased': namelist, 'username': username})