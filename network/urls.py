from django.urls import path
from django.contrib.auth.views import login
from accounts.forms import LoginForm

urlpatterns = [

   path('login/',login,{'template_name':'accounts/login.html','authentication_form':LoginForm}),
   
]