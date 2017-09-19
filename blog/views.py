from django.shortcuts import render,HttpResponse,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog import models
from django.contrib import auth
from Blog_system import settings
from django.db.models import Avg,Sum,Max,Min,Count
from blog import forms
from django.db.models import F,Q
import json
from blog.models import Article,Tag,Blog,UserInfo,Category,UserFans,ArticleDetail,ArticleUpDown,\
    Comment,Article2Tag
from bs4 import BeautifulSoup
# Create your views here.

def func_class(request):
    '''
    返回主页功能种类
    :param request: 
    :return: 
    '''

    return {"func":settings.FUNCTION}

def index(request,**kwargs):
    '''
    公共首页
    :param request: 
    :param kwargs: 
    :return: 
    '''

    type_choices = models.Article.type_choices

    current_type_choices_id = int(kwargs.get("article_type_id",0))

    article_list=models.Article.objects.all()

    p_obj = Paginator(article_list, 6)

    page_num = request.GET.get('page')

    try:
        article_list = p_obj.page(page_num)
    except EmptyPage:  # 如果输入的值超出现有页数，就显示最后一页
        article_list = p_obj.page(p_obj.num_pages)
    except PageNotAnInteger:  # 如果输入的页数不合法，就显示第一页
        article_list = p_obj.page(1)

    return render(request,'index.html',{"type_choices":type_choices,
                                        "current_type_choices_id":current_type_choices_id,
                                        "article_list":article_list,
                                        "request":request,"p_obj":p_obj,"page_num":page_num})

def userindex(request,user_site,**kwargs):
    '''
    用户首页
    :param request: 
    :param user_site: 
    :param kwargs: 
    :return: 
    '''

    user_obj = UserInfo.objects.filter(username=user_site).first()

    if not user_obj:
        return render(request,"NotFound.html")

    currentBlog = Blog.objects.filter(user=user_obj).first()

    article_list = Article.objects.filter(blog=currentBlog)

    category_list=Article.objects.filter(blog=currentBlog).values_list("category__title","category__nid").annotate(Count("title"))

    tag_list=Article.objects.filter(blog=currentBlog).values_list("tags__title","tags__nid").annotate(Count("title"))

    time_list = Article.objects.filter(blog=currentBlog).values_list("create_time")   #所有属于当前博客文章的创建时间

    fans_num = UserFans.objects.filter(user=user_obj).count()

    follow_num = UserFans.objects.filter(follower=user_obj).count()

    l=[]
    for i in time_list:
        time=i[0].strftime("%Y-%m-%d")

        if time not in l:
            l.append(time)

    current_time_list=[]   #拿到当前的时间列表和对应的文章个数
    for j in l:
        temp=[]
        article_count=Article.objects.filter(blog=currentBlog,create_time__contains=j).count()
        temp.append(j)
        temp.append(article_count)
        current_time_list.append(temp)

    if kwargs.get("condition"):  #判断用户有没有点击分类列表，如果有，根据用户点击的按钮返回相应的文章列表

        con=kwargs.get("condition")

        if con == "category":

            article_list=Article.objects.filter(blog=currentBlog,category_id=kwargs.get("para"))

        elif con == "tag":

            article_list = Article.objects.filter(blog=currentBlog,tags=kwargs.get("para"))

        elif con == "date":

            article_list = Article.objects.filter(blog=currentBlog,create_time__contains=kwargs.get("para"))

    return render(request,"userblog.html",{"user_obj":user_obj,"article_list":article_list,"category_list":category_list,
                                           "tag_list":tag_list,"current_time_list":current_time_list,"fans_num":fans_num,
                                           "follow_num":follow_num,"request":request})

def article_content(request,user_site,article_nid):
    '''
    文章内容页面
    :param request: 
    :param user_site: 
    :param article_nid: 
    :return: 
    '''
    user_obj = UserInfo.objects.filter(username=user_site).first()

    article = Article.objects.filter(nid=article_nid).first()

    article_detail = ArticleDetail.objects.filter(article=article).first()

    if not user_obj:
        return render(request, "NotFound.html")

    currentBlog = Blog.objects.filter(user=user_obj).first()

    category_list = Article.objects.filter(blog=currentBlog).values_list("category__title","category__nid").annotate(Count("title"))

    tag_list = Article.objects.filter(blog=currentBlog).values_list("tags__title","tags__nid").annotate(Count("title"))

    time_list = Article.objects.filter(blog=currentBlog).values_list("create_time")

    fans_num = UserFans.objects.filter(user=user_obj).count()

    follow_num = UserFans.objects.filter(follower=user_obj).count()

    comment_list = Comment.objects.filter(article=article)

    l = []
    for i in time_list:
        time = i[0].strftime("%Y-%m-%d")

        if time not in l:
            l.append(time)

    current_time_list = []
    for j in l:
        temp = []
        article_count = Article.objects.filter(blog=currentBlog).filter(create_time__contains=j).count()
        temp.append(j)
        temp.append(article_count)
        current_time_list.append(temp)

    return render(request, "article_content.html",{"user_obj": user_obj, "category_list": category_list,
                   "tag_list": tag_list, "current_time_list": current_time_list, "fans_num": fans_num,
                   "follow_num": follow_num,"article":article,"article_detail":article_detail,
                    "request":request,"comment_list":comment_list})

def log_in(request):

    if request.is_ajax():
        username = request.POST.get("username")
        password = request.POST.get("password")
        valid_code = request.POST.get("valid_code")

        ajax_response = {"user": None, "error_message": ''}

        user = auth.authenticate(username=username,password=password)

        if valid_code.upper() == request.session.get("valid_code").upper():
            if user:
                ajax_response["user"]=username
                auth.login(request,user)
            else:
                ajax_response["error_message"]='用户名或密码错误！'
        else:
            ajax_response["error_message"] = '验证码输入错误！'

        return HttpResponse(json.dumps(ajax_response))

    return render(request,"login.html")

def log_out(request):
    '''
    注销
    :param request: 
    :return: 
    '''
    auth.logout(request)

    return redirect("/index/")

def valid_code(request):
    '''
    验证码函数
    :param request: 
    :return: 
    '''

    from PIL import Image,ImageDraw,ImageFont
    from io import BytesIO
    import random

    #因为验证码只用一次，所以我们在内存中直接创建和调用就好
    f=BytesIO()
    img = Image.new(mode='RGB',size=(120,30),color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    draw = ImageDraw.Draw(img,mode='RGB')

    font = ImageFont.truetype("blog/static/bootstrap/fonts/kumo.ttf",28)

    code_list = []
    for i in range(5):
        char = random.choice([chr(random.randint(65,90)),str(random.randint(1,9))])
        code_list.append(char)
        draw.text([i * 24,0],char,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),
                  font=font)

    img.save(f,"png")

    valid_code = ''.join(code_list)

    request.session["valid_code"]=valid_code

    return HttpResponse(f.getvalue())

def register(request):
    '''
    注册视图
    :param request: 
    :return: 
    '''

    if request.method=="POST":

        ajax_response = {"status": False, "error_msg": ""}
        form_obj = forms.RegisterForm(request,request.POST)

        if form_obj.is_valid():
            file_obj = request.FILES["img"]
            ajax_response["status"]=True
            models.UserInfo.objects.create_user(username=request.POST.get("username"),
                                                password=request.POST.get("password"),
                                                email=request.POST.get("email"),
                                                avatar=file_obj)
        else:
            errors = form_obj.errors
            ajax_response["error_msg"]=errors
        return HttpResponse(json.dumps(ajax_response))

    form_obj=forms.RegisterForm(request)
    return render(request,"register.html",{"form_obj":form_obj})

def poll(request):

    response_msg={"flag":1,"error_msg":""}

    article_nid = request.POST.get("article_nid")

    article_obj=Article.objects.filter(nid=article_nid).first()

    if ArticleUpDown.objects.filter(article=article_obj,user=request.user):
        response_msg["error_msg"]="您已经点过赞了"
        response_msg["flag"] = 0

    elif article_obj.blog.user == request.user:
        response_msg["error_msg"] = "不能给自己点赞哦！"
        response_msg["flag"] = 0

    else:

        Article.objects.filter(nid=article_nid).update(up_count=F("up_count")+1)

        ArticleUpDown.objects.create(user=request.user,article_id=article_nid)

    return HttpResponse(json.dumps(response_msg))

def comment(request):
    '''
    评论视图
    :param request: 
    :return: 
    '''

    user_obj = request.user
    article_nid = request.POST.get("article_nid")
    comment_content = request.POST.get("comment_content")

    #如果有父ID,就是子评论，如果没有，就是文章评论
    if request.POST.get("parent_comment_id"):
        parent_comment_id=int(request.POST.get("parent_comment_id"))
        comment_obj = Comment.objects.create(user=user_obj, article_id=article_nid, content=comment_content,
                                             parent_id=parent_comment_id)
    else:
        comment_obj=Comment.objects.create(user=user_obj,article_id=article_nid,content=comment_content)

    Article.objects.filter(nid=article_nid).update(comment_count=F("comment_count")+1)

    ajax_response = {"comment_create_time":str(comment_obj.create_time)[:16],"comment_up_count":comment_obj.up_count,
                     "comment_nid":comment_obj.nid}

    return HttpResponse(json.dumps(ajax_response))

def add_article(request,user_site):
    user_obj = UserInfo.objects.filter(username=user_site).first()

    currentBlog = Blog.objects.filter(user=user_obj).first()

    category_list=Category.objects.filter(blog=currentBlog)

    tag_list=Tag.objects.filter(blog=currentBlog)

    type_choices = models.Article.type_choices

    if request.method == "POST":
        print(request.POST)

        title = request.POST.get("article_title")
        desc = request.POST.get("article_desc")
        content = request.POST.get("article_content")
        category_nid = request.POST.get("category_nid")
        tags_nid = request.POST.get("tags_nid")
        type_id = request.POST.get("type_id")

        tag_obj_list = []
        for tag_nid in tags_nid:
            tag_obj=Tag.objects.filter(nid=tag_nid).first()
            tag_obj_list.append(tag_obj)

        #处理非法标签
        error_label_list = ["script","link"]

        content_BS = BeautifulSoup(content,"html.parser")

        for label in content_BS.find_all():

            if label.name in error_label_list:
                label.decompose()

        # 添加文章
        article_obj=Article.objects.create(title=title,desc=desc,article_type_id=type_id,
                                           category_id=category_nid,blog=currentBlog)
        ArticleDetail.objects.create(article=article_obj,content=content)

        for tag_obj in tag_obj_list:
            Article2Tag.objects.create(tag=tag_obj,article=article_obj)

        return redirect("blog/"+user_site+"/article/back_stage")

    return render(request,"addarticle.html",{"category_list":category_list,"tag_list":tag_list,
                                             "type_choices":type_choices,"request":request})

def back_stage(request,user_site):

    user_obj = UserInfo.objects.filter(username=user_site).first()

    currentBlog = Blog.objects.filter(user=user_obj).first()

    article_list = Article.objects.filter(blog=currentBlog)

    p_obj = Paginator(article_list, 6)

    page_num = request.GET.get('page')

    try:
        article_list = p_obj.page(page_num)
    except EmptyPage:  # 如果输入的值超出现有页数，就显示最后一页
        article_list = p_obj.page(p_obj.num_pages)
    except PageNotAnInteger:  # 如果输入的页数不合法，就显示第一页
        article_list = p_obj.page(1)


    return render(request,"back_stage.html",{"article_list":article_list,"p_obj": p_obj,
                                             "page_num": page_num,"request":request})

def delete_article(request):

    article_nid = request.POST.get("article_nid")

    Article.objects.filter(nid=article_nid).delete()

    return HttpResponse("删除成功")

def upload_file(request):

    file_obj = request.FILES.get("imgFile")

    filename = file_obj.name

    with open('blog/media/upload/put_img/'+filename,'wb') as f:

        for chunk in file_obj.chunks():
            f.write(chunk)

    response_msg={
        "error":0,
        "url":'/media/upload/put_img/'+filename
        #文件路径传到前端之后，前端的富文本编辑框会拿到这个路径自动预览
    }

    return HttpResponse(json.dumps(response_msg))

def article_detail2(request,user_site,article_nid):

    if request.is_ajax():

        comment_list = Comment.objects.filter(article_id=article_nid).values("nid","create_time","content","parent_id",
                                                                             "up_count","user__avatar","user__username")

        print("comment_list+++++++",comment_list)

        import collections

        comment_dict = collections.OrderedDict()

        for comment in comment_list:
            comment["create_time"]=comment["create_time"].strftime("%Y-%m-%d %H:%M")
            comment["user__avatar"]='/media/'+comment["user__avatar"]
            comment["children_comments"]=[]
            comment_dict[comment["nid"]] = comment

        print("comment_dict=======================",comment_dict)

        root_comment = []

        for comment in comment_dict:
            if comment_dict[comment]["parent_id"]:
                pid = comment_dict[comment]["parent_id"]
                comment_dict[pid]["children_comments"].append(comment_dict[comment])
            else:
                root_comment.append(comment_dict[comment])
        print("root_comment+++++++++++++++++",root_comment)

        return HttpResponse(json.dumps(root_comment))

    user_obj = UserInfo.objects.filter(username=user_site).first()

    article = Article.objects.filter(nid=article_nid).first()

    article_detail = ArticleDetail.objects.filter(article=article).first()

    if not user_obj:
        return render(request, "NotFound.html")

    currentBlog = Blog.objects.filter(user=user_obj).first()

    category_list = Article.objects.filter(blog=currentBlog).values_list("category__title","category__nid").annotate(Count("title"))

    tag_list = Article.objects.filter(blog=currentBlog).values_list("tags__title","tags__nid").annotate(Count("title"))

    time_list = Article.objects.filter(blog=currentBlog).values_list("create_time")

    fans_num = UserFans.objects.filter(user=user_obj).count()

    follow_num = UserFans.objects.filter(follower=user_obj).count()

    l = []
    for i in time_list:
        time = i[0].strftime("%Y-%m-%d")

        if time not in l:
            l.append(time)

    current_time_list = []
    for j in l:
        temp = []
        article_count = Article.objects.filter(blog=currentBlog).filter(create_time__contains=j).count()
        temp.append(j)
        temp.append(article_count)
        current_time_list.append(temp)


    return render(request,"article_detail2.html",locals())


