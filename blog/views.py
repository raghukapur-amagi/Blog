from django.shortcuts import render
from blog.models import Articles ,Tags, ArticleTagMapping, Comments
from django.contrib import messages
from user.models import Users
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
import random
import string

# Create your views here.
def create(request):
    if request.method == "POST":
        form = (request.POST)
        check = Users.objects.get(user_id=request.user.id)
        slug = get_slug()
        article = Articles(user = check, title= form["title"], body = form["body"], status = form['status'], slug = slug)
        article.save()
        tags = form["tags"].split(",")
        if tags[0] != '':
            for i in tags:
                query_set = Tags.objects.filter(tag_name= i )
                if query_set.exists():
                    mapping = ArticleTagMapping(article_id = article.id, tag_id = query_set[0].id)
                else:
                    tag= Tags(tag_name = i)
                    tag.save()
                    mapping = ArticleTagMapping(article_id = article.id, tag_id = tag.id)
                mapping.save()
        messages.info(request,"New article has been created with title {}".format(form["title"]))
        return HttpResponseRedirect('/home')
    else:
        return(render(request,
                "createArticle.html",
                context={"check":"check"})
            )

def view(request, title,slug):
    article = Articles.objects.filter(title = title, slug = slug)
    tags = ArticleTagMapping.objects.filter(article_id = article[0].id)
    tag_names = []
    for i in tags:
        tag_names.append(Tags.objects.filter(id = i.tag_id)[0].tag_name)
    comments = Comments.objects.filter(article_id = article[0].id)[:5]
    return(render(request, "article_view.html", context = { "user_articles":article, "tags":tag_names, "comments":comments}))

def update(request, title,slug):
    article = Articles.objects.filter(title = title, slug = slug)
    tags = ArticleTagMapping.objects.filter(article_id = article[0].id)
    tag_names = ""
    for i in tags:
        tag_names = tag_names +Tags.objects.filter(id = i.tag_id)[0].tag_name +","
    return(render(request, "update_article.html", context = { "user_articles":article, "tags":tag_names}))


def save(request, title,slug):
    if request.method == "POST":
        form = (request.POST)
        tags = form["tags"].split(",")
        id = Articles.objects.filter(title = title, slug = slug)[0].id
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
        return(HttpResponseRedirect('/home'))

def search(request):
    if request.method == "POST":
        form = (request.POST)
        tag = form['Search By Tag']
        title = form['Search By Title']
        print(Articles.objects.filter(title=title, user_id = not None))
        article_search = []
        if request.user.is_authenticated:
            user_id = Users.objects.get(user_id=request.user.id)
            if  title:
                articles = Articles.objects.filter(title=title, user_id=user_id)
                if articles.exists():
                    article_search = articles
            if  tag:
                tags = Tags.objects.filter(tag_name=tag)
                if tags.exists(): 
                    article_tag_ids  = ArticleTagMapping.objects.filter(tag_id = tags[0].id)
                    if article_tag_ids.exists():
                        if article_search:
                            article_search = article_search | Articles.objects.filter(id = article_tag_ids[0].article_id,user_id = user_id)
                        else:
                            article_search = Articles.objects.filter(id = article_tag_ids[0].article_id,user_id = user_id)
                        for ids in range(1,len(article_tag_ids)):
                            article_search = article_search | Articles.objects.filter(id = article_tag_ids[ids].article_id, user_id=user_id)
        else:
            if  title:
                articles = Articles.objects.filter(title=title)[:5]
                if articles.exists():
                    article_search = articles
            if  tag:
                tags = Tags.objects.filter(tag_name=tag)
                if tags.exists(): 
                    article_tag_ids  = ArticleTagMapping.objects.filter(tag_id = tags[0].id)
                    if article_tag_ids.exists():
                        if article_search:
                            article_search = article_search | Articles.objects.filter(id = article_tag_ids[0].article_id)
                        else:
                            article_search = Articles.objects.filter(id = article_tag_ids[0].article_id)
                        for ids in range(1,len(article_tag_ids)):
                            article_search = article_search | Articles.objects.filter(id = article_tag_ids[ids].article_id)
            """
            if username:
                user_id = User.objects.get(username=username).pk
                user_id = Users.objects.get(user_id = user_id).pk
                article = Articles.objects.filter(user_id = user_id)
                print(article)
                if article.exists():
                    if article_search:
                        article_search = article_search |  Articles.objects.filter(id = article[0].id)
                    else:
                        article_search = Articles.objects.filter(id = article[0].id)
                    for ids in range(1,len(article)):
                        article_search = article_search |  Articles.objects.filter(id = article[ids].id)
            """
        print(article_search)
        return(render(request, "search_view.html", context = { "article_search":article_search}))
        


def comment(request, title,slug):
    if request.method == "POST":
        form = (request.POST)
        print(form)
        id = Articles.objects.filter(title = title, slug = slug)[0].id
        comment = Comments(comments = form['comment'], article_id= id)
        print(comment)
        comment.save()
        messages.info(request,"Your comment has been successfully added")
        return(HttpResponseRedirect('/home'))


def get_slug():
    letters = string.ascii_lowercase
    return(''.join(random.choice(letters) for i in range(5)))