from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from .forms import *

def checkUserLogin(r) :
    return r.user.is_authenticated 

def loginM(r) :
    if checkUserLogin(r) :
        return redirect("main")
    if r.method == "POST" :
        print(r.POST)
        theLoginForm = loginForm(r.POST)
        if theLoginForm.is_valid() :
            theStdCode = theLoginForm.cleaned_data.get("stdcode")
            thePassword = theLoginForm.cleaned_data.get("password")
            user = authenticate(r,stdcode=theStdCode,password=thePassword)
            if user is not None :
                login(r,user)
            return redirect("profile")
    else : 
        theLoginForm = loginForm()
    return render(r,"login.html",{"form":theLoginForm})
def logoutM(r) :
    if checkUserLogin(r) :
        logout(r)
    return redirect("main")
def profile(r) :
    if checkUserLogin(r) == False :
        return redirect("main")
    else :
        return render(r,"profile.html")
def mainPage(r) :
    if checkUserLogin(r) :
        return redirect("profile")
    else :
        return redirect("loginM")
def signupM(r):
    if r.method=="POST":
        print(r.POST)
        thesignupform=signupForm(r.POST)
        if thesignupform.is_valid() :
            theStdCode = thesignupform.cleaned_data.get("stdcode")
            thePassword = thesignupform.cleaned_data.get("password")
            thrPassword2 =thesignupform.cleaned_data.get("password2")  
            if theStdCode.is_valid():
                theStdCode=
            if len(thrPassword2):

    else : 
        thesignupform = signupForm()
    return render(r,"signup.html",{"form":thesignupform})

# Create your views here.



"""def tf(r) :
    if r.method == "POST" :
        ttff = testForm(r.POST)
        if ttff.is_valid() :
            theName = ttff['name'].value()
            theName = ttff.cleaned_data.get('name')
            return render(r,"tt.html",{"msg":f"tnx {theName}"})
    else :
        ttff = testForm()
    return render(r,"tt.html",{"form":ttff})"""