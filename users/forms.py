from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from quiz_app.models import User
#**********************************************************************************
class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']
		labels = {'image' : 'پروفایل:'}

class UserCreationForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ("username", "first_name", "last_name")