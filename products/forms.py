from django import forms
from .models import Product, Comment, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'desc', 'price', 'image']

class QidiruvForm(forms.Form):
    q = forms.CharField(required=False)

class CommitForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']
