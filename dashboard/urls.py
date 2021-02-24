from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/<str:order_id>/delete/', views.delete_order, name='delete_order'),
]