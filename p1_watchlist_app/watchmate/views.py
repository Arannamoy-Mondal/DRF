from django.shortcuts import render,redirect
from .models import WatchList,StreamPlatform,Review
from django.http import HttpResponse,JsonResponse
from rest_framework import viewsets,views
from .serializers import WatchListSerializer,StreamPlatformSerializer,ReviewListSerializer
from rest_framework import decorators,response,status,mixins,generics

# Create your views here.

class movie_list(views.APIView):

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
    def get(self,request,pk):
        stream=StreamPlatform.objects.get(pk=pk)
        serializer=StreamPlatformSerializer(stream,context={'request': request})
        return response.Response(serializer.data)        


class ReviewAV(views.APIView):
    def get(self,request):
        review=Review.objects.all()
        serializer=ReviewListSerializer(review,many=True)
        return response.Response(serializer.data)
    def post(self,request):
        serializer=ReviewListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors)
        
class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewListSerializer
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)
    
class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewListSerializer
    def get(self,request,pk):
        return self.retrieve(request)
    def put(self,request,pk):
        return self.update(request,pk)