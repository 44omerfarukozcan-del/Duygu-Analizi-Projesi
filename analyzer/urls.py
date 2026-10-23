from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_form, name='student_form'),           # Ana sayfa: Halka açık form
    path('dashboard/', views.dashboard, name='dashboard'),       # Yönetim Paneli: Şifreli alan
]
urlpatterns = [
    path('', views.student_form, name='student_form'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export/', views.export_to_excel, name='export_to_excel'), # Yeni Eklenen Satır
]