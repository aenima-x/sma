from django.urls import path, include
from . import views

urlpatterns = [
    path('signup', views.signup_view, name="signup"),
    path('stocks/<str:symbol>', views.get_stocks_view, name="get_stocks"),
]
