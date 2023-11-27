from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import random, time, string, os, requests, json, cv2, io
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, JsonResponse
from flask_restful import Api, Resource, abort
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect
from django.urls import reverse
from mtcnn.mtcnn import MTCNN
from matplotlib import pyplot
from flask import Flask
from PIL import Image
from .models import *
from .forms import *

rawImagePath = "theApi/iMgrAW/"
detectImagePath = "theApi/iMgDeTECTfaCe/"
def convertToJpg(imagePath):
    img = Image.open(imagePath)
    png_path = imagePath.rsplit('.', 1)[0] + '.jpg'
    rgb_im = img.convert("RGB") 
    rgb_im.save(png_path)
def getImageExtension(imagePath):
    filename, file_extension = os.path.splitext(imagePath)
    return file_extension
def generateRandomString(length):
    letters = string.ascii_letters
    randomString = ''.join(random.choice(letters) for i in range(length))
    return randomString
def drawImageWithBox(fileName,resultList,cc,faceBox) :
    global rawImagePath
    img = cv2.imread(f"{rawImagePath}{fileName}")
    for result in resultList :
        faceBox[cc] = result['box']
        print(cc,result)
        x,y,w,h = result['box']
        cv2.rectangle(img, (x, y), (x+w, y+h), (240, 240, 14), 2)
        cv2.putText(img, str(cc), (x+10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (240, 240, 14), 2)
        cc += 1
        for key,value in result['keypoints'].items() :
            pass
            #cv2.circle(img,value,2,(240, 240, 14),-1)
    cv2.imwrite(f"{detectImagePath}{fileName}",img)
    return [len(resultList),cc,faceBox]


def checkAllSesstionAndCloseEndedSesstion() :
    theAllOpenSession = classSessionModel.objects.filter(classSessionStutus="open")
    for theOpenS in theAllOpenSession :
        if (theOpenS.classSessionOpenTime + theOpenS.classSessionOpenUntil) < int(time.time()) :
            print(theOpenS.classSessionSessionCode)
            classSessionModel.objects.filter(classSessionClassCode=theOpenS.classSessionClassCode,classSessionSessionCode=theOpenS.classSessionSessionCode,classSessionStutus="open").update(classSessionStutus="close")
            classModel.objects.filter(classCode=theOpenS.classSessionClassCode).update(classHasActiveSession=False)
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
        checkAllSesstionAndCloseEndedSesstion()
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
    checkAllSesstionAndCloseEndedSesstion()
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
            return redirect("ulistclass")
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
            "classNewSLink":reverse("unewsession",args=[cls.classCode]),
            "classSesstion":reverse("ulistclassde",args=[cls.classCode])


        }
        counter += 1
    checkAllSesstionAndCloseEndedSesstion()
    return render(request, "listOfClass.html", {'listClassAll': listClassAll})

@login_required
def uNewSession(r,theClassCode) :
    if r.user.rank=="std":
        return redirect("umain") #daneshjo ba link natavanad vared shavad
    if r.method == "POST" :
        theNewSessionForm = newSessionForm(r.POST,r.FILES)
        if theNewSessionForm.is_valid() :
            theRandonSessionCode = random.randint(1000000,9999999)
            theAllFiles = r.FILES.getlist('file_field')
            theFileNamesAll = ""
            fs = FileSystemStorage()
            for theTempFile in theAllFiles :
                theFileEx = getImageExtension(theTempFile.name)
                theRandFileName = generateRandomString(25)
                theFilePath = f"{rawImagePath}{theRandFileName}{theFileEx}"
                fs.save(theFilePath, theTempFile)
                if theFileEx != ".jpg" :
                    convertToJpg(theFilePath)
                theFileNamesAll += f"{theRandFileName}.jpg,"
            theUrlForDetectFace = reverse("detectface",args=["a",theFileNamesAll])
            theUrlForDetectFace = r.build_absolute_uri(theUrlForDetectFace)
            # print(theUrlForDetectFace)
            res = requests.get(theUrlForDetectFace)
            theDetectFaceRes = json.loads(res.text)
            if(theDetectFaceRes['face'] <= 0) :
                theNewSessionForm=newSessionForm()
                return render(r,"newSession.html",{"form":theNewSessionForm})
            theAllFaceLen = theDetectFaceRes['face']
            theCreateTime = int(time.time())
            classSessionModel(classSessionClassCode=theClassCode,classSessionSessionCode=theRandonSessionCode,classSessionStutus="open",classSessionOpenTime=theCreateTime,classSessionOpenUntil=600,classSessionHowManyUserDetect=theAllFaceLen,classSessionHowManyUserRecord=0).save()
            for theImgInfo in theDetectFaceRes['info'] :
                theImgDataInfo = theDetectFaceRes['info'][theImgInfo]
                theCreateTime = int(time.time())
                sessionImage(sessionImageClassCode=theClassCode,sessionImageSessionCode=theRandonSessionCode,sessionFakeFileName=generateRandomString(40),sessionImageImage=theImgInfo,sessionImageFaceJson=theImgDataInfo,sessionImageTime=theCreateTime).save()
            classModel.objects.filter(classCode=theClassCode).update(classHasActiveSession=True)
            return redirect(reverse("ulistclassde",args=[theClassCode]))
            # classSessionModel(sessionName=theSessionName,sessionDes=theDesSession,sessionPass=thePassword,sessionCode=theRandonSessionCode,sessionOwner=r.user.stdcode,sessionMakeTime=theCreateTime,sessionMemberLen=0,sessionHasActiveSession=False).save()
    checkTheClassId = classModel.objects.filter(classCode=theClassCode)
    if len(checkTheClassId) <= 0 :
        return redirect("ulistclass")
    if checkTheClassId[0].classHasActiveSession == True :
        return render(r,"newSession.html",{"msg":"این کلاس یک جلسه فعال دارد، هر کلاس در لحظه فقط می‌تواند یک جلسه فعال داشته باشد"})
    else :
        theNewSessionForm=newSessionForm()
        return render(r,"newSession.html",{"form":theNewSessionForm})
def uListClassDe(r,classcode):
    if r.user.rank=="std":
        return redirect("umain") #daneshjo ba link natavanad vared shavad
    checkAllSesstionAndCloseEndedSesstion()
    checkTheClassId = classModel.objects.filter(classCode=classcode)
    if len(checkTheClassId) <= 0 :
        return redirect("ulistclass")
    theClassSesstion = classSessionModel.objects.filter(classSessionClassCode=classcode)
    theResult = {}
    theCounter = 1
    for tCS in theClassSesstion :
        theSFile = sessionImage.objects.filter(sessionImageClassCode=classcode,sessionImageSessionCode=tCS.classSessionSessionCode)
        theSFileString = {}
        theSFCounter = 1
        for sFFile in theSFile :
            # theSFileString += f"<a href='{sFFile.sessionFakeFileName}'>عکس {theSFCounter}</a>"
            theSFileString[theSFCounter] = {"n":f"عکس {theSFCounter}","u":reverse("showimage",args=[sFFile.sessionFakeFileName])}
            theSFCounter += 1
        theEndIn = (tCS.classSessionOpenTime + tCS.classSessionOpenUntil) - int(time.time())
        if theEndIn < 0 :
            theEndIn = 0
        theResult[theCounter] = {"sCode":tCS.classSessionSessionCode,"sStatus":tCS.classSessionStutus,"sStart":tCS.classSessionOpenTime,"sEnd":theEndIn,"sDetect":tCS.classSessionHowManyUserDetect,"sRecord":tCS.classSessionHowManyUserRecord,"sImg":theSFileString}
        theCounter += 1    
    return render(r,"listOfClassDe.html",{"listSesstionAll":theResult})
def detectFace(r,key,query) :
    if key != "a" :
        return redirect("umain")
    cc = 1
    allFace = 0
    fileInfo = {}
    for fileName in query.split(",") :
        if fileName :
            faceBox = {}
            pixels = pyplot.imread(f"{rawImagePath}{fileName}")
            detector = MTCNN()
            faces = detector.detect_faces(pixels)
            rData = drawImageWithBox(fileName,faces,cc,faceBox)
            fileInfo[fileName] = {"face":rData[0],"from":cc,"to":rData[1] - 1,"faceBox":{}}
            cc = rData[1]
            allFace += rData[0]
            faceBox = rData[2]
            fileInfo[fileName]["faceBox"] = faceBox
    return JsonResponse({"ok":True,"face":allFace,"info":fileInfo})
@login_required
def showImage(r,fakeName) :
    makeFileNameValid = sessionImage.objects.filter(sessionFakeFileName=fakeName)
    if len(makeFileNameValid) <= 0 :
        return redirect("uprofile")
    fileName = makeFileNameValid[0].sessionImageImage
    imagePath = f"{detectImagePath}{fileName}"
    return FileResponse(open(imagePath, 'rb'), content_type='image/png')
def cropImage(r,fakeName,x,y,w,h) :
    makeFileNameValid = sessionImage.objects.filter(sessionFakeFileName=fakeName)
    if len(makeFileNameValid) <= 0 :
        return redirect("uprofile")
    fileName = makeFileNameValid[0].sessionImageImage
    imagePath = f"{rawImagePath}{fileName}"
    
    image = Image.open(imagePath)
    # x, y, w, h = 50, 50, 200, 200
    croppedImage = image.crop((x - 35, y - 35, w+x+75, h+y+75))
    byteArr = io.BytesIO()
    croppedImage.save(byteArr, format='PNG')
    byteArr.seek(0)
    return FileResponse(byteArr, content_type='image/png')
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