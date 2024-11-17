from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_date']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        # You can add more validation here if needed
        return title
