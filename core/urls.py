from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
 path('', views.home, name='home'),
 path('trips/', views.trips, name='trips'),
 path('feed/', views.feed, name='feed'),
 path('chat/', views.chat, name='chat'),
 path('profile/', views.profile, name='profile'),
 path('book/<int:trip_id>/', views.book_trip, name='book_trip'),
 path('new-trip/', views.new_trip, name='new_trip'),
 path('request-trip/', views.request_trip, name='request_trip'),
 path('fulfill-trip-request/<int:request_id>/', views.fulfill_trip_request, name='fulfill_trip_request'),
 path('join-clan/<int:clan_id>/', views.join_clan, name='join_clan'),
 path('login/', views.login_view, name='login'),
 path('logout/', views.logout_view, name='logout'),
 path('register/', views.register_view, name='register'),
 path('cancel-trip/<int:trip_id>/', views.cancel_trip, name='cancel_trip'),
 path('rate-trip/<int:booking_id>/', views.rate_trip, name='rate_trip'),
 path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
 path('mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
]