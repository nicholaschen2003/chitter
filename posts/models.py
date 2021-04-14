from django.db import models
from django.contrib.auth.models import User

class Poster(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    poster_name = models.CharField(max_length=200, default=None)
    poster_handle = models.CharField(max_length=200, default=None)
    poster_pfp = models.ImageField(default=None)
    poster_password = models.CharField(max_length=200, default=None)
    liked_posts = models.CharField(max_length=200,default="")

    def __str__(self):
        return self.poster_name

class Post(models.Model):
    poster = models.ForeignKey(Poster, on_delete=models.CASCADE, default=None)
    replying_to = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='reply')
    post_content = models.CharField(max_length=200, default=None)
    pub_date = models.DateTimeField('date published')
    replies = models.IntegerField(default=0)
    retweets = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.post_content
