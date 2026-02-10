from django import forms
from .models import CustomUser, Xabar

class ProfilForm(forms.ModelForm):
    class Meta:
        model =  CustomUser
        fields = ["username", "email", "image", "password"]


class XabarForm(forms.ModelForm):
    class Meta:
        model = Xabar
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={
                "rows": 2,
                "placesholder": "Xabar yozing....",
                "class": "chat-input"
            })
        }

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    phone = forms.CharField(max_length=120)
    addres = forms.CharField(max_length=150)
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={'rowss':3}))
