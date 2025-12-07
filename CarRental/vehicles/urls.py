from django.urls import path
from . import views 
from django.conf import settings

app_name = 'vehicles'

urlpatterns = [
    path('', views.car_list, name='car_list'),

    path('<int:pk>/', views.car_detail, name='car_detail'),
    path('<int:car_pk>/add-review/', views.add_car_review, name='add_car_review'),

    # --- روابط لوحة الإدارة (للأدمن) ---
    path('manage/', views.manage_cars, name='manage_cars'),
    path('add/', views.add_car, name='add_car'),
    path('edit/<int:pk>/', views.edit_car, name='edit_car'),
    path('delete/<int:pk>/', views.delete_car, name='delete_car'),

    path('companies/manage/', views.manage_companies, name='manage_companies'),
    path('companies/add/', views.add_company, name='add_company'),

    path('companies/edit/<int:pk>/', views.edit_company, name='edit_company'),
    path('companies/delete/<int:pk>/', views.delete_company, name='delete_company'),
]