from django.contrib import admin
from django.urls import path
from main.views import index, blog, posting, new_post

app_name='main'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('blog/', blog, name='blog'),
    # URL:80/blog/숫자 로 접속하면 게시글-세부페이지(posting)
    path('blog/<int:pk>/', posting, name='posting'),
    path('blog/new_post/', new_post, name='new_post'),
]