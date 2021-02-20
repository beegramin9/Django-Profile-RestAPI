from django.urls import path
from profiles_api import views

# controller와 service를 연결
urlpatterns = [
    # view 클래스를 해당 url에 render
    # 이게 NestJS의 controller - service이랑 다른 점
    # as_view()로 html로 render해서 Postman 역할을 한다
    path('hello-view/', views.HelloAPIView.as_view()),
]
