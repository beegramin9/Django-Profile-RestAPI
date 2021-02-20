from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles_api import views

# ViewSet은 router라는 놈으로 url에 연결한다.
router = DefaultRouter()
# 연결할 url 이름, base_name은 url 가져올때 사용됨
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
""" router가 연결이 되면 ViewSet과 관련된 url의 리스트를 만든다
그 리스트기 router.urls고 밑에서 include해주는 것 """

# controller와 service를 연결
urlpatterns = [
    # view 클래스를 해당 url에 render
    # 이게 NestJS의 controller - service이랑 다른 점
    # as_view()로 html로 render해서 Postman 역할을 한다
    path('hello-view/', views.HelloAPIView.as_view()),
    path('', include(router.urls))
]
