from django.contrib import admin
from django.urls import path,include
from . import views
app_name = "main"
urlpatterns = [
    path("login/",views.loginM,name="loginM"),
    path("logout/",views.logoutM,name="logoutM"),
    path("profile/",views.profile,name="profile"),
    path("",views.mainPage,name="main"),
    path("signup/",views.signupM,name="signupM"),
]
