from django import forms
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

User=get_user_model()

class SignupForm(forms.Form):
    username = forms.CharField(
        label='아이디',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    email = forms.EmailField(
        label='이메일',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    phone_number = forms.CharField(
        label='핸드폰번호',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    # form.is_valid()를 통과하지 못한 경우,
    #  유효성 검증을 통과하지 못한 내용은 form.<field>.errors에 정의됨 -> form을 순회하면 form.<field>를 하나씩 순회
    #  (통과하지 못한 경우의 'form'변수를 디버깅을 이용해 확인해본다)

    # 1. form.is_valid()를 통과하지 못했을 경우, 해당 내용을 template에 출력하도록 구현
    # 2. SignupForm의 clean()메서드를 재정의하고, password와 password2를 비교해서 유효성을 검증하도록 구현



    def clean_username(self):
        # 적절히작성
        # 원하는결과는, 중복되지 않는 username을 사용하면 유저 생성
        # 중복된 username을 입력하면 오류목록이 출력(자동)

        #username field의 clean() 실행결곽가 self.cleaned_data['username']에 있음
        data = self.cleaned_data['username']

        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('같은 아이디가 존재합니다.')

        return data

    def clean_email(self):

        data = self.cleaned_data['email']

        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('같은 이메일 존재합니다.')

        return data


    #01066511550
    #010665115500
    #010-6651-1550
    def clean_phone_number(self):

        data = self.cleaned_data['phone_number']

        data_type_mask = ['0','0','0','-','0','0','0','0','-','0','0','0','0']

        for index,number in enumerate(data):
            # 해당 자리수에서 데이터 타입 다르면
            if data_type_mask[index].isdigit() != number.isdigit():
                raise forms.ValidationError('010-xxxx-xxxx 형식에 맞게 번호를 입력해주세요')

            # -의 경우 타입 같더라도 - 외의 기호 들어가면
            if number == False and number !='-':
                raise forms.ValidationError('010-xxxx-xxxx 형식에 맞게 번호를 입력해주세요')

        return data

#form의 에러와 field에러가 다르다.from
#form의 에러는 자동으로 form위에 나오고 field에러는 템플릿에서 출력해줬다.

#field에러 처럼 처리해주자.from

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')


        # if password != password2:
        #     raise ValidationError('비밀번호와 비밀번호확인값일치 안함.')
        #
        # return self.cleaned_data


        if password != password2:

            msg = "비밀번호 두개가 불일치 합니다."

            self.add_error('password',msg)
            # self.add_error('password2',msg)


    def signup(self):

        fields =[
            'username',
            'email',
            'password',
            'phone_number',
        ]


        # user=User.objects.create_user(**self.cleaned_data) ##이렇게 바로 받으면 password2있어서 안된다.
        # user = User.objects.create_user(**{field: self.cleaned_data.get(field) for field in fields}) #내가한것.

        # create_user_dict={}
        # for key, value in self.cleaned_data.items():
        #     if key in fields:
        #         create_user_dict[key]=value

        #user = User.objects.create_user(**create_user_dict)





        #       위에 것을 리스트 컴프리핸션으로 바꾸자.

        # create_user_dict = { key:value for key, value in self.cleaned_data.items() if key in fields }
        # user = User.objects.create_user(**create_user_dict)





        #       filter쓰는 방법으로 해보자.

        #items 에는 key,value로된 tuple있어서 이것 처리하는 함수 만들어 줘야함.

        def in_fields(item):
            return item[0] in fields

        result = filter(in_fields, self.cleaned_data.items()) # 이 값을 순회하면 튜풀이 나온다.

        #이 ((key1,value1), (key2,value2) . . . . ..) 이렇게 거처서 나옴,

        # 다시 dict에 담아줌.
        create_user_dict={}
        for item in result:
            create_user_dict[item[0]]=item[1]

        user = User.objects.create_user(**create_user_dict)

        #더쉽게는 이렇게 호출하면 끝남.
        # create_user_dict = dict(filter(in_fields, self.cleaned_data.items()))
        #람다함수 쓰면
        # create_user_dict = dict(filter(lambda item:item[0] in fiedls , self.cleaned_data.items()))



        return user



