from django.contrib import admin
from django.urls import path, include
from markdownx import urls as markdownx

urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('markdownx/', include(markdownx)),
]
