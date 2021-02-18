# 즉 이거 하기 전에 내가 app 디렉토리를 만들어야 에러 안남
# sudo docker build .
FROM python:3.7-alpine
# python을 Docker에서 돌릴 때 추천됨
ENV PYTHONUNBUFFERED 1
# 현재 경로에 있는 ./requirements.txt를 도커 내 /requirements.txt에 복사
COPY ./requirements.txt /requirements.txt
# --update는 레지스트리 업데이트(= sudo apt update)
# --no-cache, 레지스트리 인덱스 저장 안함 ==> 패키지 최소화로 설치
## RUN apk add --update --no-cache postgresql-client

# temporary requirements, 맨 처음 할때만 필요
# Dockerfile에 꼭 필요한 디펜던시만
# virtual: 디펜던시 별명 설정
## RUN apk add --update --no-cache --virtual .tmp-build-deps \
# 파이썬 디펜던시 설치를 위한 모든 temporary 디펜던시를 
##    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

# 앱 run할때 기본 명령어 설정하는 것 같은데?
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# 이거 docker-compose에서 command에 넣어놔서 할 필요 없음

# Docker 내에 application source code를 넣을 디렉토리. Dokcer 내 가상 /app
# 즉 이거 하기 전에 내가 app 디렉토리를 만들어야 에러 안남
# 왜냐면 실제 디렉토리에 app을 만든 게 아니거든
RUN mkdir /app


# 만든 app 디렉토리를 메인 work directory로
WORKDIR /app
# 위 COPY랑 똑같은 과정
# 즉 현재 경로 app에서 만들어진 파일을 도커 내에 복사함
COPY ./app app

# 도커 내에서 어플을 돌릴 USER 생성, -D는 app만 돌릴수 있게 권한제한
RUN adduser -D user
# 만든 user를 user로, 이러면 user 뚫려도 root 안 뚫림
USER user
