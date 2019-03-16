from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as Validoation_Core_Error

from django.contrib.auth import get_user_model,authenticate
from django.core.validators import EmailValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from movies.serializers import MovieMainSerializer

User = get_user_model()

from ..tasks import send_email


class UserSerializer(serializers.ModelSerializer):
    movie = MovieMainSerializer( many=True)
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


        errors = dict()

        try:
            # 이걸로 규칙 유효한지 검사해보는듯. 1234등 부적절한거 거르는듯.
            validate_password(password=value)

        except serializers.ValidationError as e:
            errors['password'] = list(e.messages)
            print(errors)

        if errors:
            raise serializers.ValidationError(errors)
        return value

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('이메일이 이미 존재합니다')

        errors = dict()
        validator = EmailValidator()
        try:
            validator(value)
        except Validoation_Core_Error as e :
            errors['email'] = list(e.message)
            print(errors)

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def validate_phone_number(self,phone_number):
        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError('휴대전화번호가 이미 존재합니다')

        for index,number in enumerate(phone_number):
            # 해당 자리수에서 데이터 타입이 숫자가 아니면
            if number.isdigit() == False :
                raise serializers.ValidationError('- 없이 숫자만 입력해 주세요')

        # 자리수가 10~11자 아니면
        if len(phone_number)!=10 and len(phone_number)!=11:
            raise serializers.ValidationError('010aaaabbbb 형식에 맞게 번호를 입력해주세요')

        return phone_number

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
        email=validated_data['email'],
        phone_number=validated_data['phone_number'],
        )

        user.is_active = False
        user.save()

        # 그냥 유저 전달하면 에러떠서 민규님 따라해봄
        send_email.delay(user.pk)


        return user



class AccessTokenSerializer(serializers.Serializer):

    access_token = serializers.CharField()

    def validate(self, attrs):

        access_token = attrs.get('access_token')
        print(f'22222, {access_token}')

        if access_token:
            user = authenticate(access_token=access_token)
            if not user:
                raise serializers.ValidationError('액세스 토큰이 잘못됬습니다.')

        else:
            raise serializers.ValidationError('액세스 토큰이 필요해요')

        attrs['user'] = user
        return attrs
