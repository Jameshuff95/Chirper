from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    # <int:pk> represents the primary key (id) of the user.
    # This line makes the desired profile appear when called
    path('profile/<int:pk>', views.profile, name='profile'),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
]
