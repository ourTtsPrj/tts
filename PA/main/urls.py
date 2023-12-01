from django.contrib import admin
from django.urls import path,include
from .views import *
# app_name = "main"
urlpatterns = [
    path("login/",ulogin,name="ulogin"),
    path("logout/",ulogout,name="ulogout"),
    path("profile/",uprofile,name="uprofile"),
    path("",umain,name="umain"),
    path("signup/",usignup,name="usignup"),
    path("createClass/",ucreateclass,name="ucreateclass"),
    path("listClass/",uListClass,name="ulistclass"),
    path("listClass/<int:classcode>",uListClassDe,name="ulistclassde"),#name mohem hast,kar ba moteghaiierha
    path("newSession/<int:theClassCode>",uNewSession,name="unewsession"),
    path("confirmList/<int:theClassCode>/<int:sessionCode>",confirmList,name="confirmlist"),
    path("id/<str:key>/<str:query>",detectFace,name="detectface"), #image detect
    path("is/<str:fakeName>",showImage,name="showimage"), #image show
    path("ic/<str:fakeName>/<int:x>/<int:y>/<int:w>/<int:h>",cropImage,name="cropimage"), #image crop
    path("ic/<int:classCode>/<int:faceId>",cropImageMinimal,name="cropimageminimal"),
    path("c/",makeClassPresent,name="makeclasspresent"),
    path("l/",listOfUserPresent,name="listofuserpresent"),
    path("myClasses/",uMyClesses,name="umyclasses")
]
