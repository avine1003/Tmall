import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum
from django.forms import model_to_dict

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import BannerImg, Category, Product, Categorysub, Productimage, Property, Propertyvalue


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
        banners = [model_to_dict(banner) for banner in BannerImg.objects.all()]
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


def get_shop_detail(request):
    result = {}
    try:
        pid = request.GET.get('pid')
        product = Product.objects.get(id=pid)
        # 获取商品的图片对象
        imgs = product.productimage_set.filter(type='type_single')
        # 获取商品销量
        sale_count = product.orderitem_set.all().aggregate(Sum('number')).get('number__sum')
        # 获取评论数量
        review_count = product.review_set.count()

        # 获取评论内容对象
        review_contents = product.review_set.all()
        review_list = []
        for content in review_contents:
            content_dict = model_to_dict(content)
            content_dict['createdate'] = datetime.datetime.strftime(content_dict['createdate'], '%Y-%m-%d %H:%M:%S')
            review_list.append(content_dict)

        # 获取商品的属性
        # [{'name':"品牌", 'value':'Hisense/海信'}, {'name':'型号', 'value':'123'}]
        property_list = Property.objects.filter(cid=product.cid)
        propertys = []
        for property in property_list:
            property_dic = model_to_dict(property)
            # 获取属性值表匹配的对象
            p = property.propertyvalue_set.filter(ptid=property.id, pid=product.id)
            property_dic['value'] = model_to_dict(p[0])['value']
            propertys.append(property_dic)

        product = model_to_dict(product)
        product['createdate'] = datetime.datetime.strftime(product['createdate'], '%Y-%m-%d %H:%M:%S')
        # 将图片属性加到商品中
        product['imgs'] = [model_to_dict(img) for img in imgs]
        product['sale_count'] = sale_count
        product['review_count'] = review_count
        product['property'] = propertys
        product['review_content'] = review_list

        result.update(state=200, msg='success', data=product)
    except:
        pass
    return HttpResponse(json.dumps(result), content_type='application/json')

