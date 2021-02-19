# profiles의 모든 model을 모아놓는 게 제일 좋다.
from django.db import models
# Override(=customize)할 때 필요한 모듈
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# BaseUserManager: 디폴트 User model을 위한 쟝고 default model manager
# 일반 모델의 매니저는 models.Manager
# 모델 매니저는 데이터베이스 쿼리와 연동되는 인터페이스
# 각 모델은 애플리케이션에서 최소 하나의 매니저를 가진다.
# 디폴트 모델 매니저의 이름은 objects이다.
# objects를 set해줘야 모델에 쟝고 ORM 사용 가능
from django.contrib.auth.models import BaseUserManager

# for 쟝고 CLT에서 custom model을 사용
# custom manager 설치 필요


class UserProfileManager(BaseUserManager):
    """ 쟝고 ORM에서 사용될 수 있는 함수들을 customizing """

    def create_user(self, email, name, password=None):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address.')

        # normalizing: @ 이후를 전부 lowercase로
        # 여기 self는 다른게 아니라 문법적으로 UserProfileManager가 맞음
        # 즉 BaseUserManager의 normalize_email 메소드
        email = self.normalize_email(email)

        """ 여기 model도 BaseUserManager의 메소드
        Manager가 target하는 모델, 즉 UserProfile
        그럼 이제 user 변수에 UserProfile이 들어가는 것
        필드값 넣어주면 됨 """
        user = self.model(email=email, name=name)
        """ 이제부턴 UserProfile의 메소드 """
        # encryption, PermissionsMixin메소드
        user.set_password(password)
        # AbstractBaseUser메소드, 모든 DB table(model, entity)에 있는 기능
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """ Creata and save a new superuser with given details """
        # 여기는 왜 self 없어?
        # 같은 클래스의 다른 메소드 쓰는 건데
        # 이땐 필요없음
        # create_user가 user=UserProfile을 리턴함
        user = self.create_user(email, name, password)
        # PermissionMixin
        user.is_superuser = True

        user.is_staff = True
        user.save(using=self._db)
        return user

# 이 custom 모델을 사용하려면 settings.py에서


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Model(= DB Table/Entity)"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    """ for 쟝고 admin, authentication """
    # 기본 ID name => email 변경
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserProfileManager()

    """ Model manager(= DB Repository) """

    def get_full_name(self):
        """ Retrieve full name of user """
        return self.name

    def get_short_name(self):
        """ Retrieve short name of user """
        return self.name

    def __str__(self):
        """ String representation of the model
        <__main__.MyRepr object at 0x100656cc0>같은 객체를 나타내는 표현을
        return 값으로 대체한다. """
        return self.email
