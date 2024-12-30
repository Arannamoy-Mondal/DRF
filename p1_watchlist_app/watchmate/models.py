from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator 
from django.contrib.auth.models import User
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
    platform=models.ManyToManyField(StreamPlatform,related_name="watchlists")
    # review=models.ManyToManyField(Review,on_delete=models.CASCADE,related_name="reviews_only",null=True)
    # platform=models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,related_name="watchlist")

    def __str__(self):
        return self.title    
    

class Review(models.Model):
    review_user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])    
    description=models.TextField(max_length=200,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    watchlist=models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name="reviews")
    def __str__(self):
        return str(self.rating) + " | " + self.description
    
    
    