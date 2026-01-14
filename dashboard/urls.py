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
    # path('payments/today/',views.today_payments,name='today_payments'),
    # path('payments/',views.all_payments,name='all_payments'),
    # path('payment2/',views.all_payment2,name='all_payment2'),
    path('staff/today-payments/', views.staff_today_payments, name='staff_today_payments'),
    path('staff/expired-members/', views.staff_expired_members, name='staff_expired_members'),

    # General View
    path('profile',views.profile_page,name='profile'),

    path('faq',views.faq,name='faq'),
    # path('payments/today/',views.today_payment,name='today_payments'),
    path('payments/', views.payments_view, name='payments_all'),
    path('payments/today/', views.payments_view, {'period': 'today'}, name='payments_today'),
    path('payments/last-7-days/', views.payments_view, {'period': 'last_7_days'}, name='payments_last_7_days'),
    path('payments/this-month/', views.payments_view, {'period': 'this_month'}, name='payments_this_month'),

    # Subscription 
    path('subscriptions/', views.subscription_expiry_view, name='subscriptions_all'),
    path('subscriptions/expire-today/', views.subscription_expiry_view, {'period': 'today'}, name='subscriptions_expire_today'),
    path('subscriptions/expire-tomorrow/', views.subscription_expiry_view, {'period': 'tomorrow'}, name='subscriptions_expire_tomorrow'),
    path('subscriptions/expired-last-7-days/', views.subscription_expiry_view, {'period': 'last_7_days'}, name='subscriptions_expired_last_7_days'),


]
