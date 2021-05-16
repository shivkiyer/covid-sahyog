from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.launch_app, name='home_page'),
    path('request-help', views.request_help, name='request_help'),
    path('offer-help', views.offer_help, name='offer_help'),
    path('about-us', views.about_us, name='about_us'),
    #path('populate-db', views.populate_db, name='populate_db'),
    path('submit-help-request', views.submit_help_request, name='submit_help_request'),
    path('confirm-submission', views.confirm_help, name='confirm_submission'),
    path('state/<slug:slug>', views.state_list, name='state_list'),
    path('edit-help/<int:help_id>', views.edit_help, name='edit_help'),
    path('validate-help/<int:help_id>', views.validate_help, name='validate_help'),
    path('logout', views.logout_user, name='logout_user'),
    path('search', views.search_query, name='search_query')
]
