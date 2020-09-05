"""hypercar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from tickets.views import WelcomeView
from tickets.views import MenuView
from tickets.views import TicketView
from tickets.views import ProcessingView
from tickets.views import NextView
from django.urls import re_path
from django.views.generic import RedirectView

urlpatterns = [
    path('', MenuView.as_view()),
    path('welcome/', WelcomeView.as_view()),
    path('menu/', MenuView.as_view(), name="index"),
    path('processing', ProcessingView.as_view(), name="processing"),
    path('processing/', RedirectView.as_view(url='/next')),
    path('next', NextView.as_view(), name="next"),
    re_path('get_ticket/(?P<service>[\w_]+)', TicketView.as_view()),
]
