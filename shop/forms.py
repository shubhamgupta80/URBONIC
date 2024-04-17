from .models import Product, Review, Article
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['title', 'image', 'description', 'price', 'category', 'available', 'best_seller', 'seller']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'user', 'description', 'rating']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text']
        widgets = {
            'text': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
                config_name="content"),
        }