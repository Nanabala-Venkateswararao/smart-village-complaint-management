from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Complaint

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True, label="Full name")

    class Meta:
        model = User
        fields = ["username", "first_name", "email", "password1", "password2"]

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["title", "category", "village_location", "description", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }

class OfficialUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["status", "official_response"]
        widgets = {
            "official_response": forms.Textarea(attrs={"rows": 4}),
        }
