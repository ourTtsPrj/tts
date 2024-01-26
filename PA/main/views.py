import random, time, string, os, requests, json, cv2, io, pytz
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, JsonResponse
from flask_restful import Api, Resource, abort
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect
from django.urls import reverse
from mtcnn.mtcnn import MTCNN
from matplotlib import pyplot
from datetime import datetime
from flask import Flask
from PIL import Image
from .models import *
from .forms import *
rawImagePath = "theApi/iMgrAW/"
detectImagePath = "theApi/iMgDeTECTfaCe/"

def iranTime(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if (gm > 2):
        gy2 = gy + 1
    else:
        gy2 = gy
    days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
    jy = -1595 + (33 * (days // 12053))
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if (days > 365):
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if (days < 186):
        jm = 1 + (days // 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + ((days - 186) // 30)
        jd = 1 + ((days - 186) % 30)
    return [jy, jm, jd]
def getIranTime() :
    tT = pytz.timezone("Asia/Tehran")
    datetime_ist = datetime.now(tT)
def getIranTimeFromTimestamp(timestamp) :
    ttz = pytz.timezone("Asia/Tehran")
    datetime_ist = datetime.fromtimestamp(timestamp,tz=ttz)
    y,m,d = datetime_ist.strftime("%Y:%m:%d").split(":")
    if int(m) < 10 :
        m = str(m).replace("0","")
    if int(d) < 10 :
        d = str(d).replace("0","")
    dIran = iranTime(int(y),int(m),int(d))
    realDate = datetime_ist.strftime(f'{dIran[0]}-{dIran[1]}-{dIran[2]} %H:%M:%S')
    return realDate
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
def getAllLinkOfSessionImage(classCode) :
    theClassForCheckSe = classModel.objects.filter(classCode=classCode)
    if len(theClassForCheckSe) < 0 :
        return
    theClassForCheckSe = theClassForCheckSe[0]
    if theClassForCheckSe.classHasActiveSession == False :
        return
    theThisClassSeCode = classSessionModel.objects.filter(classSessionClassCode=classCode,classSessionStutus="open")[0].classSessionSessionCode
    theImges = sessionImage.objects.filter(sessionImageClassCode=classCode,sessionImageSessionCode=theThisClassSeCode)
    rFR = {}
    counter = 1
    for tci in theImges :
        rFR[counter] = {"url":reverse("showimage",args=[tci.sessionFakeFileName])}
        counter += 1
    return rFR
def findFaceBoxInActiveSe(classCode,userFaceId) :
    theClassForCheckSe = classModel.objects.filter(classCode=classCode)
    if len(theClassForCheckSe) < 0 :
        return
    theClassForCheckSe = theClassForCheckSe[0]
    if theClassForCheckSe.classHasActiveSession == False :
        return
    theThisClassSeCode = classSessionModel.objects.filter(classSessionClassCode=classCode,classSessionStutus="open")[0].classSessionSessionCode
    theImges = sessionImage.objects.filter(sessionImageClassCode=classCode,sessionImageSessionCode=theThisClassSeCode)
    isFaceIdValid = False
    theUserFaceBox = None
    theUserFakeFileName = None
    for tic in theImges :
        theThisImgFaceJson = json.loads(tic.sessionImageFaceJson.replace("'",'"'))
        if userFaceId >= theThisImgFaceJson['from'] and userFaceId <= theThisImgFaceJson['to'] :
            isFaceIdValid = True
            theUserFaceBox = theThisImgFaceJson['faceBox'][str(userFaceId)]
            theUserFakeFileName = tic.sessionFakeFileName
    if isFaceIdValid == False :
        return "bad face id"
    return [isFaceIdValid,theUserFakeFileName,theUserFaceBox]
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
    if r.user.rank != "teach":
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
            'class_memberlen':len(whoWhereModel.objects.filter(whoWhereClassCode=cls.classCode)), 
            'class_hasactive':cls.classHasActiveSession, 
            "classNewSLink":reverse("unewsession",args=[cls.classCode]),
            "classSesstion":reverse("ulistclassde",args=[cls.classCode])


        }
        counter += 1
    checkAllSesstionAndCloseEndedSesstion()
    return render(request, "listOfClass.html", {'listClassAll': listClassAll})

@login_required
def uNewSession(r,theClassCode) :
    if r.user.rank != "teach" :
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
    if r.user.rank != "teach" :
        return redirect("umain") #daneshjo ba link natavanad vared shavad
    checkAllSesstionAndCloseEndedSesstion()
    checkTheClassId = classModel.objects.filter(classCode=classcode)
    if len(checkTheClassId) <= 0 :
        return redirect("ulistclass")
    theClassSesstion = classSessionModel.objects.filter(classSessionClassCode=classcode).order_by("-classSessionOpenTime")
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
        theSSS = tCS.classSessionStutus
        if theSSS == "close" :
            theSSS = "بسته"
        else :
            theSSS = "باز"
        theResult[theCounter] = {"sCode":tCS.classSessionSessionCode,"sStatus":theSSS,"sStart":getIranTimeFromTimestamp(tCS.classSessionOpenTime),"sEnd":theEndIn,"sDetect":tCS.classSessionHowManyUserDetect,"sRecord":tCS.classSessionHowManyUserRecord,"sImg":theSFileString,"confrimUrl":reverse("confirmlist",args=[classcode,tCS.classSessionSessionCode])}
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
@login_required
def makeClassPresent(r) :
    checkAllSesstionAndCloseEndedSesstion()
    # makeClassPresent.html
    if r.method == "POST" :
        theFilledForm = makeClassPresentForm(r.POST)
        if theFilledForm.is_valid() :
            thePClassCode = theFilledForm.cleaned_data.get("classCode")
            thePClassPass = theFilledForm.cleaned_data.get("classPass")
            thePUserFace = theFilledForm.cleaned_data.get("userFace")
            if thePClassCode is not None and thePClassPass is not None and thePUserFace is not None : # ? mode 3 | no new mode
                checkClassE = classModel.objects.filter(classCode=thePClassCode)
                if len(checkClassE) <= 0 :
                    return render(r,"makeClassPresent.html",{"form":makeClassPresentForm(),"mode":1,"msg":"کد کلاس اشتباه می‌باشد"})
                checkTheUserInClassBefore = whoWhereModel.objects.filter(whoWhereStdCode=r.user.stdcode)
                if len(checkTheUserInClassBefore) > 0 :
                    theMakeClassPresent = makeClassPresentForm(initial={"classCode":thePClassCode,"classPass":checkClassE[0].classPass})
                    if checkClassE[0].classHasActiveSession == False :
                        return render(r,"makeClassPresent.html",{"form":makeClassPresentForm(),"mode":1,"msg":"در حال حاضر جلسه فعالی برای ثبت حاضری وجود ندارد"})
                checkUserFaceId = cropImageMinimal(r,thePClassCode,thePUserFace)
                if type(checkUserFaceId) is bool :
                    theMakeClassPresent = makeClassPresentForm(initial={"classCode":thePClassCode,"classPass":thePClassPass})
                    return render(r,"makeClassPresent.html",{"form":theMakeClassPresent,"mode":3,"msg":"شماره چهره وارد شده متعبر نمی‌باشد"})
                theThisClassSeCode = classSessionModel.objects.filter(classSessionClassCode=thePClassCode,classSessionStutus="open")[0]
                checkThisFaceUseBefore = sessionLog.objects.filter(sessionLogClassCode=thePClassCode,sessionLogSessionCode=theThisClassSeCode.classSessionSessionCode,sessionLogFaceCode=thePUserFace)
                if len(checkThisFaceUseBefore) > 0 :
                    theLinkOfPhotos = getAllLinkOfSessionImage(thePClassCode)
                    return render(r,"makeClassPresent.html",{"form":theMakeClassPresent,"mode":3,"msg":"این شماره چهره قبلا ثبت شده، هر چهره فقط یکبار میتواند ثبت شود","theImg":theLinkOfPhotos})
                userFaceIdUrl = reverse("cropimageminimal",args=[thePClassCode,thePUserFace])
                checkUserSetPABefore = sessionLog.objects.filter(sessionLogClassCode=thePClassCode,sessionLogSessionCode=theThisClassSeCode.classSessionSessionCode,sessionLogStdCode=r.user.stdcode)
                theSomeDataFromInCode = findFaceBoxInActiveSe(thePClassCode,thePUserFace)
                theJsonForDes = json.dumps({"fakeFile":theSomeDataFromInCode[1],"faceBox":theSomeDataFromInCode[2]})
                if len(checkUserSetPABefore) > 0 :
                    checkUserSetPABefore.update(sessionLogFaceCode=thePUserFace,sessionLogFaceDes=theJsonForDes,sessionLogTime=int(time.time()))
                else :
                    sessionLog(sessionLogClassCode=thePClassCode,sessionLogSessionCode=theThisClassSeCode.classSessionSessionCode,sessionLogStdCode=r.user.stdcode,sessionLogFaceCode=thePUserFace,sessionLogFaceDes=theJsonForDes,sessionLogTime=int(time.time())).save()
                    classSessionModel.objects.filter(classSessionClassCode=thePClassCode,classSessionStutus="open").update(classSessionHowManyUserRecord=(theThisClassSeCode.classSessionHowManyUserRecord + 1))
                theMakeClassPresent = makeClassPresentForm(initial={"classCode":thePClassCode,"classPass":thePClassPass,"userFace":thePUserFace})
                return render(r,"makeClassPresent.html",{"form":theMakeClassPresent,"mode":3,"theCroppedUserFace":userFaceIdUrl,"msg":"حاضری شما باموفقیت ثبت شد"}) 
            
            
            elif thePClassCode is not None and thePClassPass is not None : #? mode 2 | new mode 3
                checkClassE = classModel.objects.filter(classCode=thePClassCode,classPass=thePClassPass)
                if len(checkClassE) <= 0 :
                    return render(r,"makeClassPresent.html",{"form":makeClassPresentForm(),"mode":1,"msg":"کد و یا رمز کلاس اشتباه می‌باشد"})
                checkTheUserInClassBefore = whoWhereModel.objects.filter(whoWhereStdCode=r.user.stdcode)
                if len(checkTheUserInClassBefore) <= 0 :
                    whoWhereModel(whoWhereStdCode=r.user.stdcode,whoWhereClassCode=thePClassCode,whoWhereJoinedTime=int(time.time())).save()

                if checkClassE[0].classHasActiveSession == False :
                    return render(r,"makeClassPresent.html",{"form":makeClassPresentForm(),"mode":1,"msg":"در حال حاضر جلسه فعالی برای ثبت حاضری وجود ندارد"})
                
                theLinkOfPhotos = getAllLinkOfSessionImage(thePClassCode)
                theMakeClassPresent = makeClassPresentForm(initial={"classCode":thePClassCode,"classPass":thePClassPass})
                return render(r,"makeClassPresent.html",{"form":theMakeClassPresent,"mode":3,"msg":"شماره چهره خود را وارد کنید","theImg":theLinkOfPhotos})
            
            
            elif thePClassCode is not None : #? mode 1 | new mode 2
                checkClassE = classModel.objects.filter(classCode=thePClassCode)
                if len(checkClassE) <= 0 :
                    return render(r,"makeClassPresent.html",{"form":makeClassPresentForm(),"mode":1,"msg":"کد کلاس اشتباه می‌باشد"})
                checkTheUserInClassBefore = whoWhereModel.objects.filter(whoWhereStdCode=r.user.stdcode)
                if len(checkTheUserInClassBefore) > 0 :
                    theMakeClassPresent = makeClassPresentForm(initial={"classCode":thePClassCode,"classPass":checkClassE[0].classPass})
                    if checkClassE[0].classHasActiveSession == False :
                        return render(r,"makeClassPresent.html",{"form":makeClassPresentForm(),"mode":1,"msg":"در حال حاضر جلسه فعالی برای ثبت حاضری وجود ندارد"})
                    
                    theThisClassSeCode = classSessionModel.objects.filter(classSessionClassCode=thePClassCode,classSessionStutus="open")[0].classSessionSessionCode
                    checkUserSetPABefore = sessionLog.objects.filter(sessionLogClassCode=thePClassCode,sessionLogSessionCode=theThisClassSeCode,sessionLogStdCode=r.user.stdcode)
                    theLinkOfPhotos = getAllLinkOfSessionImage(thePClassCode)
                    if len(checkUserSetPABefore) > 0 :
                        userFaceIdUrl = reverse("cropimageminimal",args=[thePClassCode,checkUserSetPABefore[0].sessionLogFaceCode])
                        theMakeClassPresent = makeClassPresentForm(initial={"classCode":thePClassCode,"classPass":checkClassE[0].classPass,"userFace":checkUserSetPABefore[0].sessionLogFaceCode})
                        return render(r,"makeClassPresent.html",{"form":theMakeClassPresent,"mode":3,"theCroppedUserFace":userFaceIdUrl,"msg":"شما قبلا حاضری خود را ثبت کرده‌اید می‌توانید شماره چهره را تغییر دهید","theImg":theLinkOfPhotos}) 

                    return render(r,"makeClassPresent.html",{"form":theMakeClassPresent,"mode":3,"msg":"شماره چهره خود را وارد کنید","theImg":theLinkOfPhotos})
                theMakeClassPresent = makeClassPresentForm(initial={"classCode":thePClassCode})
                return render(r,"makeClassPresent.html",{"form":theMakeClassPresent,"mode":2,"msg":"رمز کلاس را وارد کنید"})


    theMakeClassPresent = makeClassPresentForm()
    return render(r,"makeClassPresent.html",{"form":theMakeClassPresent,"mode":1,"msg":"پس از ثبت اولین حاضری شما عضو کلاس خواهید شد"})
@login_required
def cropImageMinimal(r,classCode,faceId) :
    getFaceInfo = findFaceBoxInActiveSe(classCode,faceId)
    if type(getFaceInfo) is list :
        return cropImage(r,getFaceInfo[1],getFaceInfo[2][0],getFaceInfo[2][1],getFaceInfo[2][2],getFaceInfo[2][3])
    return False
def confirmList(r,theClassCode,sessionCode) :
    if r.user.rank != "teach" :
        return redirect("umain") #daneshjo ba link natavanad vared shavad
    checkTheClassAndSession = classSessionModel.objects.filter(classSessionClassCode=theClassCode,classSessionSessionCode=sessionCode)
    if len(checkTheClassAndSession) <= 0 :
        return redirect('umain')
    theAllSessionLog = sessionLog.objects.filter(sessionLogClassCode=theClassCode,sessionLogSessionCode=sessionCode)
    rFR = {}
    counter = 1
    for theasl in theAllSessionLog :
        theUserDes = json.loads(theasl.sessionLogFaceDes)
        theUserFakeFileName = theUserDes["fakeFile"]
        theUserFakeFaceBox = theUserDes["faceBox"]
        rFR[counter] = {"codeClass":theClassCode,"codeSe":sessionCode,"sCode":theasl.sessionLogStdCode,"fCode":theasl.sessionLogFaceCode,"faceUrl":reverse("cropimage",args=[theUserFakeFileName,theUserFakeFaceBox[0],theUserFakeFaceBox[1],theUserFakeFaceBox[2],theUserFakeFaceBox[3]]),"rTime":getIranTimeFromTimestamp(theasl.sessionLogTime)}
        counter += 1
    theBackLink = reverse("ulistclassde",args=[theClassCode])
    return render(r,"confirmList.html",{"listSesstionAll":rFR,"backLink":theBackLink,"theTitle":"لیست تایید جلسه"})
@login_required
def listOfUserPresent(r) :
    theAllSessionLog = sessionLog.objects.filter(sessionLogStdCode=r.user.stdcode)
    rFR = {}
    counter = 1
    for theasl in theAllSessionLog :
        theUserDes = json.loads(theasl.sessionLogFaceDes)
        theUserFakeFileName = theUserDes["fakeFile"]
        theUserFakeFaceBox = theUserDes["faceBox"]
        rFR[counter] = {"codeClass":theasl.sessionLogClassCode,"codeSe":theasl.sessionLogSessionCode,"sCode":theasl.sessionLogStdCode,"fCode":theasl.sessionLogFaceCode,"faceUrl":reverse("cropimage",args=[theUserFakeFileName,theUserFakeFaceBox[0],theUserFakeFaceBox[1],theUserFakeFaceBox[2],theUserFakeFaceBox[3]]),"rTime":getIranTimeFromTimestamp(theasl.sessionLogTime)}
        counter += 1
    theBackLink = reverse("umain")
    return render(r,"confirmList.html",{"listSesstionAll":rFR,"backLink":theBackLink,"theTitle":"لیست حاضری‌های من"})
@login_required
def uMyClesses(r) :
    theResult = {}
    counter = 1
    theListOfClassUJoined = whoWhereModel.objects.filter(whoWhereStdCode=r.user.stdcode)
    for theW in theListOfClassUJoined :
        theClassDetail = classModel.objects.filter(classCode=theW.whoWhereClassCode)[0]
        theOwenerName = User.objects.filter(stdcode=theClassDetail.classOwner)[0]
        theOwenerName = f"{theOwenerName.firstName} {theOwenerName.lastName}"
        theResult[counter] = {"className":theClassDetail.className,"classDes":theClassDetail.classDes,"classCode":theClassDetail.classCode,"classMemberLen":len(whoWhereModel.objects.filter(whoWhereClassCode=theClassDetail.classCode)),"theOwenerName":theOwenerName}
        counter += 1
    return render(r,"myclasses.html",{"theResult":theResult})
# !fix : have bug when user logged in as teach can control other class which not class owner !!!