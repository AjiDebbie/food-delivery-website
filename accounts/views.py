from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


# Create your views here.


def RegisterUser(request):
    # return HttpResponse(request.method)
    myform = UserCreationForm(request.POST or None)
    if(request.method=="POST"):
        if myform.is_valid():
            user= myform.save()
            login(request,user)
            return redirect('/')
    data = {"form":myform,"title":"User Registration"}
    return render(request,"registration/signup.html",data)





