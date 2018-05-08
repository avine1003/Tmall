import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import BannerImg, Category, Product, Categorysub, Productimage

#
# def get_cate(request):
#     #导航
#     cate_list = Category.objects.all()
#     for cate in cate_list:
#         cate_sub_list = Categorysub.objects.filter(cid=cate.id)
#         cate.cate_sub_list = cate_sub_list
#
#     banner_list = BannerImg.objects.all()
#     context = {
#         'cate_list': cate_list,
#         'banner_list': banner_list,
#     }
#     return render(request, 'home.html', context)


def create_img(request):
    # banner_img = BannerImg.objects.create()
    banner_list = []
    path = '/static/img/banner/'
    for i in range(5):
        banner_img = BannerImg(img_addr= path + str(i+1) + '.jpg')
        banner_list.append(banner_img)
    BannerImg.objects.bulk_create(banner_list)
    return render(request, 'index.html')


# @login_required
def search_shop(request):
    result = {}
    try:
        keywords = request.GET.get('key')
        products = Product.objects.filter(name__contains=keywords)
        li = []
        for product in products:
            product_dic = model_to_dict(product)
            product_dic['img'] = [model_to_dict(img) for img in product.productimage_set.all()]
            li.append(product_dic)
        result.update(state=200, msg='成功', data=li)
    except BaseException as e:
        result.update(state=-1, msg='失败')
    return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder), content_type='application/json')
    # keywords = request.GET.get('key')
    # if keywords:
    #     product_list = Product.objects.filter(name__contains=keywords)
    #     for product in product_list:
    #         if product.productimage_set.all():
    #             product.img = str(product.productimage_set.all().first().id)
    #             # product.save()
        # product_list = Product.objects.filter(name__contains=keywords)
    # else:
    #     product_list = Product.objects.all()
    # data = serializers.serialize('json', product_list)
    # return HttpResponse(data, content_type="Application/json")
    # # 将query_set 对象序列化成json数据


def index(request):
    return render(request, 'index.html')


def get_category_data(request):
    """
    获取分类菜单的数据
    :param request:
    :return:
    """
    result = {}
    try:
        cate_list = Category.objects.all()
        banners =[model_to_dict(banner) for banner in BannerImg.objects.all()]
        result['banners'] = banners

        li = []
        for cate in cate_list:
            cate_dic = model_to_dict(cate)
            sub_list = [model_to_dict(sub) for sub in cate.categorysub_set.all()]
            cate_dic['subs'] = sub_list
            li.append(cate_dic)
        result.update(state=200, msg='success', data=li)
    except:
        result.update(state=400, msg='查询失败')

    return HttpResponse(json.dumps(result), content_type='application/json')


def get_shop_data(request):
    result = {}
    li = []

    try:
        cates = Category.objects.all()
        for cate in cates:
            products = cate.product_set.all()
            product_list = []
            for product in products:
                product_dic = model_to_dict(product)
                product_dic['createdate'] = datetime.datetime.strftime(product_dic['createdate'], '%Y-%m-%d %H:%M:%S')
                product_dic['img'] = [model_to_dict(img) for img in product.productimage_set.all()]
                product_list.append(product_dic)
            cate_dic = model_to_dict(cate)
            cate_dic['products'] = product_list
            li.append(cate_dic)
        result.update(state=200, msg='success', data=li)
    except:
        result.update(state=400, msg='查询失败')
    return HttpResponse(json.dumps(result), content_type='application/json')
