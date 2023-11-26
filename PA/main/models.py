from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import time

class UserManager(BaseUserManager):

  def _create_user(self, stdcode, password, fName, lName, rank, is_superuser, is_staff, **extra_fields):
    if not stdcode:
        raise ValueError('Users must have stdcode')
    now = int(time.time())
    user = self.model(
        stdcode=stdcode,
        firstName=fName,
        lastName=lName,
        joinTime=now, 
        lastLogin=now,
        rank=rank, 
        is_superuser=is_superuser,
        is_staff=is_staff,
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, stdcode, password, fName, lName, rank, **extra_fields):
    return self._create_user(stdcode, password, fName, lName, rank, 0,0, **extra_fields)
  def create_superuser(self, stdcode, password, fName, lName, rank,**extra_fields):
    return self._create_user(stdcode, password, fName, lName, rank, 1,1, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "stdcode"
    stdcode = models.IntegerField(unique=True)
    firstName = models.CharField(max_length=70)
    lastName = models.CharField(max_length=70)
    joinTime = models.IntegerField()
    lastLogin = models.IntegerField()
    rank = models.CharField(max_length=50)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)


class classModel(models.Model) :
   className = models.CharField(max_length=128)
   classDes=models.CharField(max_length=128)
   classPass=models.CharField(max_length=32)
   classCode=models.IntegerField()
   classOwner=models.IntegerField()
   classMakeTime=models.IntegerField()
   classMemberLen=models.IntegerField()
   classHasActiveSession = models.BooleanField(default=False)

class whoWhereModel(models.Model):
   whoWhereFirstName=models.CharField(max_length=70)
   whoWhereLastName=models.CharField(max_length=70)
   whoWhereStdCode=models.IntegerField()
   whoWhereClassCode=models.IntegerField()
   whoWhereJoinedTime=models.IntegerField()

class classSessionModel(models.Model):
   classSessionClassCode=models.IntegerField()
   classSessionSessionCode=models.IntegerField()
   classSessionStutus=models.CharField(max_length=10)
   classSessionOpenTime=models.IntegerField()
   classSessionOpenUntil=models.IntegerField()
   classSessionHowManyUserDetect=models.IntegerField()
   classSessionHowManyUserRecord=models.IntegerField()

class sessionLog(models.Model):
   sessionLogClassCode=models.IntegerField()
   sessionLogSessionCode=models.IntegerField()
   sessionLogStdCode=models.IntegerField()
   sessionLogFaceCode=models.IntegerField()
   sessionLogFaceDes=models.CharField(max_length=6000)
   sessionLogTime=models.IntegerField()

class sessionImage(models.Model):
   sessionImageClassCode=models.IntegerField()
   sessionImageSessionCode=models.IntegerField()
   sessionFakeFileName=models.CharField(max_length=50,default="")
   sessionImageImage=models.CharField(max_length=30)
   sessionImageFaceJson=models.TextField(max_length=65535,default="")
   sessionImageTime=models.IntegerField()