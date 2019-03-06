from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("create_account", views.createAccount, name="create_account"),
    path('ideas', views.ideas, name='ideas'),
    path('trade', views.trade, name='trade'),
    path('build_trade/<str:ticker>', views.build_trade, name='build_trade'),


]