from django import forms
from .models import Xabar

class XabarForm(forms.ModelForm):
    class Meta:
        model = Xabar
        fields = ["matn"]
