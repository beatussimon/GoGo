from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from decimal import Decimal

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    is_driver = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    hype_score = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username

class Trip(models.Model):
    driver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='trips')
    start = models.CharField(max_length=100)
    end = models.CharField(max_length=100)
    seats = models.PositiveIntegerField()
    cargo_capacity = models.FloatField(default=0.0)
    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    departure = models.DateTimeField()
    auction_mode = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='open')

    def __str__(self):
        return f"{self.start} to {self.end}"

class Booking(models.Model):
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
    seats = models.PositiveIntegerField()
    cargo_weight = models.FloatField(default=0.0)
    bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending')

    def __str__(self):
        return f"Booking by {self.passenger.username} for {self.trip}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

class Clan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, related_name='clans')

    def __str__(self):
        return self.name

class VerificationRequest(models.Model):
    USER_TYPES = [('passenger', 'Passenger'), ('driver', 'Driver')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='passenger')
    nida_doc = models.FileField(upload_to='verification_docs/', validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])
    license_doc = models.FileField(upload_to='verification_docs/', null=True, blank=True, validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification for {self.user.username} ({self.user_type})"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

class TripRating(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"Rating for {self.booking}"

class TripRequest(models.Model):
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trip_requests')
    start = models.CharField(max_length=100)
    end = models.CharField(max_length=100)
    preferred_date = models.DateField()
    seats_needed = models.PositiveIntegerField()
    cargo_weight = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('fulfilled', 'Fulfilled'), ('cancelled', 'Cancelled')], default='pending')
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Trip request from {self.start} to {self.end} by {self.passenger.username}"

class Ad(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='ads/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Vehicle(models.Model):
    driver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='vehicles')
    type = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.type} - {self.reg_number}"