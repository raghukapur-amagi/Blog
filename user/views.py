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
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework.decorators import api_view
import logging
from django.db import IntegrityError, transaction

logger = logging.getLogger('django')

User = get_user_model()

@csrf_exempt
@api_view(['POST', ])
def login_user(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return HttpResponse(status = 400)
        data = JSONParser().parse(request)
        username = data["username"]
        user = authenticate(username = username,password = data["password"])
        if user:
                login(request,user)
                logger.info("User with username {} has been successfully logged in".format(username))
                return(Response({"info":"User has successfully logged in"},status = status.HTTP_200_OK))
        else:
            logger.info("User with username {} could not be logged in".format(username))
            return(Response({"error":"User with username {} could not be logged in".format(username)},status= status.HTTP_401_UNAUTHORIZED))

@csrf_exempt
@api_view(['GET', ])
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return(Response({"info":"User has been logged out"},status = status.HTTP_200_OK))
    else:
        return(Response({"info":"User hasn't logged in"},status = status.HTTP_400_BAD_REQUEST))


@csrf_exempt
@api_view(['POST', ])
def register_user(request):
    if request.method == "POST":
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data = user_data)
        if user_serializer.is_valid():
            with transaction.atomic():
                user_serializer.save()
                user_id = User.objects.get(username = user_data["username"]).id
                user_data["user_id"] = user_id
                user_profile_serializer = UserProfileSerializer(data = user_data)
                if user_profile_serializer.is_valid():
                    user_profile_serializer.save()
                    logger.info("new user has been added with username {}".format(user_data["username"]))
                    return(Response(user_data, status = status.HTTP_201_CREATED))
        logger.error("user could not be added with data {}".format(user_data))
        return(Response(user_serializer.errors, status = status.HTTP_400_BAD_REQUEST))

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
            logger.info("new user has been added with username {}".format(username))
            return(HttpResponseRedirect('/home'))
        else:
            for msg in form.error_messages:
                logger.error("Error with the registration form {msg}: {form.error_messages[msg]}")
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
                logger.info("{username} has logged in.")
                messages.info(request, "Logged in successfully as {}".format(username))
                return(HttpResponseRedirect('/home'))
            else:
                logger.error("Wrong Username: {username} and Password {password}")
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