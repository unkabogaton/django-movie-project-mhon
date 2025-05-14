
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('transactions/', views.transactions_list, name='transactions'),
    path('transactions/<uuid:transaction_id>/', views.transaction_detail_modal, name='transaction_detail_modal'),
    path('transactions/update/', views.update_transaction_status, name='update_transaction_status'),
    
    path('ticket-purchases/', views.ticket_purchases, name='ticket_purchases'),
    path('ticket-purchases/redeem/<uuid:ticket_id>/', views.redeem_ticket, name='redeem_ticket'),
    
    path('customers/', views.customers_list, name='customers'),
    
    path('showrooms/', views.showrooms, name='showrooms'),
    path('showrooms/update/<uuid:schedule_id>/', views.update_schedule, name='update_schedule'),
    
    path('movies/', views.movie_list, name='movies'),
    path('movies/<uuid:id>/details/', views.movie_detail, name='movie_detail'),
    path('movies/add/', views.add_movie, name='add_movie'),
    path('movies/edit/', views.edit_movie, name='edit_movie'),
    path('movies/<uuid:id>/delete/', views.delete_movie, name='delete_movie'),
    
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
