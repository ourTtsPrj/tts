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
    password2= forms.CharField(widget=forms.PasswordInput(attrs={"id":"password","autocomplete":"off","oninput":"handleInputPassword(event)","class":"password","type":"password"}))
