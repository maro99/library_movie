from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()

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

    # 한 filed에 대해서 유효성 검사시
    #  validate_field명
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('패스워드 최소 8자 이상이어야 합니다.')
        return value

    # 여러 필드에 걸처서 유효성 검사시
    # validate(attrs)
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('패스워드가 일치하지 않습니다.')
        return attrs


    def create(self,validated_data):
        user = User.objects.create_user(
        username=validated_data['username'],
        password=validated_data['password'],
        email=validated_data['email']
        )
        return user


    class Meta:
        model = User
        fields = "__all__"






