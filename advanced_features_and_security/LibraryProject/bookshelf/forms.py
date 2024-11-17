from django import forms
from .models import Book

class ExampleForm(forms.Form):
    # Example of a form with a title and description field
    title = forms.CharField(max_length=100, label="Book Title")
    description = forms.CharField(widget=forms.Textarea, label="Description")

    # Optional: You can add a custom validation method
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title should be at least 5 characters long.")
        return title