from django.urls import path
from .import views

urlpatterns = [
      path('',views.home,name="home"),
      path('register/',views.register,name="register"),
      path('login/',views.login,name="login"),
      # path('appointment/',views.book_appointment,name="appointment"),


      
]
