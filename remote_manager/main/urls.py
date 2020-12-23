from django.urls import path
from . import views

urlpatterns = [
    path('login', views.MainLoginView.as_view(), name='login'),
    path('logout', views.MainLogoutView.as_view(), name='logout'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('user/list', views.UserListView.as_view(), name='user_list'),
    path('user/create', views.UserCreateView.as_view(), name='user_create'),
    path('user/update/<str:pk>', views.UserUpdateView.as_view(), name='user_update'),
    path('user/detail/<str:pk>', views.UserDetailView.as_view(), name='user_detail'),
    path('org/list', views.OrgListView.as_view(), name='org_list'),
    path('org/create', views.OrgCreateView.as_view(), name='org_create'),
    path('org/update/<str:pk>', views.OrgUpdateView.as_view(), name='org_update'),
    path('org/detail/<str:pk>', views.OrgDetailView.as_view(), name='org_detail')
]