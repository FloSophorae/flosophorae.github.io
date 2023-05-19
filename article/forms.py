from django import forms
from .models import Article, ArticleCategory

class NewArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = (
            'father',
            'title',
            'description',
        )
        required = { 'father': False }

class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            'title',
            'category',
            'tags',
            'body',
        )
        required = { 'category': False }
