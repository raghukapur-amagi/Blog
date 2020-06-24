from django.shortcuts import render
from blog.models import Articles ,Tags, ArticleTagMapping, Comments
from django.contrib import messages
from user.models import Users
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from .serializers import ArticleSerializer, TagSerializer , CommentSerializer
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_articles(request):
    if request.method == "GET":
        start, end = entriesPerPage(request)
        articles = Articles.objects.filter()[start:end]
        serializer = ArticleSerializer(articles, many = True)
        return(JsonResponse(serializer.data, safe = False))
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return(JsonResponse(serializer.data, status = 201))
        return(JsonResponse(serializer.errors, status = 400))

@csrf_exempt
def get_article_detail(request,pk):
    try:
        article = Articles.objects.get(pk = int(pk))
    except Articles.DoesNotExist:
        return HttpResponse(status = 404)

    if request.method == "GET":
        serializer = ArticleSerializer(article)
        return(JsonResponse(serializer.data, safe = False))
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data = data)
        if serializer.is_valid():
            serializer.save()
            return(JsonResponse(serializer.data))
        return(JsonResponse(serializer.errors, status = 400))
    elif request.method =="DELETE":
        article.delete()
        return HttpResponse(status = 204)

@csrf_exempt
def get_tags(request):
    if request.method == "GET":
        start, end = entriesPerPage(request)
        tags = Tags.objects.filter()[start:end]
        serializer = TagSerializer(tags, many = True)
        return(JsonResponse(serializer.data, safe = False))
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = TagSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return(JsonResponse(serializer.data, status = 201))
        return(JsonResponse(serializer.errors, status = 400))

@csrf_exempt
def get_tag_detail(request,pk):
    try:
        tag = Tags.objects.get(pk = int(pk))
    except Tags.DoesNotExist:
        return HttpResponse(status = 404)
    if request.method == "GET":
        serializer = TagSerializer(tag)
        return(JsonResponse(serializer.data, safe = False))
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = TagSerializer(tag, data = data)
        if serializer.is_valid():
            serializer.save()
            return(JsonResponse(serializer.data))
        return(JsonResponse(serializer.errors, status = 400))
    elif request.method =="DELETE":
        tag.delete()
        return HttpResponse(status = 204)

@csrf_exempt
def get_comments(request):
    if request.method == "GET":
        start, end = entriesPerPage(request)
        comments = Comments.objects.filter()[start:end]
        serializer = CommentSerializer(comments, many = True)
        return(JsonResponse(serializer.data, safe = False))
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return(JsonResponse(serializer.data, status = 201))
        return(JsonResponse(serializer.errors, status = 400))

@csrf_exempt
def get_comment_detail(request,pk):
    try:
        comment = Comments.objects.get(pk = int(pk))
    except Comments.DoesNotExist:
        return HttpResponse(status = 404)
    if request.method == "GET":
        serializer = CommentSerializer(tag)
        return(JsonResponse(serializer.data, safe = False))
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = CommentSerializer(comment, data = data)
        if serializer.is_valid():
            serializer.save()
            return(JsonResponse(serializer.data))
        return(JsonResponse(serializer.errors, status = 400))
    elif request.method =="DELETE":
        comment.delete()
        return HttpResponse(status = 204)

# Create your views here.
def create(request):
    if request.method == "POST":
        form = (request.POST)
        user = Users.objects.get(user_id=request.user.id)
        article = Articles(user = user, title= form["title"], body = form["body"], status = form['status'])
        article.save()
        if len(form["tags"]) > 0:
            tags = form["tags"].split(",")
            for tag in tags:
                query_set = Tags.objects.filter(tag_name= tag )
                if query_set.exists():
                    mapping = ArticleTagMapping(article_id = article.id, tag_id = query_set[0].id)
                else:
                    tag= Tags(tag_name = tag)
                    tag.save()
                    mapping = ArticleTagMapping(article_id = article.id, tag_id = tag.id)
                mapping.save()
        messages.info(request,"New article has been created with title {}".format(form["title"]))
        return HttpResponseRedirect("/create")
    else:
        return(render(request,
                "createArticle.html")
            )

def view(request, slug):
    article = Articles.objects.get(slug = slug)
    tags = ArticleTagMapping.objects.filter(article_id = article.id)
    tags = ArticleTagMapping.objects.select_related().filter(article__slug = slug)
    tag_names = []
    for tag in tags:
        tag_names.append(Tags.objects.get(id = tag.tag_id).tag_name)
    comments = Comments.objects.filter(article_id = article.id)[:5]
    return(render(request, "article_view.html", context = { "user_articles":article, "tags":tag_names, "comments":comments}))

def update(request, slug):
    article = Articles.objects.get(slug = slug)
    tags = ArticleTagMapping.objects.filter(article_id = article.id)
    tag_names = ""
    for i in tags:
        tag_names = tag_names +Tags.objects.get(id = i.tag_id).tag_name +","
    return(render(request, "update_article.html", context = { "user_articles":article, "tags":tag_names}))


def save(request, slug):
    if request.method == "POST":
        form = (request.POST)
        tags = form["tags"].split(",")
        id = Articles.objects.get(slug = slug).id
        ArticleTagMapping.objects.filter(article_id=id).delete()
        for i in tags:
            if i!='':
                query_set = Tags.objects.filter(tag_name= i )
                if query_set.exists():
                    mapping = ArticleTagMapping(article_id = id, tag_id = query_set[0].id)
                else:
                    tag= Tags(tag_name = i)
                    tag.save()
                    mapping = ArticleTagMapping(article_id = id, tag_id = tag.id)
                mapping.save()
        Articles.objects.select_related().filter(id  = id).update( title = form['title'], body = form['body'], status = form['status'])
        messages.info(request,"Article has been updated with title {}".format(form["title"]))
        prev = request.POST.get('prev', '/')
        return(HttpResponseRedirect(prev))

def search(request):
    if request.method == "POST":
        form = (request.POST)
        search = form['search']
        article_search = []
        articles = Articles.objects.filter(title = search)
        if articles.exists():
                article_search = articles
        try:
            tag = Tags.objects.get(tag_name = search).id
        except Tags.DoesNotExist:
            tag = None
        if tag is not None:
            articles = Articles.objects.select_related().filter(articletagmapping__tag_id = tag)
            if articles.exists():
                if article_search:
                    article_search = article_search | articles
                else:
                    article_search = articles
        if request.user.is_authenticated:
            if article_search:
                article_search = article_search.filter(user_id = Users.objects.get(user_id=request.user.id))
        return(render(request, "search_view.html", context = { "article_search":article_search}))


def comment(request, slug):
    if request.method == "POST":
        form = (request.POST)
        id = Articles.objects.get(slug = slug).id
        comment = Comments(comments = form['comment'], article_id= id)
        comment.save()
        messages.info(request,"Your comment has been successfully added")
        prev = request.POST.get('prev', '/')
        return(HttpResponseRedirect(prev))


def entriesPerPage(request):
    params = request.GET
    page_size = 20
    start_page = 1
    if "page_size" in params:
        page_size = int(params["page_size"])
    if "start_page" in params:
        start_page = int(params["start_page"])
    start = (start_page-1)*page_size
    end =  (start_page)*page_size
    return(start, end)