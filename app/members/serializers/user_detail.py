from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.core.exceptions import ValidationError as Validoation_Core_Error

User = get_user_model()


class UserInfoChangePageSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields =(
            'username',
            'password',
            'email',
            'phone_number',
        )


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    password2 = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'password',
            'password2',
        )

    # 1. 두개의 비밀번호 일치하는지 검사
    # 2. 일치하면 비밀번호 유효성 검사.
    def validate_password(self, password):

        password2 = self.initial_data.get('password2')
        if not password == password2:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')

        errors = dict()


        try:
            # 이걸로 규칙 유효한지 검사해보는듯. 1234등 부적절한거 거르는듯.
            validate_password(password=password)

        except ValidationError as e:
            errors['password'] = list(e.messages)
            print(errors)

        if errors:
            raise serializers.ValidationError(errors)

        return password


class ChangeEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField

    class Meta:
        model = User
        fields = (
            'email',
        )

    # 1.일치하는 메일 이 있는지 검사.
    def validate_email(self,email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('이메일이 이미 존재합니다')


        errors = dict()
        validator = EmailValidator()
        try:
            validator(email)
        except Validoation_Core_Error as e :
            errors['email'] = list(e.message)
            print(errors)

        if errors:
            raise serializers.ValidationError(errors)

        return email
