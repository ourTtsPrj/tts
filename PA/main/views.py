from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
import random, time
from django.http import HttpResponse

def checkUserLogin(r) :
    return r.user.is_authenticated 


@login_required
def ulogout(r) :
    logout(r)
    return redirect("umain")
@login_required
def uprofile(r) :
    ufn = r.user.firstName
    lfn= r.user.lastName
    urank = r.user.rank
    if urank == "std":
        return render(r,"userprofile.html",{"fname":ufn,"lname":lfn})
    elif urank == "teach":
         return render(r,"teachprofile.html",{"fname":ufn,"lname":lfn})
def umain(r) :
    if checkUserLogin(r) :
        return redirect("uprofile")
    else :
        #print("ok")
        return redirect("ulogin")
def usignup(r):
    if checkUserLogin(r) :
        return redirect("umain")
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
                        checkduser=User.objects.filter(stdcode=theStdCode)
                        if len(checkduser)>0:
                            return render(r,"signup.html",{"form":thesignupform})
                        theNewUser = get_user_model().objects.create_user(theStdCode,thePassword,firstName,lastName ,"std")
                        user = authenticate(r,stdcode=theStdCode,password=thePassword)
                        if user is not None :
                            login(r,user)
                            return redirect("uprofile")

        else :
            print(thesignupform.errors)
    else : 
        thesignupform = signupForm()
    return render(r,"signup.html",{"form":thesignupform})
def ulogin(r) :
    if checkUserLogin(r) :
        return redirect("umain")
    if r.method == "POST" :
        print(r.POST)
        theLoginForm = loginForm(r.POST)
        if theLoginForm.is_valid() :
            theStdCode = theLoginForm.cleaned_data.get("stdcode")
            thePassword = theLoginForm.cleaned_data.get("password")
            user = authenticate(r,stdcode=theStdCode,password=thePassword)
            if user is not None :
                login(r,user)
                return redirect("uprofile")
    else : 
        theLoginForm = loginForm()
    return render(r,"login.html",{"form":theLoginForm})
@login_required
def ucreateclass(r) :
    if r.user.rank=="std":
        return redirect("umain") #daneshjo ba link natavanad vared shavad
    if r.method == "POST" :
        print(r.POST)
        theCreateClassForm = createclassForm(r.POST)
        if theCreateClassForm.is_valid() :
            theClassName = theCreateClassForm.cleaned_data.get("className")
            thePassword = theCreateClassForm.cleaned_data.get("password")
            theDesClass = theCreateClassForm.cleaned_data.get("desClass")
            theRandonClassCode=random.randint(1000000,9999999)
            theCreateTime=int(time.time())
            classModel(className=theClassName,classDes=theDesClass,classPass=thePassword,classCode=theRandonClassCode,classOwner=r.user.stdcode,classMakeTime=theCreateTime,classMemberLen=0,classHasActiveSession=False).save()
    theNewClassForm=createclassForm()
    return render(r,"createclass.html",{"form":theNewClassForm})
@login_required
def uListClass(r) :
    return render(r,"listOfClass.html")

@login_required
def uListClass(request):
    
    theUserClass = classModel.objects.filter(classOwner=request.user.stdcode)
    listClassAll = {}
    counter = 1

    for cls in theUserClass:
        
        listClassAll[counter] = {
            'class_name':cls.className ,  
            'class_des':cls.classDes, 
            'class_pass':cls.classPass, 
            'class_code':cls.classCode, 
            'class_memberlen':cls.classMemberLen, 
            'class_hasactive':cls.classHasActiveSession, 


        }
        counter += 1
    return render(request, "listOfClass.html", {'listClassAll': listClassAll})

@login_required
def uNewSession(r) :
    if r.user.rank=="std":
        return redirect("umain") #daneshjo ba link natavanad vared shavad
    if r.method == "POST" :
        print(r.POST)
        theNewSessionForm = newSessionForm(r.POST)
        if theNewSessionForm.is_valid() :
            # theSessionName = theNewSessionForm.cleaned_data.get("sesseionName")
            # thePassword = theNewSessionForm.cleaned_data.get("password")
            # theDesSession = theNewSessionForm.cleaned_data.get("desSession")
            theRandonSessionCode=random.randint(1000000,9999999)
            theCreateTime=int(time.time())
            # classSessionModel(sessionName=theSessionName,sessionDes=theDesSession,sessionPass=thePassword,sessionCode=theRandonSessionCode,sessionOwner=r.user.stdcode,sessionMakeTime=theCreateTime,sessionMemberLen=0,sessionHasActiveSession=False).save()
    theNewSessionForm=newSessionForm()
    return render(r,"newSession.html",{"form":theNewSessionForm})
def uListClassDe(r,classcode):
    pass


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