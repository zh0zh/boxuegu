from django.conf.urls import url
from .views import CourseDetailView,CourseListView

urlpatterns = [
    url(r'^course/detail/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^course/list/$', CourseListView.as_view(), name='course_list'),

]
