from django import forms
from app.models import Comment,Post
from django.contrib.auth.models import User

class emailform(forms.Form):
    name=forms.CharField()
    to=forms.EmailField()
    fromm=forms.EmailField(label='From')
    comments=forms.CharField(required=False,widget=forms.Textarea)


class add_post(forms.ModelForm):
    class Meta:
        model=Post
        exclude=('created','updated','publish','status',)

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    email=forms.EmailField()
    class Meta:
        model=User
        fields=('username','email','password')
