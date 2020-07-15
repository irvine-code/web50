from django.urls import path
from . import views 
from .views import TweetListView,TweetCreateView,TweetUpdateView,TweetDeleteView,postpreference,PostDetailView,UserPostListView,FollowsListView, FollowersListView,AllListView
    
    

urlpatterns = [
   path('',TweetListView.as_view(),name='home'),
   path('create',TweetCreateView.as_view(),name='tweetcreate'),
   path('alltweets',AllListView.as_view(),name='alltweets'),
   path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
   path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
   path('tweet/<int:pk>/update',TweetUpdateView.as_view(),name='tweetupdate'),
   path('tweet/<int:pk>/delete',TweetDeleteView.as_view(),name='tweetdelete'),
   path('user/<str:username>/follows', FollowsListView.as_view(), name='user-follows'),
   path('user/<str:username>/followers', FollowersListView.as_view(), name='user-followers'),
   path('post/<int:tweetid>/preference/<int:userpreference>', postpreference, name='postpreference'),
]