from django.urls import path
from . import views

urlpatterns = [
    path('list', views.VNCListView.as_view(), name='vnc_list'),
    path('create', views.VNCCreateView.as_view(), name='vnc_create'),
    path('detail/<str:pk>', views.VNCDetailView.as_view(), name='vnc_detail'),
    path('update/<str:pk>', views.VNCUpdateView.as_view(), name='vnc_update'),
    path('vnc_console/<str:pk>', views.VNCConsoleView.as_view(), name='vnc_console'),
]