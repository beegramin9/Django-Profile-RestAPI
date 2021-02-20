""" Post, Put, Patch, Delete 처럼
DB와의 인터랙션이 필요한 API를 위해
DB 데이터 <-> JSON 데이터로 변환 
이 뿐만 아니라 NestJS의 DTO처럼 
validation 역할도 수행한다
"""
from rest_framework import serializers


class HelloSerializers(serializers.Serializer):
    """ Serializes a name field for testing our APIView """
    # Post, Put, Patch, Delete에 쓸 Field만 인풋으로 받으면 끝

    # DTO 역할. name은 max_length가 10입니다!

    name = serializers.CharField(max_length=10)
