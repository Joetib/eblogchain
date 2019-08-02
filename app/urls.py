from django.urls import path
from . import views


app_name = 'app'

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.loginview, name="login"),
    path('welcome/', views.welcome, name="welcome"),
    path('contact/', views.contact_us, name="contact"),
    path('profile/', views.profile, name="profile"),
    path('about/', views.about_us, name="about"), 
    path('history/', views.history, name="history"),
    path('ref_num/', views.momo_ref_confirm, name="momo_ref_confirm"),
    path('logout/', views.logout_view, name="logout"),
]