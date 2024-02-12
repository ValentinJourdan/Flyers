from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_profile, name='profile'),
    path('modify/', views.modify_profile, name='modify_profile'),
    path('demande-validation/', views.request_vendor_status,
         name='demande_validation'),
    path('create-stripe-connect-account/', views.create_stripe_connect_account,
         name='create_stripe_connect_account'),
]
