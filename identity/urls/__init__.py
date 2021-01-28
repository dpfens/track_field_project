from django.urls import path
from django.contrib.auth import views as auth_views
from identity import views


app_name = 'identity'
urlpatterns = [
    path('preferences/', views.PreferenceView.as_view(), name='preferences'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('privacy', views.PrivacyView.as_view(), name='privacy'),

    path('login/', auth_views.LoginView.as_view(), 'login'),
    # password reset paths
    path('password/reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done',),
    path('password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete',)
]
