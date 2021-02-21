""" When to user APIViews?
Need full control over the logic
Processing files and rendering asynchronous respone
Calling other APIs / Services
Accessing local files or data
returns a response """
from rest_framework.views import APIView
from rest_framework import viewsets
# View로부터 response를 얻어옴
from rest_framework.response import Response
from rest_framework import status

from profiles_api import serializers
from profiles_api import models
# Nest처럼 복잡한 로직 + DB 인터랙션 쓰려면
# API View 써야 함

# permission
from profiles_api import permissions
# Nest처럼 bearer Token이랑 똑같은 개념
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters


class HelloAPIView(APIView):
    """ Test API View """
    # JSON변환 + DTO 적용
    # 이름 그대로 써야함
    serializer_class = serializers.HelloSerializers

    def get(self, request, format=None):
        """ Return a list of APIView features """
        an_apiview = [
            'Users HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a tradiational Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs'
        ]
        # 뿌려주는 Response에 들어갈 데이터, 딕셔너리 형태로
        return Response({'message': "Hello", 'an_apiview': an_apiview})

    def post(self, request):
        """ Create a hello message with out name """
        # request.data = post request로 들어온 데이터
        serializer = self.serializer_class(data=request.data)

        # DTO 맞게 들어와서 validation 됐을땐 비즈니스로직 실행
        if serializer.is_valid():
            # validated된 field를 가져옴
            name = serializer.validated_data.get('name')
            message = f"Hello {name}"
            return Response({"message": message})
        # DTO 틀리면 404 에러. verbose하게 에러를 전달하기떄문에
        # 다른 개발자가 보기 편하다.
        # 200은 따로 없다. Response의 디폴트가 200이기 떄문
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """ Put vs Patch
    이름, 성 중에 Patch로 이름만 바꾸면 성은 남아있음
    Put은 object를 아예 바꾸기 때문에 이름만 바꾸면 성이 없어짐(이름만 들어옴) """

    def put(self, request, pk=None):
        """ Handle updating an object """
        # put 요청엔 일반적으로 primary key로 update할 id의 object를 매치
        # 여기선 object id가 없으니 None
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """ Handle a partial update of an object """
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """ Delete an object """
        return Response({'method': 'DELETE'})

# 미리 빌트인된 service 함수들. 즉 정해져있던거야


class HelloViewSet(viewsets.ViewSet):
    """ Test API ViewSet """
    # ViewSet에서도 사용가능
    serializer_class = serializers.HelloSerializers
    # ViewSet의 빌트인 함수들

    # 전체 다가지고 오는
    def list(self, request):
        """ Return a hello message """
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLS using routers',
            'Provides more functionality with less code'
        ]
        return Response({'message': 'hello', 'a_viewset': a_viewset})

    def create(self, request):
        """ Create a new hello message """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f"Hello {name}"
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # where절로 가져오는
    def retrieve(self, request, pk=None):
        """ Handle getting an object by its ID """
        return Response({'http_method': 'GET'})

    # Put이나 Patch가 보이지 않는 이유는
    # 저 두개는 특정한 object를 업뎃하는거니까 pk(id)를 예상하는데
    # 그냥 /api/hello-viewset으로 들어가면 안됨
    def update(self, request, pk=None):
        """ Handle updating an object """
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """ Handle updating part of an update """
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """ Handle removing an object """
        return Response({'http_method': "DELETE"})

# Model ViewSet 사용. 일반 ViewSet이랑 비슷한데
# Model 관리에 트과되어있음


class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handle creating and updating profiles """
    serializer_class = serializers.UserProfileSerializer
    # 쟝고 ORM
    queryset = models.UserProfile.objects.all()
    # 사용할 authentication 방법들 튜플이어야 함.
    authentication_classes = (TokenAuthentication,)
    # permission 줄 방법. 내가 만든 커스텀 퍼미션 사용
    # 매 api request마다 사용됨
    permission_classes = (permissions.UpdateOwnProfile,)
    # search 기능을 수행하는 filter
    filter_backends = (filters.SearchFilter,)
    # 어떤 field을 searchable하게 할건데?
    search_fields = ('name', 'email')
