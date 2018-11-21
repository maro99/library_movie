from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()
from .tokens import account_activation_token

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
       # 이런식으로 기존의 validator가져다가 쓸 수 도 있다.
       # 여기서 이렇게 지정시 알아서 어떤 애러이고 왜 일어났는지 error에 같이 보내준다.
       validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = "__all__"

    def to_internal_value(self, data):
        """
        POST/PUT과 같이 데이터 변경이 있을 때
        데이터를 저장하기 전에 핸들링 할수 있는 함수.

        """
        ret = super(UserSerializer, self).to_internal_value(data)

        return ret

    def to_representation(self, obj):
        """
        GET/POST/PUT과 같이 데이터 변경이 있고난 후
        serializer.data로 접근할 때 값을 변하여 보여줍니다.
        """
        ret = super(UserSerializer,self).to_representation(obj)
        return ret

    # 한 filed에 대해서 유효성 검사시
    #  validate_field명
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('패스워드 최소 8자 이상이어야 합니다.')
        return value

    # def validate_email(self,value):
    #     if User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError('이메일이 이미 존재합니다')
    #     return value

    # 여러 필드에 걸처서 유효성 검사시
    # validate(attrs)
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('패스워드가 일치하지 않습니다.')
        return attrs



    def create(self,validated_data):
        """
        데 이터를 저장할 때 필요한 과정을 구현한다.
        """
        user = User.objects.create_user(
        username=validated_data['username'],
        password=validated_data['password'],
        email=validated_data['email']
        )

        user.is_active =False
        user.save()

        # current_site = get_current_site(self.context['request']
        message = render_to_string('members/account_activate_email.html',{
                'user':user, # 생성한 사용자 객체
                'domain':'localhost:8000', # 이거 추후에 배포시에는 바꿔줬던것 같다? #########
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'), # 생성한 사용자 객체의 pk를 암호화한 값
                'token':account_activation_token.make_token(user) # 생성한 사용자 객체를 통해 생성한 token값.
        })

        # 이메일 전송 과정
        mail_subject = 'test'
        to_email = 'nadcdc@naver.com'
        # EmailMessaage(제목, 본문, 받는이)
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()


        return user








