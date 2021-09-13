from django.urls import path
from . import views

#app_name = 'anon'
urlpatterns = [
        path('',views.loggin,name='login'),
        path('signup/',views.signup,name='signup'),
        path('home/',views.home,name='home'),
        path('home/like/',views.like_post,name='like'),
        path('home/unlike/',views.unlike_post,name='unlike'),
        path('home/saved/',views.save_post,name='saved'),
        path('home/unsaved/',views.unsave_post,name='unsaved'),
        path('home/cmnt/',views.comment,name='cmnt'),
        path('inbox/',views.chat,name='chat'),
        path('post/',views.post_add,name='post'),
        path('logout/',views.logut,name='logout'),
        path('u/<str:usrname>/',views.profile,name='profile'),
        path('reset/',views.reset_password,name='reset'),
        path('u/<str:usrname>/follow/',views.follow,name='follow'),
        path('u/<str:usrname>/unfollow/',views.unfollow,name='unfollow'),
        path('reset/<str:urn>/',views.reset_link,name='reset_pass'),
]
