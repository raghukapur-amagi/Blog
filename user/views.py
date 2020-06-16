from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignUpForm
from user.models import Users
from django.template import RequestContext
from blog.models import Articles
# Create your views here.


def homepage(request):
    if request.user.is_authenticated:
        user_id = Users.objects.filter(user_id=request.user.id)
        print(user_id)
        if user_id.exists():
            print(user_id[0].id)
            user_articles = Articles.objects.filter(user_id=user_id[0].id)[:5]
            return(render(request, "homepage.html", context = { "user_articles":user_articles}))
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
            return HttpResponseRedirect('/home')
        else:
            print(form.error_messages)
            for msg in form.error_messages:
                messages.error(request,"{msg}: {form.error_messages[msg]}")
    else:
        form = SignUpForm()
    return(render(request,
                "register.html",
                context={"form":form})
            )

def login_request(request):
    print("inside login request")
    if request.method=='POST':
        form = AuthenticationForm(request, data = request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username,password = password)
            if user:
                print('user authenticated.')
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
    return(HttpResponseRedirect('login/'))