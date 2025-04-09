from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('resume/', views.resume_form, name='resume_form'),
    path('success/', views.success, name='success'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('export/pdf/<int:pk>/', views.export_pdf, name='export_pdf'),
    path('resume/public/<uuid:public_id>/', views.resume_public, name='resume_public'),

]
