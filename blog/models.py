from django.db import models
from django.utils import timezone
# Create your models here.


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class Post(models.Model):
    # Link to another model
    author = models.ForeignKey('auth.User')
    # Defines text
    title = models.CharField(max_length=200)
    text = models.TextField()

    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")

    is_active = models.BooleanField(default=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200, default='anon')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def delete(self):
        self.is_active = False
        self.save()

    def undelete(self):
        self.is_active = True
        self.save()

    def __str__(self):
        return self.text


class Me(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    is_active = models.BooleanField(default=True)
