from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.contrib import messages
from django.contrib.auth.models import auth
from account.models import Account
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        
        user = Account.objects.create_user(email=email, phone=phone, name=name, password=password)
        user.save()
        
        messages.info(request, 'Account created successfully. Please sign in!')
        
        return redirect("/account/login")
    else:
        return render(request, "register.html")

def login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        
        if not Account.objects.filter(phone=phone).exists():
            messages.info(request, 'Your phone number does not hold an account. Please sign up!')
            return redirect("register")
        
        user = auth.authenticate(phone=phone, password=password)
        
        if user is not None:
            auth.login(request, user)
            next = request.POST.get('next')
            if(next is not None):
                return redirect(next)
            return redirect("/")
        else:
            messages.info(request, 'Invalid password!')
            return redirect("login")
    else:
        data = {}
        next = request.GET.get('next')
        if(next is not None):
            data = {'next': next}
        return render(request, "login.html", data)
    
def logout(request):
    auth.logout(request)
    return redirect("/")

@login_required(login_url='/account/login/')    
def profileView(request):
    return render(request, "profileView.html")

@login_required(login_url='/account/login/')    
def profileEdit(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        user = Account.objects.get(phone=request.user.phone)
        user.set_name(name)
        user.set_phone(phone)
        user.set_email(email)
        
        user.save()
        return redirect("/account/profileView/")
    else:
        context = {}
        return render(request, "profileEdit.html")
    
@login_required(login_url='/account/login/')    
def changePasswd(request):
    if request.method == 'POST':
        oldPasswd = request.POST['oldPasswd']
        passwd = request.POST['password']
        user = auth.authenticate(phone=request.user.phone, password=oldPasswd)
        if(user != None):
            user.set_password(passwd)
            user.save()
            messages.info(request, "Please login with the new password!")
            return redirect("login")
        else:
            messages.info(request, "Current password is wrong!")
            return redirect("changePasswd")    
    else:
        return render(request, "changePasswd.html")
    
# Ajax Functions
def phoneCheck(request):
    phone = request.GET.get('Phone', None)
    if Account.objects.filter(phone=phone).exists():
        return HttpResponse(json.dumps({"Exist": "True"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"Exist": "False"}), content_type="application/json")
    
def emailCheck(request):
    email = request.GET.get('Email', None)
    if Account.objects.filter(email=email).exists():
        return HttpResponse(json.dumps({"Exist": "True"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"Exist": "False"}), content_type="application/json")
    
def phoneEditCheck(request):
    phone = request.GET.get('Phone', None)
    if(request.user.phone!=phone and Account.objects.filter(phone=phone).exists()):
        return HttpResponse(json.dumps({"Exist": "True"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"Exist": "False"}), content_type="application/json")
    
def emailEditCheck(request):
    email = request.GET.get('Email', None)
    if(request.user.email!=email and Account.objects.filter(email=email).exists()) :
        return HttpResponse(json.dumps({"Exist": "True"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"Exist": "False"}), content_type="application/json")
    
