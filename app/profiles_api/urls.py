from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles_api import views

# ViewSet은 router라는 놈으로 url에 연결한다.
router = DefaultRouter()
# 연결할 url 이름, base_name은 url 가져올때 사용됨
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
""" router가 연결이 되면 ViewSet과 관련된 url의 리스트를 만든다
그 리스트기 router.urls고 밑에서 include해주는 것 """

""" viewset에 queryset이 정해져있으면 그 query가 타겟으로 한 모델을 보고
쟝고 drf가 모델을 알아채기 때문에 base_name 줄 필요 없다.
즉 queryset이 없거나 viewset을 override하고싶을떄만 base_name을 준다 """
router.register('profile', views.UserProfileViewSet)
router.register('feed', views.UserProfileFeedViewSet)


# controller와 service를 연결
urlpatterns = [
    # view 클래스를 해당 url에 render
    # 이게 NestJS의 controller - service이랑 다른 점
    # as_view()로 html로 render해서 Postman 역할을 한다
    path('hello-view/', views.HelloAPIView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls))
]
