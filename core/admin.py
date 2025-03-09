from django.contrib import admin
from .models import Profile, Vehicle, Trip, Booking, Post, Message, Clan, VerificationRequest, Notification, TripRating, TripRequest

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
 list_display = ('user', 'phone', 'is_driver', 'verified', 'hype_score')
 list_filter = ('is_driver', 'verified')
 search_fields = ('user__username', 'phone')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
 list_display = ('driver', 'type', 'reg_number')
 search_fields = ('reg_number',)

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
 list_display = ('driver', 'start', 'end', 'seats', 'cargo_capacity', 'departure', 'status')
 list_filter = ('status',)
 search_fields = ('start', 'end')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
 list_display = ('passenger', 'trip', 'seats', 'cargo_weight', 'total_cost', 'status')
 list_filter = ('status',)
 search_fields = ('passenger__username',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
 list_display = ('user', 'content', 'created_at')
 search_fields = ('content',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
 list_display = ('sender', 'receiver', 'content', 'timestamp')
 search_fields = ('sender__username', 'receiver__username', 'content')

@admin.register(Clan)
class ClanAdmin(admin.ModelAdmin):
    list_display = ('name', 'member_count')
    search_fields = ('name',)

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'

@admin.register(VerificationRequest)
class VerificationRequestAdmin(admin.ModelAdmin):
 list_display = ('user', 'status', 'submitted_at')
 list_filter = ('status',)
 search_fields = ('user__username',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
 list_display = ('user', 'message', 'read', 'created_at')
 list_filter = ('read',)
 search_fields = ('user__username', 'message')

@admin.register(TripRating)
class TripRatingAdmin(admin.ModelAdmin):
 list_display = ('booking', 'rating', 'comments')
 search_fields = ('booking__passenger__username', 'comments')

@admin.register(TripRequest)
class TripRequestAdmin(admin.ModelAdmin):
 list_display = ('passenger', 'start', 'end', 'preferred_date', 'status')
 list_filter = ('status',)
 search_fields = ('start', 'end', 'passenger__username')