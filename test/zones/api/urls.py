from django.urls import path

from zones.api import views

urlpatterns = [
    path('edit/', views.edit),
    path('remove_dist/',views.remove_distribution) # Nueva ruta para eliminar distribution
    ]
