# from django import forms
# # from django.contrib.auth.models import User 
# from airtalesapp.models import User, Profile

# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     class Meta:
#         model = User
#         fields = ('email','username', 'password',)

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('userID',)

# class LoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class UserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ()#('userID',)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

