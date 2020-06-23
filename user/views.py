from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import SignUpForm
from user.models import Users
from django.template import RequestContext
from blog.models import Articles
from rest_framework import serializers, viewsets, status
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserProfileSerializer

User = get_user_model()

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return HttpResponse(status = 400)
        data = JSONParser().parse(request)
        user = authenticate(username = data["username"],password = data["password"])
        if user:
                login(request,user)
                return(HttpResponse(status = 200))
        else:
            return(HttpResponse(status= 401))

@csrf_exempt
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return(HttpResponse(status = 200))
    else:
        return(HttpResponse(status = 400))


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            user_id = User.objects.get(username=data["username"]).id
            data["user_id"] = user_id
            serializer = UserProfileSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return(JsonResponse(data, status = 201))
        return(JsonResponse(serializer.errors, status = 400))

def homepage(request):
    if request.user.is_authenticated:
        try:
            user_id = Users.objects.get(user_id=request.user.id).id
        except Users.DoesNotExist:
            user_id = None
        if user_id:
            user_articles = Articles.objects.filter(user_id=user_id)[:5]
            if user_articles.exists():
                return(render(request, "homepage.html", context = { "user_articles":user_articles}))
            else:
                return(render(request, "homepage.html", context = { "user_articles":[]}))
        else:
            return(render(request, "homepage.html", context = { "user_articles":[]}))
    else:
        user_articles = Articles.objects.select_related().filter(status = "publish")[:5]
        if user_articles.exists():
            return(render(request, "homepage.html", context = {"user_articles":user_articles}))
        else:
            return(render(request, "homepage.html", context = { "user_articles":[]}))

def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request,user)
            current_user = request.user
            profile = Users(user_id= current_user.id, bio=form.cleaned_data.get('Bio'))
            profile.save()
            messages.info(request,"You are now logged in as {}".format(username))
            return(HttpResponseRedirect('/home'))
        else:
            for msg in form.error_messages:
                messages.error(request,"{msg}: {form.error_messages[msg]}")
            return HttpResponseRedirect('/home')
    else:
        form = SignUpForm()
    return(render(request,
                "register.html",
                context={"form":form})
            )

def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username,password = password)
            if user:
                login(request,user)
                messages.info(request, "Logged in successfully as {}".format(username))
                return(HttpResponseRedirect('/home'))
            else:
                messages.error(request, "Wrong username and password")
                return(HttpResponseRedirect('login'))
        else:
            messages.error(request,"Error with the form")
            return(HttpResponseRedirect('login'))
    
    form = AuthenticationForm
    return(render(request,
                "login.html",
                context={"form":form})
            )

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return(HttpResponseRedirect('/home'))