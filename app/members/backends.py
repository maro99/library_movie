
# admin /특정비밀번호
# 위 값으로 로그인 시도시 authenticate가 성송하도록 커스텀 Backend를 작성
# members.backends모듈에 작성
# Backend 명은 Settings.Backend
# password는 장고안의 문자열을 생성해서? 써야함.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()


class SettingsBackend:
    '''
        ADMIN = 'admin'
        ADMIN_PASSWORD ='pbkdf2_sha256$100000$zNIjdY5qwrae$dASPtmQ/vw7VQ9cFD69aYu7hTxTLQLoFFzLqUzxtq1I='
        '''

    def authenticate(self, request, username=None,password=None):
        login_valid = (settings.ADMIN_USERNAME == username)                                     # 입력한 username과 settings의 username같은지 판별.
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)             # pwd유효한지 판단.

        if login_valid and pwd_valid:                     # username, password 일치시에
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:                                                                                        # User가 없을 경우에 만들어준다.
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = User(username=username)                                                         # createsuperuser는 password반드시 넣어줘야 되서 안쓰는듯.
                user.is_staff = True                   # 이 계정은 password궂이 필요없는 계정.( 어짜피 위에서 입력시마다 authenticate로 검사하니까. <db 에서 가져오는것이 아님.> )
                user.is_superuser = True
                user.save()
            return user                                  # user 를 get했다면 여기서 반환. 없응면 except안에서 만들어서 반환.
        return None                                # pwd,username유효하지 않은경우는 아무것도 돌려주지 않는다.


    def get_user(self, user_id):                                  #이건 문서그대로 넣는다. (custom하기 전과 같은듯.)
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None