from django.shortcuts import render,redirect
from .models import WatchList,StreamPlatform,Review
from django.http import HttpResponse,JsonResponse
from rest_framework import viewsets,views,filters
from .serializers import WatchListSerializer,StreamPlatformSerializer,ReviewListSerializer
from rest_framework import decorators,response,status,mixins,generics,serializers,permissions
from .permission import AdmimOrReadOnly,ReviewUserOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from .throttling import ReviewCreateThrottle,ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import WatchListPagination,ReviewListPagination


# Create your views here.

class movie_list(views.APIView):
    # permission_classes=[permissions.IsAuthenticated]
    throttle_classes=[UserRateThrottle,AnonRateThrottle]
    def get(self,request): # instead of get condition and can not use if serializer.is_valid() in get method
        movies=WatchList.objects.all()
        serializer=WatchListSerializer(movies,many=True)
        return response.Response(serializer.data)
        
    def post(self,request): 
        serializer=WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors)


class movie_detail(views.APIView):
    permission_classes=[AdmimOrReadOnly]
    def get(self,request,pk): # r = read operation
        movie=WatchList.objects.get(pk=pk)
        serializer=WatchListSerializer(movie)
        return response.Response(serializer.data)
    
    def post(self,request): # c = create operation
        serializer=WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors)
        
    def put(self,request,pk): # u = update operation
        movie=WatchList.objects.get(pk=pk)
        serializer=WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
            # return redirect('movie_list')
        else:
            return response.Response(serializer.errors)
            # return redirect('movie_detail')    
        
    def delete(self,request,pk): # d = delete operation
            movie=WatchList.objects.get(pk=pk)
            movie.delete()
            return redirect('movie_list')



class StreamListAV(views.APIView):
    # permission_classes=[AdmimOrReadOnly]
    def get(self,request):
        platform=StreamPlatform.objects.all()
        serializer_class=StreamPlatformSerializer(platform,many=True,context={'request': request})
        return response.Response(serializer_class.data)
    def post(self,request):
        serializer=StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors)
        

class StreamDetailAV(views.APIView):
    permission_classes=[AdmimOrReadOnly]
    def get(self,request,pk):
        stream=StreamPlatform.objects.get(pk=pk)
        serializer=StreamPlatformSerializer(stream,context={'request': request})
        return response.Response(serializer.data)        


class CreateReview(generics.CreateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ReviewListSerializer
    throttle_classes=[ReviewCreateThrottle]
    # queryset=Review.objects.all()
    def get_queryset(self):
        pk=self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)
    def perform_create(self,serializer):
        pk=self.kwargs.get('pk')
        watchlist=WatchList.objects.get(pk=pk)
        review_user=self.request.user
        review_queryset=Review.objects.filter(watchlist=watchlist,review_user=review_user)
        if review_queryset.exists():
            raise serializers.ValidationError("You have already reviewed this movie")
        
        if watchlist.number_rating==0:
            watchlist.avg_rating=serializer.validated_data['rating']
        else:
            watchlist.avg_rating=(watchlist.avg_rating+serializer.validated_data['rating'])/2    

        watchlist.number_rating=watchlist.number_rating+1
        watchlist.save()
        serializer.save(watchlist=watchlist,review_user=review_user)

        
class ReviewList(generics.ListCreateAPIView): #ListAPIView with CreateAPIView is a class based view that provides get and post method handlers.
    permission_classes=[ReviewUserOrReadOnly]
    # throttle_classes=[ReviewListThrottle]
    queryset=Review.objects.all()
    pagination_class=ReviewListPagination
    serializer_class=ReviewListSerializer
    filter_backends=[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields=['review_user__username','active']
    search_fields=['review_user__username','rating']
    ordering_fields=['rating','created','updated']
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView): # RetrieveUpdateDestroyAPIView is a class based view that provides get, put, patch and delete method handlers.
    permission_classes=[ReviewUserOrReadOnly]
    queryset=Review.objects.all()
    serializer_class=ReviewListSerializer



class UserReviewDetail(generics.ListAPIView):
    serializer_class=ReviewListSerializer
    def get_queryset(self):
        review_user=self.kwargs['username']
        return Review.objects.filter(review_user__username=review_user)    