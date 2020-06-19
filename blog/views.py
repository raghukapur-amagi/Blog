from django.shortcuts import render
from blog.models import Articles ,Tags, ArticleTagMapping, Comments
from django.contrib import messages
from user.models import Users
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

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
        articles = Articles.objects.filter(title = search).order_by('-updated_at')
        if articles.exists():
                article_search = articles
        try:
            tag = Tags.objects.get(tag_name = search).id
        except Tags.DoesNotExist:
            tag = None
        if tag is not None:
            articles = Articles.objects.select_related().filter(articletagmapping__tag_id = tag).order_by('-updated_at')
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
