from django.urls import path
from .views import signup
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView


# app_name='accounts'

urlpatterns=[
	path('signup/', signup, name='signup' ),
	path('logout/', LogoutView.as_view(), name='logout' ),
	path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login' ),
	
	path('reset/', PasswordResetView.as_view(
		template_name='accounts/reset.html',
		email_template_name='accounts/reset_email.html',
		subject_template_name='accounts/reset_subject.txt'), name='password_reset' ),
	
	path('reset/done/', PasswordResetDoneView.as_view(template_name='accounts/reset_done.html'), name='password_reset_done' ),
	
	path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/reset_confirm.html'), name='password_reset_confirm' ),
	
	path('reset/complete/', PasswordResetCompleteView.as_view(template_name='accounts/reset_complete.html'), name='password_reset_complete' ),


	path('setting/password/', PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change' ),
	path('setting/password/done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done' ),
]