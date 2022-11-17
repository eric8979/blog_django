from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # user auth
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('signout/', views.signoutUser, name='signout'),

    # profile page
    path('profile/<str:pk>', views.updateProfile, name='profile'),
    # about page
    path('about', views.about, name='about'),

    # blog post
    path('post/<str:pk>', views.getPost, name='post'),
    path('post-form', views.createPost, name='create-post' ),
    path('post-update/<str:pk>', views.updatePost, name='update-post' ),
]