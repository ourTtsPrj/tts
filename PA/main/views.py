from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required

def checkUserLogin(r) :
    return r.user.is_authenticated 


@login_required
def logoutM(r) :
    logout(r)
    return redirect("mainM")
@login_required
def profile(r) :
    ufn = r.user.firstName
    lfn= r.user.lastName
    urank = r.user.rank
    return render(r,"profile.html",{"fname":ufn,"lname":lfn})
def mainM(r) :
    if checkUserLogin(r) :
        return redirect("profile")
    else :
        print("ok")
        # return redirect("loginM")
def signupM(r):
    if r.method=="POST":
        print(r.POST)
        thesignupform=signupForm(r.POST)
        if thesignupform.is_valid() :
            firstName= thesignupform.cleaned_data.get("firstName")
            lastName= thesignupform.cleaned_data.get("lastName")
            theStdCode = thesignupform.cleaned_data.get("stdcode")
            thePassword = thesignupform.cleaned_data.get("password")
            thePassword2 =thesignupform.cleaned_data.get("password2") 
            if theStdCode.isnumeric():
                if len(theStdCode)>=8 and len(theStdCode)<=9:
                    if thePassword==thePassword2:
                        theNewUser = get_user_model().objects.create_user(theStdCode,thePassword,"test","acc" ,"std")
                        user = authenticate(r,stdcode=theStdCode,password=thePassword)
                        if user is not None :
                            login(r,user)
                            # return redirect("profileM")

    else : 
        thesignupform = signupForm()
    return render(r,"signup.html",{"form":thesignupform})
def loginM(r) :
    if checkUserLogin(r) :
        return redirect("mainM")
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