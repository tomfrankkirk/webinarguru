from django.db import models
from textwrap import dedent

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    link = models.URLField()
    hashtags = models.CharField(max_length=200)
    tweet_id = models.BigIntegerField()

    def __str__(self):
        return dedent(f"""
                title: {self.title},
                datetime: {self.datetime},
                link: {self.link},
                hashtags: {self.hashtags},
                tweet_id: {self.tweet_id}.""")

    # ['title', 'datetime', 'link', 'hashtags', 'tweet_id']