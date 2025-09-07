from django import forms
from core.models import *
from django.core.exceptions import ValidationError


# ------------------------------------post form---------------------------------
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'picture', 'content', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
            'content': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


# ---------------------------------Category Form---------------------------------
class CategoryForm(forms.ModelForm):
    cat_name = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Category
        fields = ('cat_name',)

    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        cat_name = cleaned_data.get("cat_name")
        if Category.objects.filter(cat_name=cat_name).exists():
            raise ValidationError("Category Already exists !")


# ---------------------------------Comment Form------------------------------------
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'md-textarea form-control',
            'placeholder': 'Type here ...',
            'rows': '3',
            'Style': 'resize:none;'
        }))

    class Meta:
        model = Comment
        fields = ('content',)


# ----------------------------------Reply Form----------------------------------------
class ReplyForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'md-textarea form-control',
            'placeholder': 'comment here ...',
            'rows': '1',
        }))

    class Meta:
        model = Comment
        fields = ('content',)


# --------------------------------ForbiddenWords Form--------------------------------
class ForbiddenWordsForm(forms.ModelForm):
    forbidden_word = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = ForbiddenWords
        fields = ('forbidden_word',)

    def clean(self):
        cleaned_data = super(ForbiddenWordsForm, self).clean()
        forbidden_word = cleaned_data.get("forbidden_word")
        if ForbiddenWords.objects.filter(forbidden_word=forbidden_word).exists():
            raise ValidationError("This Word Already exists !")

