from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from feedback import views
from django.urls import path, include

urlpatterns = [
    path('video/', views.SnippetList.as_view()),
    path('form/', views.FormList.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)