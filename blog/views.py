from django.shortcuts import render
from blog.models import Articles ,Tags, Article_Tag_Mapping, Comments
from django.contrib import messages
from user.models import Users
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def create(request):
    if request.method == "POST":
        form = (request.POST)
        check = Users.objects.get(user_id=request.user.id)
        article = Articles(user = check, title= form["title"], body = form["body"], status = form['status'])
        article.save()
        tags = form["tags"].split(",")
        if tags[0] != '':
            for i in tags:
                query_set = Tags.objects.filter(tag_name= i )
                if query_set.exists():
                    mapping = Article_Tag_Mapping(article_id = article.id, tag_id = query_set[0].id)
                else:
                    tag= Tags(tag_name = i)
                    tag.save()
                    mapping = Article_Tag_Mapping(article_id = article.id, tag_id = tag.id)
                mapping.save()
        messages.info(request,"New article has been created with title {}".format(form["title"]))
        return HttpResponseRedirect('home')
    else:
        return(render(request,
                "createArticle.html",
                context={"check":"check"})
            )

def view(request, id):
    article = Articles.objects.filter(id = int(id))
    tags = Article_Tag_Mapping.objects.filter(article_id = int(id))
    tag_names = []
    for i in tags:
        tag_names.append(Tags.objects.filter(id = i.tag_id)[0].tag_name)
    return(render(request, "article_view.html", context = { "user_articles":article, "tags":tag_names}))

def update(request, id):
    article = Articles.objects.filter(id = int(id))
    tags = Article_Tag_Mapping.objects.filter(article_id = int(id))
    tag_names = ""
    for i in tags:
        tag_names = tag_names +Tags.objects.filter(id = i.tag_id)[0].tag_name +","
    return(render(request, "update_article.html", context = { "user_articles":article, "tags":tag_names}))


def save(request,id):
    if request.method == "POST":
        form = (request.POST)
        tags = form["tags"].split(",")
        Article_Tag_Mapping.objects.filter(article_id=id).delete()
        for i in tags:
            if i!='':
                query_set = Tags.objects.filter(tag_name= i )
                if query_set.exists():
                    mapping = Article_Tag_Mapping(article_id = id, tag_id = query_set[0].id)
                else:
                    tag= Tags(tag_name = i)
                    tag.save()
                    mapping = Article_Tag_Mapping(article_id = id, tag_id = tag.id)
                mapping.save()
        Articles.objects.select_related().filter(id  = id).update(title=form['title'])
        Articles.objects.select_related().filter(id  = id).update(body=form['body'])
        Articles.objects.select_related().filter(id  = id).update(status=form['status'])
        messages.info(request,"Article has been updated with title {}".format(form["title"]))
        return(HttpResponseRedirect('home'))

def search(request):
    #print("hello")
    if request.method == "POST":
        form = (request.POST)
        tag = form['Search By Tag']
        title = form['Search By Title']
        user_id = Users.objects.get(user_id=request.user.id)
        article_search = []
        if  title:
            articles = Articles.objects.filter(title=title, user_id=user_id)
            if articles.exists():
                article_search = articles
        if  tag:
            tags = Tags.objects.filter(tag_name=tag)
            if tags.exists(): 
                article_tag_ids  = Article_Tag_Mapping.objects.filter(tag_id = tags[0].id)
                if article_tag_ids.exists():
                    if article_search:
                        article_search = article_search | Articles.objects.filter(id = article_tag_ids[0].article_id,user_id = user_id)
                    else:
                        article_search = Articles.objects.filter(id = article_tag_ids[0].article_id,user_id = user_id)
                    for ids in range(1,len(article_tag_ids)):
                        article_search = article_search | Articles.objects.filter(id = article_tag_ids[ids].article_id, user_id=user_id)
        return(render(request, "search_view.html", context = { "article_search":article_search}))
            