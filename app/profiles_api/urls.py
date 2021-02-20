from django.urls import path
from profiles_api import views

# controller와 service를 연결
urlpatterns = [
    # view 클래스를 해당 url에 render
    path('hello-view/', views.HelloAPIView.as_view()),
]
