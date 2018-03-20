from django.urls import path
from . import views

urlpatterns = [
    path('',views.jddatashow,name='jddatashow'),
    path('<int:question_id>/', views.jd_detail, name="jd_detail"),
]
