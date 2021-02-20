""" When to user APIViews?
Need full control over the logic
Processing files and rendering asynchronous respone
Calling other APIs / Services
Accessing local files or data
returns a response """
from rest_framework.views import APIView
# View로부터 response를 얻어옴
from rest_framework.response import Response
# Create your views here.


class HelloAPIView(APIView):
    """ Test API View """

    def get(self, request, format=None):
        """ Return a list of APIView features """
        an_apiview = [
            'Users HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a tradiational Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs'
        ]
        return Response({'message': "Hello", 'an_apiview': an_apiview})
