from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class tweet(models.Model):
      text=models.TextField(max_length=28,default='')
      datetime=models.DateTimeField(default=timezone.now)
      uname=models.ForeignKey(User,on_delete=models.CASCADE)
      likes= models.IntegerField(default=0)
      dislikes= models.IntegerField(default=0)

      
      def __str__(self):
        return self.text[:5]

      @property
      def number_of_comments(self):
        return Comment.objects.filter(post_connected=self).count()

class Comment(models.Model):
    content = models.TextField(max_length=150)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(tweet, on_delete=models.CASCADE)
    
    



class Preference(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    tweet= models.ForeignKey(tweet, on_delete=models.CASCADE)
    value= models.IntegerField()
    date= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.user) + ':' + str(self.tweet) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "tweet", "value")
      
