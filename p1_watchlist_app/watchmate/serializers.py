from rest_framework import serializers
from .models import WatchList,StreamPlatform,Review

class WatchListSerializer(serializers.ModelSerializer): # Model serializer . Don not need crud method. This is the benefit of model serializers.
    reviews=serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model=WatchList # select Model
        fields='__all__'


class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    # watchlists=WatchListSerializer(many=True,read_only=True)
    
    class Meta:
        model=StreamPlatform
        fields='__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        exclude=('watchlist',) # exclude watchlist field from review list serializer