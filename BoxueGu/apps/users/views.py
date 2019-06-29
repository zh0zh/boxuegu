from django import http
from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from users import expiry
from users.forms import RegisterForm, LoginForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from users.models import Banner, UserProfile
from utils import bx_signature
from celery_tasks.mail.tasks import send_user_email
from pure_pagination.paginator import Paginator


class IndexView(View):
    """首页"""

    def get(self, request):
        """获取首页页面"""
        all_banners = Banner.objects.all()
        courses = Course.objects.all()
        banner_courses = Course.objects.all()
        course_orgs = CourseOrg.objects.all()

        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
            'MEDIA_URL': settings.MEDIA_URL,
        })


class RegisterView(View):
    """注册"""

    def get(self, request):
        """获取注册页面"""
        # 生成表单对象
        register_form = RegisterForm()
        # 调用模版渲染生成表单
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        """验证表单数据"""
        # 1、获取前端传递的表单数据
        data = request.POST
        # 2、验证表单数据
        register_form = RegisterForm(data)
        res = register_form.is_valid()  # 验证成功返回True，验证失败返回False

        if res:
            # 验证成功，则执行相应业务逻辑操作，这里就直接返回验证成功后的字段数据
            data = register_form.cleaned_data
            user = UserProfile.objects.create_user(username=data['email'], password=data['password'],
                                                   email=data['email'])

            # 保持登陆
            login(request, user)

            # 响应对象添加cookies， 生成cookies保存用户名，用于网页前端状态条读取
            next_url = '/'
            response = redirect(next_url)
            response.set_cookie('username', user.username, max_age=expiry.LOGIN_EXPIRY)

            return response

        else:
            # 验证失败，则在注册模板中通过register_form.errors获取错误
            return render(request, 'register.html', {'register_form': register_form})


class LoginView(View):
    """登录"""

    def get(self, request):
        """获取登录页面"""
        return render(request, 'login.html')

    def post(self, request):
        """登录表单验证"""
        # 1、获取前端传递的表单数据
        data = request.POST
        # 2、验证表单数据
        login_form = LoginForm(data)
        res = login_form.is_valid()  # 验证成功返回True，验证失败返回False
        print(login_form.cleaned_data)

        if res:
            # 验证成功，则执行相应业务逻辑操作，这里就直接返回验证成功后的字段数据
            user_data = login_form.cleaned_data
            user = authenticate(request, username=user_data['username'], password=user_data['password'])

            if user:
                # 保持登陆
                login(request, user)

                # 响应对象添加cookies， 生成cookies保存用户名，用于网页前端状态条读取
                next_url = '/'
                response = redirect(next_url)
                response.set_cookie('username', user.username, max_age=expiry.LOGIN_EXPIRY)

                return response

            else:
                return render(request, 'register.html', {'register_form': login_form})

        else:
            # 验证失败，则在注册模板中通过login_form.errors获取错误
            return render(request, 'register.html', {'register_form': login_form})


class LogoutView(View):
    """退出登录"""

    def get(self, request):
        """实现退出登录逻辑"""
        # 清理session
        logout(request)
        # 退出登录，重定向到首页
        response = redirect('/')
        # 退出登录时清除cookie中的username
        response.delete_cookie('username')

        return response


class ForgetPwdView(View):
    def get(self, request):
        # 生成表单对象
        forget_form = ForgetForm()
        # 调用模版渲染生成表单
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        # 1、获取前端传递的表单数据
        data = request.POST
        # 2、验证表单数据
        forget_form = ForgetForm(data)
        res = forget_form.is_valid()  # 验证成功返回True，验证失败返回False

        if res:
            # 验证成功，则执行相应业务逻辑操作，这里就直接返回验证成功后的字段数据
            forget_data = forget_form.cleaned_data
            email = forget_data['email']
            user = UserProfile.objects.get(email=email)
            # csrftoken = forget_data['csrfmiddlewaretoken']

            # 调用celery发送邮件任务
            token = bx_signature.dumps({'user_id': user.id}, expiry.EMAIL_ACTIVATE_EXPIRES)
            url = settings.EMAIL_ACTIVE_URL + '?token=%s' % token
            send_user_email.delay(email, url)

            return render(request, 'send_success.html')

        else:
            # 验证失败，则在注册模板中通过register_form.errors获取错误
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request):
        # 接收
        token = request.GET.get('token')

        # 验证
        if not all([token]):
            return http.HttpResponseBadRequest('参数不完整')

        json = bx_signature.loads(token, expiry.EMAIL_ACTIVATE_EXPIRES)
        if json is None:
            return http.HttpResponseBadRequest('激活链接无效')

        # 处理
        user_id = json.get('user_id')
        try:
            user = UserProfile.objects.get(pk=user_id)
            email = user.email
        except:
            return http.HttpResponseBadRequest('无此用户')
        else:
            # 响应
            return render(request, 'password_reset.html', {'email': email})

    def post(self, request):
        # 1、获取前端传递的表单数据
        data = request.POST
        # 2、验证表单数据
        modify_form = ModifyPwdForm(data)
        res = modify_form.is_valid()  # 验证成功返回True，验证失败返回False

        if res:
            modify_data = modify_form.cleaned_data
            password1 = modify_data.get('password1')
            password2 = modify_data.get('password2')
            email = data.get('email')
            if password1 == password2:
                try:
                    user = UserProfile.objects.get(email=email)
                except:
                    return http.HttpResponseBadRequest('无此用户')
                else:
                    user.set_password(password2)
                    user.save()
                    return redirect('/login/')
            else:
                return http.HttpResponseBadRequest('两次输入的密码不同')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': modify_form})


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {
            'MEDIA_URL': settings.MEDIA_URL,
        })

    def post(self, request):
        # 1、获取前端传递的表单数据
        data = request.POST
        user = request.user
        # 2、验证表单数据
        userinfo_form = UserInfoForm(data)
        res = userinfo_form.is_valid()  # 验证成功返回True，验证失败返回False

        if res:
            # 验证成功，则执行相应业务逻辑操作，这里就直接返回验证成功后的字段数据
            userinfo_data = userinfo_form.cleaned_data
            try:
                UserProfile.objects.filter(pk=user.id).update(**userinfo_data)
            except Exception as e:
                return http.JsonResponse({"status": "error"})
            else:
                return http.JsonResponse({"status": "success"})


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        # 1、获取前端传递的表单数据
        data = request.POST
        img_dict = request.FILES
        img_file = img_dict.get('image').read()
        # 2、验证表单数据
        img_form = UploadImageForm(data)
        res = img_form.is_valid()  # 验证成功返回True，验证失败返回False

        if res:
            try:
                print(settings.BASE_DIR + '/static/media/image/' + '%s' % user.username + '.jpg')
                with open(settings.BASE_DIR + '/static/media/image/' + '%s' % user.username + '.jpg', 'wb') as file1:
                    file1.write(img_file)
                user.image = 'image/' + str(user.username) + '.jpg'
                user.save()

                return http.JsonResponse({
                    "status": "success"
                })
            except Exception as e:
                return http.HttpResponseBadRequest('保存头像失败')
        else:
            return http.JsonResponse({
                "status": "error"
            })


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_courses = UserCourse.objects.filter(user_id=user.id)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
            'MEDIA_URL': settings.MEDIA_URL,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        fav_orgs = UserFavorite.objects.filter(user_id=user.id, fav_type=2)

        org_list = []
        for org in fav_orgs:
            org_list.append(CourseOrg.objects.get(pk=org.fav_id))

        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
            'MEDIA_URL': settings.MEDIA_URL,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        fav_teacher = UserFavorite.objects.filter(user_id=user.id, fav_type=3)

        teacher_list = []
        for teacher in fav_teacher:
            teacher_list.append(Teacher.objects.get(pk=teacher.fav_id))

        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
            'MEDIA_URL': settings.MEDIA_URL,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        fav_course = UserFavorite.objects.filter(user_id=user.id, fav_type=1)

        course_list = []
        for course in fav_course:
            course_list.append(Course.objects.get(pk=course.fav_id))

        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
            'MEDIA_URL': settings.MEDIA_URL,
        })


class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        all_messages = UserMessage.objects.filter(user=user.id)
        paginator = Paginator(all_messages, 2)
        page_num = request.GET.get('page', 1)
        messages = paginator.page(page_num)

        # pages = messages.pages
        # number = messages.number
        # messages = {
        #     'number': page_num,
        #     'pages': pages,
        #     'object_list': page_messages.object_list
        # }

        return render(request, 'usercenter-message.html', {
            'messages': messages,
            'MEDIA_URL': settings.MEDIA_URL,
        })
