from django.urls import path
from . import views

urlpatterns = [
    path('tours/', views.tour_list, name='tour_list'),
    path('booking/<int:tour_id>/', views.create_booking, name='create_booking'),
    path('comment/<int:tour_id>/', views.add_comment, name='add_comment'),
]