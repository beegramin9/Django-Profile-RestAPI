""" Post, Put, Patch, Delete 처럼
DB와의 인터랙션이 필요한 API를 위해
DB 데이터 <-> JSON 데이터로 변환 
이 뿐만 아니라 NestJS의 DTO처럼 
validation 역할도 수행한다

Create/Update()로 Object instance 반환 가능
기본이 제공되는데 굳이 한번 더 쓴다는 것은 override한다는 것
"""
from rest_framework import serializers
from profiles_api import models


class HelloSerializers(serializers.Serializer):
    """ Serializes a name field for testing our APIView """
    # Post, Put, Patch, Delete에 쓸 Field만 인풋으로 받으면 끝

    # DTO 역할. name은 max_length가 10입니다!

    name = serializers.CharField(max_length=10)


# 쟝고 DB 모델과 연결되는 시리얼라이저. DTO validation 쉽다
# 디폴트 create 함수를 제공하는데 이건 pw 해쉬 안함, override 가능

# 모델이랑 연결해서 쓰려면 그냥 Serializer가 아니라 ModelSerializer 써야 함
class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializes a user profile object """
    # Meta 클래스는 serializer가 어떤 모델을 대상으로 하는지 configure
    class Meta:
        model = models.UserProfile
        # validation할 field 명시
        fields = ('id', 'email', 'name', 'password')
        # password는 write only만, 회원들이 pw hash를 받을 수 있음 안됨
        extra_kwargs = {
            'password': {
                'write_only': True,  # Get으로 pw 얻기 불가
                'style': {'input_type': 'password'}  # input할때 안보임, ***으로 보임
            }
        }

    # validated_data: DTO를 통과한 데이터 object
    # override
    def create(self, validated_data):
        """ Create and return a new user """
        # 쟝고 ORM
        # objects를 붙여야 모델을 객채화해서 메소드와 속성을 가지고 올 수 있다
        # create_user 메소드는 models.py에서 커스터마이즈함
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """ Handle updating user account """
        if 'password' in validated_data:
            # password만 빼서 변수에 저장하고 리스트 저장
            password = validated_data.pop('password')
            instance.set_password(password)
        # 부모 클래스의 update 메소드 사용
        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """ Serializes profile feed items """
    class Meta:
        model = models.ProfileFeedItem
        # 모델에 id 필드가 없어도 id를 여기서 주면 primary key로 줄 수 있다
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        """ 사용자가 새 feed를 만들고 그걸 다른 사용자에게 assign하지 못하게 해야함 """
        extra_kwargs = {'user_profile_field': {'read_only': True}}
