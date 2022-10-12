# tweet/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'), # 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결
    path('tweet/', views.tweet, name='tweet'), # 127.0.0.1:8000/tweet 과 views.py 폴더의 tweet 함수 연결
    path('tweet/delete/<int:id>',views.delete_tweet, name='delete-tweet'),
    path('tweet/<int:id>', views.detail_tweet, name='detail-tweet'),
    path('tweet/comment/<int:id>', views.write_comment, name='write-comment'),
    path('tweet/home/comment/<int:id>', views.write_home_comment, name='write-home-comment'),
    path('tweet/comment/delete/<int:id>', views.delete_comment, name='delete-comment'),
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),
    path('tag/<str:tag>', views.TaggedObjectLV.as_view(), name='tagged_object_list'),
    path('post-add/', views.post_add),
    path('post-edit/<int:id>', views.post_edit, name='post-edit'),
    path('tweet/recommend/', views.recommend_view, name='recommend-view'),
    path('tweet/home/<int:id>', views.user_follow, name='user-follow'),   
    path('tweet/<int:id>', views.write_comment, name='write-comment'), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
