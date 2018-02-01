from django import forms
from .models import Post
from .models import Comment
from .models import Profile


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


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio',
                  'location',
                  'birth_date',
                  'workplace',
                  'github_link',
                  'facebook_link',
                  'linkedin_link',
                  'twitter_link',
                  'stackoverflow_link',)
