from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', views.register, name = "register"),
    path('login/', views.login, name = "login"),
    path('logout/', views.logout, name = "logout"),
    path('profileView/', views.profileView, name = "profileView"),
    path('profileEdit/', views.profileEdit, name = "profileEdit"),
    path('changePasswd/', views.changePasswd, name = "changePasswd"),
    path('emailCheck/', views.emailCheck, name = "emailCheck"),
    path('phoneCheck/', views.phoneCheck, name = "phoneCheck"),
    path('emailEditCheck/', views.emailEditCheck, name = "emailEditCheck"),
    path('phoneEditCheck/', views.phoneEditCheck, name = "phoneEditCheck"),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
