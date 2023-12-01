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

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
class newSessionForm(forms.Form):
    # file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}))
    file_field = MultipleFileField()
class makeClassPresentForm(forms.Form) :
    classCode = forms.IntegerField(widget=forms.TextInput(attrs={'style': 'color:#6555df;',"placeholder":"کد کلاس","autocomplete":"off","id":"className","type":"text"}))
    classPass = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'style': 'color:#6555df;',"placeholder":"رمز کلاس","autocomplete":"off","id":"className","type":"text"}))
    userFace = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'style': 'color:#6555df;',"placeholder":"شماره چهره","autocomplete":"off","id":"className","type":"text"}))
    