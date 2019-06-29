from django.contrib.auth.backends import ModelBackend
from users.models import UserProfile
import re


class Boxuegubackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 前台登录

        # username变量的值，可能是邮箱，也可能是手机号，需要判断后再查询
        try:
            if re.match(r'^1[3-9]\d{9}$', username):
                # 手机号
                user = UserProfile.objects.get(mobile=username)
            elif re.match(r'^\w+@[a-z0-9]+\.[a-z]{2,4}$', username):
                # 邮箱
                user = UserProfile.objects.get(email=username)
            else:
                # 用户名
                user = UserProfile.objects.get(username=username)
        except Exception as e:
            return None  # 如果报错，则返回空

        # 判断密码
        if not user.check_password(password):
            return None  # 用户名或手机号错误
        else:
            return user  # 返回user对象，传入视图类