from django.db import models
from django.utils import timezone

# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Slug
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Markdown
from django.utils.safestring import mark_safe
from markdown_deux import markdown

# For getting absolute url
from django.core.urlresolvers import reverse
from django.http import HttpRequest


# Create your models here.
def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # User data
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=50, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    workplace = models.CharField(max_length=200, blank=True)

    # Social networks
    github_link = models.CharField(max_length=250, blank=True)
    facebook_link = models.CharField(max_length=250, blank=True)
    linkedin_link = models.CharField(max_length=250, blank=True)
    twitter_link = models.CharField(max_length=250, blank=True)
    stackoverflow_link = models.CharField(max_length=250, blank=True)

    def get_markdown_bio(self):
        bio = self.bio
        return mark_safe(markdown(bio))


class Post(models.Model):
    # Link to another model

    author = models.ForeignKey('auth.User')

    # Defines title and gets url from title
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=750)
    slug = models.SlugField(unique=True)

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

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def publish(self):
        self.published_date = timezone.now()
        self.is_active = True
        self.save()

    def get_markdown_text(self):
        return mark_safe(markdown(self.text))

    def set_text_to_markdown(self):
        self.text = markdown(self.plain_text)

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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Recursive function that creates slug
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug

    query_set = Post.objects.filter(slug=slug).order_by("-id")
    exists = query_set.exists()
    if exists:
        new_slug = "%s-%s" % (slug, query_set.first().id)
        return create_slug(instance, new_slug=new_slug)

    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
