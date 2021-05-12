from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.launch_app, name='home_page'),
    path('request-help', views.request_help, name='request_help'),
    path('offer-help', views.offer_help, name='offer_help'),
    path('about-us', views.about_us, name='about_us'),
    path('populate-db', views.populate_db, name='populate_db'),
]
