from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from markdownx.models import MarkdownxField

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    objects = UserManager()

    def __str__(self):
        return self.username


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=200, default="Programming")
    gist = models.CharField(max_length=50, default="")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    contents = MarkdownxField()
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user_id")
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="post_id")
    contents = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.contents[0:40]

