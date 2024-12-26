from django.db import models

# Create your models here.

class StreamPlatform(models.Model):
    name=models.CharField(max_length=30)
    about=models.CharField(max_length=150)
    website=models.URLField(max_length=40)
    def __str__(self):
        return self.name
    
class WatchList(models.Model):
    title=models.CharField(max_length=40)
    storyline=models.CharField(max_length=40)
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    platform=models.ManyToManyField(StreamPlatform, blank=True,related_name="watchlist")
    # platform=models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,related_name="watchlist")

    def __str__(self):
        return self.title    
    
    
    