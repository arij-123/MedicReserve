from django.urls import path 
from . import views 



urlpatterns = [
    path('index/', views.index , name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('departments/', views.departments_view, name='departments'),
    path('details/<str:specialty>/', views.details_view, name='details'),
    path('reserver/<int:med_id>/', views.reserver_rdv, name='reserver_rdv'),


    path('medecin/<int:medecin_id>/reserver/', views.verifier_user, name='verifier_user'),

    path('reservation-success/', views.reservation_success, name='reservation_success'),

]




        
