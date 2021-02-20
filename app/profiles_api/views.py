""" When to user APIViews?
Need full control over the logic
Processing files and rendering asynchronous respone
Calling other APIs / Services
Accessing local files or data
returns a response """
from rest_framework.views import APIView
# View로부터 response를 얻어옴
from rest_framework.response import Response
from rest_framework import status
from profiles_api import serializers


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
