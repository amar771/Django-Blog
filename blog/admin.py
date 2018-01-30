from django.contrib import admin
from .models import Post
from .models import Comment
from .models import Me
from .models import Profile

# Register your models here.


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Me)
admin.site.register(Profile)
