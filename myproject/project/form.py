from django import forms
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of the News'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Content of the News'}),
        }