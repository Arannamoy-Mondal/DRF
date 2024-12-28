from django.shortcuts import render
from django.urls import URLPattern,include,path
from .views import movie_list,movie_detail,StreamListAV,StreamDetailAV,ReviewAV,ReviewList,ReviewDetail
urlpatterns=[
    path('watch/',movie_list.as_view(),name='movie-list'),
    path('watch/<int:pk>',movie_detail.as_view(),name='movie-detail'),  # it searches for specific id
    path('stream/',StreamListAV.as_view(),name='stream-list'),
    path('stream/<int:pk>',StreamDetailAV.as_view(),name='streamplatform-detail'),
    path('review/',ReviewAV.as_view(),name='review-list'), # review list for all movies
    path('review/<int:pk>',ReviewDetail.as_view(),name='review-detail'), # review list for specific movie
]