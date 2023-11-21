from django import forms
from django.forms import PasswordInput


class testForm(forms.Form) :
    # title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'style': 'color:#6555df;',"placeholder":"987654321","autocomplete":"off","id":"stdCode","type":"text"}))
class loginForm(forms.Form) :
    stdcode = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'style': 'color:#6555df;',"placeholder":"987654321","autocomplete":"off","id":"stdCode","type":"text"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id":"password","autocomplete":"off","oninput":"handleInputPassword(event)","class":"password","type":"password"}))
class signupForm(forms.Form):
    stdcode= forms.CharField(max_length=10,widget=forms.TextInput(attrs={'style': 'color:#6555df;',"placeholder":"987654321","autocomplete":"off","id":"stdCode","type":"text"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id":"password","autocomplete":"off","oninput":"handleInputPassword(event)","class":"password","type":"password"}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={"id":"password2","autocomplete":"off","oninput":"handleInputPassword(event)","class":"password","type":"password"}))
    firstName= forms.CharField(max_length=100,widget=forms.TextInput(attrs={'style': 'color:#6555df;',"placeholder":"نام شما","autocomplete":"off","id":"stdCode","type":"text"}))
    lastName= forms.CharField(max_length=100,widget=forms.TextInput(attrs={'style': 'color:#6555df;',"placeholder":"نام خانوادگی شما","autocomplete":"off","id":"stdCode","type":"text"}))

class createclassForm(forms.Form):
    className=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'style': 'color:#6555df;',"placeholder":"نام کلاس","autocomplete":"off","id":"className","type":"text"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id":"password","autocomplete":"off","oninput":"handleInputPassword(event)","class":"password","type":"password"}))
    desClass=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'style': 'color:#6555df;',"placeholder":"توضیحات کلاس","autocomplete":"off","id":"desClass","type":"text"}))
class newSessionForm(forms.Form):
    # sesseionName=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'style': 'color:#6555df;',"placeholder":"نام جلسه","autocomplete":"off","id":"sesseionName","type":"text"}))
    # password = forms.CharField(widget=forms.PasswordInput(attrs={"id":"password","autocomplete":"off","oninput":"handleInputPassword(event)","class":"password","type":"password"}))
    # desSession=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'style': 'color:#6555df;',"placeholder":"توضیحات جلسه","autocomplete":"off","id":"desSession","type":"text"}))
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
