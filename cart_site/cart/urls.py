from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('publish/', views.publish, name='publish'),
    path('publish_prod/', views.publish_prod, name='publish_prod'),
    path('view/<str:pk>/', views.view, name='view'),
]

