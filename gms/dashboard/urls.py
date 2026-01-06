from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('org/', views.sample_page, name='org'),
    path('branch/', views.sample_page, name='branch'),
    path('staff/', views.sample_page, name='staff'),
    path('blank-page/',views.blank_page,name='blank'),
    path('add-member/',views.add_member,name='add_member'),
    path('members/', views.member_list, name='member_list'),
    # dashboard/urls.py
    path('members/<int:member_id>/payments/',views.member_payment_list,name='member_payments'),
    path('members/<int:pk>/edit/', views.edit_member, name='edit_member'),

    path('members/<int:member_id>/add-payment/',views.add_payment,name='add_payment'),
    path('members/<int:member_id>/subscriptions/',views.member_subscriptions,name='member_subscriptions'),
    path('payments/today/',views.today_payments,name='today_payments'),
    path('payments/',views.all_payments,name='all_payments'),
    path('staff/today-payments/', views.staff_today_payments, name='staff_today_payments'),
    path('staff/expired-members/', views.staff_expired_members, name='staff_expired_members'),

]
