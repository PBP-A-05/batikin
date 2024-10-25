from django import forms
from .models import Product, Review

class ProductEntryForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image_urls']  # Only include Product fields here

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'rating', 'review']  # Use Review fields here
