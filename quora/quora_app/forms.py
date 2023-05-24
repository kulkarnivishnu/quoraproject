from django import forms
from .models import Question, Answer
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
