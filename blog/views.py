from django.shortcuts import render
from blog.models import Articles ,Tags, ArticleTagMapping, Comments
from django.contrib import messages
from user.models import Users
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ArticleSerializer, TagSerializer , CommentSerializer
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import logging 

logger = logging.getLogger('django')

@csrf_exempt
@api_view(['POST','GET', ])
def get_articles(request):
    if request.method == "GET":
        page_size, page = entriesPerPage(request)
        articles = Articles.objects.all()
        paginator = Paginator(articles, page_size)
        articles = paginator.get_page(page)
        serializer = ArticleSerializer(articles, many = True)
        return(Response(serializer.data, status = status.HTTP_200_OK))
    elif request.method == "POST":
        article_data = JSONParser().parse(request)
        article_serializer = ArticleSerializer(data = article_data)
        if article_serializer.is_valid():
            article_serializer.save()
            logger.info("Article has been successfully added with data {}".format(article_data))
            return(Response(article_serializer.data, status = status.HTTP_201_CREATED))
        logger.error("Article addition failed with data {}".format(article_data))
        return(Response(article_serializer.errors,status= status.HTTP_400_BAD_REQUEST))
    return(Response({"error":"Invalid Request Type"},status = status.HTTP_400_BAD_REQUEST))

@csrf_exempt
@api_view(['GET','PUT','DELETE',])
def get_article_detail(request,pk):
    try:
        article = Articles.objects.get(pk = int(pk))
    except Articles.DoesNotExist:
        logger.error("Article does not exist with article id {}".format(pk))
        return(Response({"error":"Article  Not found"}, status= status.HTTP_404_NOT_FOUND))
    if request.method == "GET":
        article_serializer = ArticleSerializer(article)
        return(Response(article_serializer.data, status = status.HTTP_200_OK))
    elif request.method == "PUT":
        article_data = JSONParser().parse(request)
        try:
            article = Articles.objects.get(pk = int(pk), user_id = article_data["user_id"])
        except Articles.DoesNotExist:
            logger.error("Article is not mapped with the userID or article does not exist with article id {}, corrosponding data {}".format(pk,article_data))
            return(Response({"error":"Article is not mapped with the userID or article Not foound"}, status= status.HTTP_404_NOT_FOUND))
        if article:
            article_serializer = ArticleSerializer(article, data = article_data)
            if article_serializer.is_valid():
                article_serializer.save()
                logger.info("Article has been successfully updated with data {}".format(article_data))
                return(Response(article_serializer.data, status = status.HTTP_200_OK))
            else:
                logger.error("Article updation failed for data {}".format(article_data))
                return(Response({"error":"Article updation failed"}, status= status.HTTP_400_BAD_REQUEST))
    elif request.method =="DELETE":
        article_data = JSONParser().parse(request)
        try:
            article = Articles.objects.get(pk = int(pk), user_id = article_data["user_id"])
        except Articles.DoesNotExist:
            logger.error("Article is not mapped with the userID or article does not exist with article id {}, corrosponding data {}".format(pk,article_data))
            return(Response({"error":"Article is not mapped with the userID or article Not found"}, status= status.HTTP_404_NOT_FOUND))
        article.delete()
        return Response({"info":"Article has successfully been deleted"},status = status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['POST','GET', ])
def get_tags(request):
    if request.method == "GET":
        page_size, page = entriesPerPage(request)
        tags = Tags.objects.all()
        paginator = Paginator(tags, page_size)
        tags = paginator.get_page(page)
        tag_serializer = TagSerializer(tags, many = True)
        return(Response(tag_serializer.data, status = status.HTTP_200_OK))
    elif request.method == "POST":
        tag_data = JSONParser().parse(request)
        tag_data["tag_name"] = tag_data["tag_name"].lower().strip()
        tag_serializer = TagSerializer(data = tag_data)
        if tag_serializer.is_valid():
            tag_serializer.save()
            logger.info("Tag:{} has been successfully added".format(tag_data["tag_name"]))
            return(Response(tag_serializer.data, status = status.HTTP_201_CREATED))
        logger.error("Adding tag: {} to the database failed".format(tag_data["tag_name"]))
        return(Response({"error":"Adding tags to the database Failed"}, status= status.HTTP_400_BAD_REQUEST))

@csrf_exempt
@api_view(['GET','PUT','DELETE', ])
def get_tag_detail(request,pk):
    try:
        tag = Tags.objects.get(pk = int(pk))
    except Tags.DoesNotExist:
        logger.error("Tag with tagID {} does not exist".format(pk))
        return Response({"error":"Tag does not exist"},status = status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        tag_serializer = TagSerializer(tag)
        return(Response(tag_serializer.data, status = status.HTTP_200_OK))
    elif request.method == "PUT":
        tag_data = JSONParser().parse(request)
        tag_serializer = TagSerializer(tag, data = tag_data)
        if tag_serializer.is_valid():
            tag_serializer.save()
            logger.info("Tag with details {} has been updated".format(tag_data))
            return(Response(tag_serializer.data, status = status.HTTP_200_OK))
        logger.error("Tag updation failed for tag data {}".format(tag_data))
        return(Response({"error":"Tag updation failed"},status = status.HTTP_400_BAD_REQUEST))
    elif request.method =="DELETE":
        tag.delete()
        return Response({"info":"Tag has been added successfully"}, status = status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['POST','GET',])
def get_comments(request):
    if request.method == "GET":
        page_size, page = entriesPerPage(request)
        comments = Comments.objects.all()
        paginator = Paginator(comments, page_size)
        comments = paginator.get_page(page)
        comment_serializer = CommentSerializer(comments, many = True)
        return(Response(comment_serializer.data, status = status.HTTP_200_OK))
    elif request.method == "POST":
        comment_data = JSONParser().parse(request)
        try:
            article = Articles.objects.get(id = comment_data["article_id"])
        except Articles.DoesNotExist:
            logger.error("Article with id {} does not exist for comment to be added".format(comment_data["article_id"]))
            return(Response({"error":"Article does not exist"}, status = status.HTTP_404_NOT_FOUND))
        if article:
            comment_serializer = CommentSerializer(data = comment_data)
            if comment_serializer.is_valid():
                comment_serializer.save()
                logger.info("Comment has been successfully added with data {}".format(comment_data))
                return(Response(comment_serializer.data, status = status.HTTP_201_CREATED))
            logger.error("Comment addition failed with data {}".format(comment_data))
            return(Response({"error":"Comment addition failed"},status = status.HTTP_400_BAD_REQUEST))

@csrf_exempt
@api_view(['GET','PUT','DELETE', ])
def get_comment_detail(request,pk):
    try:
        comment = Comments.objects.get(pk = int(pk))
    except Comments.DoesNotExist:
        logger.error("Comment with id {} does not exist.".format(pk))
        return Response({"error":"Comment with id {} does not exist.".format(pk)}, status = status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        comment_serializer = CommentSerializer(comment)
        return(Response(comment_serializer.data, status = status.HTTP_200_OK))
    elif request.method == "PUT":
        comment_data = JSONParser().parse(request)
        try:
            comment = Comments.objects.get(pk = int(pk),article_id = comment_data["article_id"])
        except Comments.DoesNotExist:
            logger.error("Comment with id {} does not exist or comment id and Article Id do not map".format(pk))
            return Response({"error":"Comment with id {} does not exist or comment id and Article Id do not map".format(pk)},status = status.HTTP_404_NOT_FOUND)
        comment_serializer = CommentSerializer(comment, data = comment_data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            logger.info("Comment has been updated for data {}".format(comment_data))
            return(Response(comment_serializer.data, status = status.HTTP_200_OK))
        logger.error("Comment updation failed for data {}".format(comment_data))
        return(Response({"Error":"Comment updation failed for data {}".format(comment_data)}, status= status.HTTP_400_BAD_REQUEST))
    elif request.method =="DELETE":
        comment_data = JSONParser().parse(request)
        comment.delete()
        logger.info("Comment has been deleted for data {}".format(comment_data))
        return Response({"info":"Comment has been deleted"}, status = status.HTTP_204_NO_CONTENT)

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
    page = 1
    if "page_size" in params:
        page_size = int(params["page_size"])
    if "page" in params:
        page = int(params["page"])
    return(page_size,page)