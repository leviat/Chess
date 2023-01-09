from django.urls import path
from chat import views

urlpatterns = [
    path('cookie/', views.Cookie.as_view()),
    path('test/', views.Test.as_view()),
]