from django.shortcuts import render
from blog.models import Articles ,Tags, ArticleTagMapping, Comments
from django.contrib import messages
from user.models import Users
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from .serializers import ArticleSerializer, TagSerializer , CommentSerializer
from django.views.decorators.csrf import csrf_exempt
import logging 
logger = logging.getLogger('django')

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
            logger.info("Article has been successfully added with data {}".format(data))
            return(JsonResponse(serializer.data, status = 201))
        logger.error("Article addition failed with data {}".format(data))
        return(HttpResponse(status= 400))
    return(HttpResponse(status = 404))

@csrf_exempt
def get_article_detail(request,pk):
    data = JSONParser().parse(request)
    try:
        article = Articles.objects.get(pk = int(pk), user_id = data["user_id"])
    except Articles.DoesNotExist:
        logger.error("Article is not mapped with the userID or article does not exist with article id {}, corrosponding data {}".format(pk,data))
        return(JsonResponse({"Error":"Article is not mapped with the userID or article Not foound"}, status= 404))
    if request.method == "GET":
        serializer = ArticleSerializer(article)
        return(JsonResponse(serializer.data, safe = False))
    elif request.method == "PUT":
        if article:
            serializer = ArticleSerializer(article, data = data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Article has been successfully updated with data {}".format(data))
                return(JsonResponse(serializer.data, status = 200))
            else:
                logger.error("Article updation failed for data {}".format(data))
                return(HttpResponse(status= 400))
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
        data["tag_name"] = data["tag_name"].lower().strip()
        serializer = TagSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Tag:{} has been successfully added".format(data["tag_name"]))
            return(JsonResponse(serializer.data, status = 201))
        logger.error("Adding tag: {} to the database failed".format(data["tag_name"]))
        return(JsonResponse({"Error":"Adding tags to the database Failed"},status= 400))

@csrf_exempt
def get_tag_detail(request,pk):
    try:
        tag = Tags.objects.get(pk = int(pk))
    except Tags.DoesNotExist:
        logger.error("Tag with tagID {} does not exist".format(pk))
        return JsonResponse({"Error":"Tag does not exist"},status = 404)
    if request.method == "GET":
        serializer = TagSerializer(tag)
        return(JsonResponse(serializer.data, safe = False))
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = TagSerializer(tag, data = data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Tag with details {} has been updated".format(data))
            return(JsonResponse(serializer.data, status =200))
        logger.error("Tag updation failed for tag data {}".format(data))
        return(JsonResponse({"Error":"Tag updation failed"},status= 400))
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
        try:
            article = Articles.objects.get(id = data["article_id"])
        except Articles.DoesNotExist:
            logger.error("Article with id {} does not exist for comment to be added".format(data["article_id"]))
            return(JsonResponse({"Error":"Article does not exist"}, status = 404))
        if article:
            serializer = CommentSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Comment has been successfully added with data {}".format(data))
                return(JsonResponse(serializer.data, status = 201))
            logger.error("Comment addition failed with data {}".format(data))
            return(JsonResponse({"Error":"Comment addition failed"},status= 400))

@csrf_exempt
def get_comment_detail(request,pk):
    try:
        comment = Comments.objects.get(pk = int(pk))
    except Comments.DoesNotExist:
        logger.error("Comment with id {} does not exist.".format(pk))
        return JsonResponse({"Error":"Comment with id {} does not exist.".format(pk)},status = 404)
    if request.method == "GET":
        serializer = CommentSerializer(tag)
        return(JsonResponse(serializer.data, safe = False))
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        try:
            comment = Comments.objects.get(pk = int(pk),article_id = data["article_id"])
        except Comments.DoesNotExist:
            logger.error("Comment with id {} does not exist or comment id and Article Id do not map".format(pk))
            return JsonResponse({"Error":"Comment with id {} does not exist or comment id and Article Id do not map".format(pk)},status = 404)
        serializer = CommentSerializer(comment, data = data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Comment has been updated for data {}".format(data))
            return(JsonResponse(serializer.data, status = 200))
        logger.error("Comment updation failed for data {}".format(data))
        return(JsonResponse({"Error":"Comment updation failed for data {}".format(data)},status= 400))
    elif request.method =="DELETE":
        comment.delete()
        logger.info("Comment has been updated for data {}".format(data))
        return HttpResponse(status = 204)

# Create your views here.
def create(request):
    if request.method == "POST":
        form = (request.POST)
        try:
            user = Users.objects.get(user_id=request.user.id)
        except Users.DoesNotExist:
            logger.info("User with user_id {} not found".format(request.user.id))
            messages.info(request,"User with user_id {} not found".format(request.user.id))
            return HttpResponseRedirect("/home")
        article = Articles(user = user, title= form["title"], body = form["body"], status = form['status'])
        article.save()
        if len(form["tags"]) > 0:
            tags = form["tags"].split(",")
            for tag in tags:
                tag = tag.strip().lower()
                query_set = Tags.objects.filter(tag_name= tag )
                if query_set.exists():
                    mapping = ArticleTagMapping(article_id = article.id, tag_id = query_set[0].id)
                else:
                    tag= Tags(tag_name = tag)
                    tag.save()
                    mapping = ArticleTagMapping(article_id = article.id, tag_id = tag.id)
                mapping.save()
        logger.info("Article has been created with title {}".format(form["title"]))
        messages.info(request,"New article has been created with title {}".format(form["title"]))
        return HttpResponseRedirect("/create")
    else:
        return(render(request,
                "createArticle.html")
            )

def view(request, slug):
    try:
        article = Articles.objects.get(slug = slug)
    except Articles.DoesNotExist:
        logger.info("Article does not exist")
        messages.info(request,"Article Does not exist ")
        return HttpResponseRedirect("/home")
    tags = ArticleTagMapping.objects.filter(article_id = article.id)
    tags = ArticleTagMapping.objects.select_related().filter(article__slug = slug)
    tag_names = []
    for tag in tags:
        tag_names.append(Tags.objects.get(id = tag.tag_id).tag_name)
    comments = Comments.objects.filter(article_id = article.id)[:5]
    return(render(request, "article_view.html", context = { "user_articles":article, "tags":tag_names, "comments":comments}))

def update(request, slug):
    try:
        article = Articles.objects.get(slug = slug)
    except Articles.DoesNotExist:
        logger.info("Article does not exist")
        messages.info(request,"Article Does not exist ")
        return HttpResponseRedirect("/home")
    tags = ArticleTagMapping.objects.filter(article_id = article.id)
    tag_names = []
    for tag in tags:
        tag_names.append(Tags.objects.get(id = tag.tag_id).tag_name)
    tag_names = ",".join(str(tag) for tag in tag_names)
    return(render(request, "update_article.html", context = { "user_articles":article, "tags":tag_names}))


def save(request, slug):
    if request.method == "POST":
        form = (request.POST)
        tags = form["tags"].split(",")
        try:
            id = Articles.objects.get(slug = slug).id
        except Articles.DoesNotExist:
            logger.info("Article does not exist")
            messages.info(request,"Article Does not exist")
            return HttpResponseRedirect("/home")
        ArticleTagMapping.objects.filter(article_id=id).delete()
        for tag in tags:
            if tag!='':
                query_set = Tags.objects.filter(tag_name= tag )
                if query_set.exists():
                    mapping = ArticleTagMapping(article_id = id, tag_id = query_set[0].id)
                else:
                    tag= Tags(tag_name = tag)
                    tag.save()
                    logger.info("New tag has been added with tag name {}".format(tag))
                    mapping = ArticleTagMapping(article_id = id, tag_id = tag.id)
                mapping.save()
        Articles.objects.select_related().filter(id  = id).update( title = form['title'], body = form['body'], status = form['status'])
        logger.info("Article has been updated with title {}".format(form["title"]))
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
        try:
            id = Articles.objects.get(slug = slug).id
        except Articles.DoesNotExist:
            logger.info("Article does not exist")
            messages.info(request,"Article Does not exist")
            return HttpResponseRedirect("/home")
        comment = Comments(comments = form['comment'], article_id= id)
        comment.save()
        logger.info("Comment has been successfully added to article with id {}".format(id))
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