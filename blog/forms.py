from django import forms
from .models import Post
from .models import Comment
from .models import Profile

from pagedown.widgets import PagedownWidget


class PostForm(forms.ModelForm):

    text = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Post
        fields = ('title',
                  'subtitle',
                  'image',
                  'text',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'style': 'height: 60px'})


class ProfileForm(forms.ModelForm):

    bio = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Profile
        fields = ('bio',)


class ContactForm(forms.Form):

    email = forms.EmailField()
    subject = forms.CharField(max_length=139)
    message = forms.CharField()
    name = forms.CharField(max_length=50, required=False)

    class Meta:
        fields = ('email',
                  'name',
                  'subject',
                  'message',)
