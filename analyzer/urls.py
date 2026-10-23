from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_form, name='student_form'),
    path('takip/', views.track_status, name='track_status'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update-status/<int:pk>/', views.update_status, name='update_status'),
    path('export/', views.export_to_excel, name='export_to_excel'),
    path('api/analyze/', views.api_analyze, name='api_analyze'),
]