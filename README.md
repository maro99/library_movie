## 도서관 무료영화 관람정보 제공 프로젝트  

---  
&nbsp;

### Introduction  
#### 서울시 50여개 도서관 의 무료 상영 정보 제공을 위한 웹 페이지를 제작하는 프로젝트 입니다. 

---  
&nbsp;

### Project URL

- API SERVER URL :  https://api.maro5.com  
- FRONT WEB URL  :  https://maro5.com  
- APP DOCUMENT : https://library-movie.gitbook.io/project/
---  
&nbsp;

### Stacks   

`Python`, `Django`,  `DRF(Django REST framework)`,  `AWS RDS`,  `AWS ElasticBeanstalk`, `AWS ElasticCache`,`AWS Route 53`, `Docker`,`Nginx`, `uWSGI`, `Celery`,`Sentry`,`html`,`jquery`,`Ajax`

---  
&nbsp;

### 주요내용   

* celery beat 스케줄링 기능 이용해서 20여개각 도서관 홈페이지 에서 영화 상영정보 매일 정해진 시간에 크롤링 후 db에 업데이트 

* 회원의 상영 영화에 대한 찜 여부 체크하여 상영 임박한 영화에 대해서 매 시간 알람 메일 발송 

* 회원 가입 절차 중 인증메일 발송시 celery이용해서 비동기적으로 task 처리 

* Google Api 이용해서 구글 로긴 기능 구현 

* 이메일 및 sms 인증 코드 발송 통해 회원정보 수정 

* Django Rest Framework 활용하여 api-view 작성 및 gitbook으로 업데이트 정보 관리 

* 기본적인 javascript, css. html 이용해서 프론트엔드웹 개발 (프래임워크 사용x) 
(프론트 저장소 https://github.com/maro99/library_movie_frontend) 

* Ajax이용하여 영화에 대한 찜하기 클릭시 요청을 비동기적으로 처리 

* 백엔드 API 서버와 프론트엔드 프로젝트 Elastic Beanstalk 이용해서 동시에 배포 


* Sentry 적용 하여 배포,크롤링 및 유저 사용 시 오류 보고  

* 개발 환경 분리(local/dev/production)  
   - loccal-> local redis, PostgreSQL  
     
   - dev -> local redis, AWS RDS 
   - production ->ElastiCache redis,  AWS RDS

---  
&nbsp;

### Requirements   

``` 
amqp==2.4.2
attrs==19.1.0
backcall==0.1.0
beautifulsoup4==4.7.1
billiard==3.5.0.5
bleach==3.1.0
boto3==1.9.142
botocore==1.12.142
celery==4.1.1
certifi==2019.3.9
chardet==3.0.4
coolsms-python-sdk==2.0.3
decorator==4.4.0
defusedxml==0.6.0
django-allauth==0.39.1
django-celery-beat==1.4.0
django-celery-results==1.0.4
django-cors-headers==2.5.3
django-storages==1.7.1
django-timezone-field==3.0
django==2.2.1
djangorestframework==3.9.3
docutils==0.14
entrypoints==0.3
idna==2.8
ipykernel==5.1.0
ipython-genutils==0.2.0
ipython==7.5.0; python_version >= '3.3'
ipywidgets==7.4.2
jedi==0.13.3
jinja2==2.10.1
jmespath==0.9.4
jsonschema==3.0.1
jupyter-client==5.2.4
jupyter-console==6.0.0
jupyter-core==4.4.0
jupyter==1.0.0
kombu==4.5.0
lxml==4.3.3
markupsafe==1.1.1
mistune==0.8.4
nbconvert==5.5.0
nbformat==4.4.0
notebook==5.7.8
oauthlib==3.0.1
pandocfilters==1.4.2
parso==0.4.0
pexpect==4.7.0; sys_platform != 'win32'
pickleshare==0.7.5
pillow==6.0.0
prometheus-client==0.6.0
prompt-toolkit==2.0.9
psycopg2-binary==2.8.2
ptyprocess==0.6.0; os_name != 'nt'
pygments==2.3.1
pyrsistent==0.15.1
python-crontab==2.3.6
python-dateutil==2.8.0
python3-openid==3.1.0
pytz==2019.1
pyzmq==18.0.1
qtconsole==4.4.4
redis==3.2.0
requests-oauthlib==1.2.0
requests==2.21.0
s3transfer==0.2.0
selenium==3.141.0
send2trash==1.5.0
sentry-sdk==0.7.14
six==1.12.0
soupsieve==1.9.1
sqlparse==0.3.0
terminado==0.8.2
testpath==0.4.2
tornado==6.0.2
traitlets==4.3.2
urllib3==1.24.3; python_version >= '3.4'
uwsgi==2.0.18
vine==1.3.0
wcwidth==0.1.7
webencodings==0.5.1
widgetsnbextension==3.4.2
``` 
---   
&nbsp;
  
  
### Secrets  
#####  .secrets/base.json  
```
{
  "SECRET_KEY" : "<Django settings SECRET_KEY value>",
  "AWS_ACCESS_KEY_ID":"<AWS_ACCESS_KEY value> ",
  "AWS_SECRET_ACCESS_KEY":"<AWS_SECRET_ACCESS_KEY value>",
  "AWS_DEFAULT_ACL":"private",
  "AWS_S3_REGION_NAME":"ap-northeast-2",
  "AWS_S3_SIGNATURE_VERSION":"s3v4",
  "SUPERUSER_USERNAME":"<superuser username>",
  "SUPERUSER_EMAIL":"<superuser user-email>",
  "SUPERUSER_PASSWORD":"<superuser user-password>",
  "FACEBOOK_APP_ID":"<FACEBOOK_APP_ID>",
  "FACEBOOK_APP_SECRET_CODE":"<FACEBOOK_APP_SECRET_CODE>",
  "KAKAOTALK_NATIVE_APP_KEY":"<KAKAOTALK_NATIVE_APP_KEY>",
  "KAKAOTALK_REST_API_KEY":"<KAKAOTALK_REST_API_KEY>",
  "NAVER_CLIENT_ID" : "<NAVER_CLIENT_ID>",
  "NAVER_CLIENT_SECRET" : "<NAVER_CLIENT_SECRET>",
  "GOOGLE_CLIENT_ID" : "<GOOGLE_CLIENT_ID>",
  "GOOGLE_CLIENT_SECRET" : "<GOOGLE_CLIENT_SECRET>",
  "API_GOOGLE_CLIENT_ID" : "<API_GOOGLE_CLIENT_ID>",
  "API_GOOGLE_CLIENT_SECRET" : "<API_GOOGLE_CLIENT_SECRET>",
  "EMAIL_BACKEND" : "django.core.mail.backends.smtp.EmailBackend",
  "EMAIL_USE_TLS" : "True",
  "EMAIL_PORT" : "587",
  "EMAIL_HOST" : "smtp.gmail.com",
  "EMAIL_HOST_USER" : "<EMAIL_HOST_USER>",
  "EMAIL_HOST_PASSWORD" : "<EMAIL_HOST_PASSWORD>",
  "SERVER_EMAIL" : "<SERVER_EMAIL_ADRESS>",
  "DEFAULT_FROM_MAIL" : "<DEFAULT_FROM_MAIL_ADRESS>",
  "AWS_ELASTIC_CACHE":"<AWS_ELASTIC_CACHE END POIN>",
  "SMS_API_KEY":"<SMS_API_KEY>",
  "SMS_API_SECRET" :"<SMS_API_SECRET>"
}
```

##### .secrets/dev.json  
```
{
  "DATABASES": {
    "default": {
      "ENGINE": "django.db.backends.postgresql",
      "HOST": "<Aws RDS ADRESS>",
      "PORT": 5432,
      "USER": "<DB username>",
      "PASSWORD": "<DB user password>",
      "NAME": "<DB name>"
    }
  },
  "AWS_STORAGE_BUCKET_NAME":"<AWS_STORAGE_BUCKET_NAME>"
}
```  
#####  .secrets/production.json  
```
{
  "ALLOWED_HOSTS" : <ALLOWED HOST STRING LIST>,
    "DATABASES": {
    "default": {
      "ENGINE": "django.db.backends.postgresql",
      "HOST": "<Aws RDS ADRESS>",
      "PORT": 5432,
      "USER": "<DB username>",
      "PASSWORD": "<DB user password>",
      "NAME": "<DB name>"
    }
  },
  "AWS_STORAGE_BUCKET_NAME":"<AWS_STORAGE_BUCKET_NAME>",
  "SENTRY_DNS":"https://<sentry_Client_Keys>""
}

```

---  
&nbsp;
  
  
### Installation  

    pipenv install  
---  
&nbsp;

### Running
#####  local + runserver  
```
# Move project`s directory
- pipenv install
- pipenv shell
- cd app
- export DjANGO_SETTINGS_MODULE=config.settings.local
- `./manage.py runserver`
```
#####  dev + runserver  
```
# Move project`s directory
- pipenv install
- pipenv shell
- cd app
- export DjANGO_SETTINGS_MODULE=config.settings.dev
- `./manage.py runserver`
```  

-Docker 사용시에는 Dockerfile.bas 빌드 후 dockerhub에 이미지 push후에 각 local, dev, production의  DOCKERFILE에서 `FROM` 으로 가져와서 사용   
#####  build Dockerfile.base  &  upload docker hub 
 ```
 python build -m base  
           # 원본이되는것                   # 새로생성할 것 
docker tag eb-docker:base nadcdc/movie-eb-docker:base  
docker login
docker push nadcdc/movie-eb-docker      
 ```
 

 #####  local + docker  

```
python build -m local  
docker run --rm -it -p 9994:8000 eb-docker:local 
```
##### dev + docker   
```  
python build -m dev  
docker run --rm -it -p 9994:8000 eb-docker:dev 
```
##### dev + docker( Front& Backend Deploy)  
 ```
 python multi_deploy_dev.sh  
 docker run --rm -it -p 8888:7000 multi-deploy  
 ```
##### production + docker  
```  
python build -m production  
docker run --rm -it -p 9994:8000 eb-docker:production 
```
##### production + ElasticBeanstalk(Backend)  
```  
python deploy.sh
```

##### production + ElasticBeanstalk( Front& Backend Deploy)  

```
python multi_deploy_eb.sh
```

---  


&nbsp;

### DockerHub

    
    docker build -t yapen-docker:base -f Dockerfile.base
    docker tag yapen-docker:base <자신의 사용자명>/<저장소명>:base

    docker push <자신의 사용자명>/<저장소명>:base





