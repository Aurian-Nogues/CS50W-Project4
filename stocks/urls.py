from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("create_account", views.createAccount, name="create_account"),
    path('track_record', views.track_record, name='track_record'),
    path('trade', views.trade, name='trade'),
    path('build_trade/<str:ticker>/<str:name>', views.build_trade, name='build_trade'),
    path('close_trade/<str:ticker>/<str:open_price>/<str:open_date>', views.close_trade, name='close_trade'),
    path('record_trade', views.record_trade, name='record_trade'),
    path('team_dashboard', views.team_dashboard, name='team_dashboard'),
    path('team_track_record', views.team_track_record, name='team_track_record'),
    
]