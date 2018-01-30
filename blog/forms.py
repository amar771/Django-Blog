from django import forms
from .models import Post
from .models import Comment
from .models import Me


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title',
                  'image',
                  'text',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)


class MeForm(forms.ModelForm):

    class Meta:
        model = Me
        fields = ('text',)
