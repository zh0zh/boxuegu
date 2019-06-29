from django.conf.urls import url
from .views import OrgHomeView, OrgListView, TeacherListView, AddFavView

urlpatterns = [
    url(r'^org/home/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^org/list/$', OrgListView.as_view(), name='org_list'),
    url(r'^org/teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^org/add_fav/$', AddFavView.as_view(), name='add_fav'),

]
