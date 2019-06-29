from django.conf.urls import url
from users.views import IndexView, UserInfoView, LogoutView, RegisterView, LoginView, ForgetPwdView, ResetView, \
    MyMessageView, MyCourseView, MyFavOrgView, UploadImageView, MyFavTeacherView, MyFavCourseView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/$', ResetView.as_view(), name='reset_pwd'),
    # url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^users/info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
]
