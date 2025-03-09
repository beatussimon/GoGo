from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Profile, Trip, Booking, Post, Message, Clan, VerificationRequest, Notification, TripRating, TripRequest, Ad
from django.contrib.auth.models import User
from decimal import Decimal
import json

def is_driver(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_driver and user.profile.verified

def get_notifications(user):
    return Notification.objects.filter(user=user, read=False).order_by('-created_at')

@login_required
def home(request):
    trips = Trip.objects.filter(status='open')[:5]
    clans = Clan.objects.all()[:3]
    trip_requests = TripRequest.objects.filter(status='pending')[:5]
    ads = Ad.objects.filter(active=True).order_by('-created_at')[:3]
    notifications = get_notifications(request.user)
    context = {
        'trips': trips,
        'clans': clans,
        'trip_requests': trip_requests,
        'ads': ads,
        'notifications': notifications,
    }
    return render(request, 'core/home.html', context)

@login_required
def trips(request):
    query = request.GET.get('q', '')
    trips_qs = Trip.objects.filter(status='open')
    if query:
        trips_qs = trips_qs.filter(Q(start__icontains=query) | Q(end__icontains=query))
    if request.method == 'POST':
        filter_type = request.POST.get('filter')
        if filter_type == 'price':
            trips_qs = trips_qs.order_by('price_per_seat')
        elif filter_type == 'seats':
            trips_qs = trips_qs.order_by('-seats')
        elif filter_type == 'cargo':
            trips_qs = trips_qs.order_by('-cargo_capacity')
        else:
            trips_qs = trips_qs.order_by('-departure')
    paginator = Paginator(trips_qs, 10)
    page_number = request.GET.get('page')
    trips = paginator.get_page(page_number)
    context = {
        'trips': trips,
        'query': query,
        'notifications': get_notifications(request.user),
    }
    return render(request, 'core/trips.html', context)

@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    trips = Trip.objects.filter(driver=request.user.profile)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        trip_id = request.POST.get('trip')
        trip = Trip.objects.get(id=trip_id) if trip_id else None
        post = Post.objects.create(user=request.user, content=content, trip=trip)
        if image:
            post.image = image
        if video:
            post.video = video
        post.save()
        messages.success(request, "Post created!")
        return redirect('core:feed')
    context = {
        'posts': posts,
        'trips': trips,
        'notifications': get_notifications(request.user),
    }
    return render(request, 'core/feed.html', context)

@login_required
def chat(request):
    users = User.objects.exclude(id=request.user.id)
    messages_qs = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('timestamp')
    paginator = Paginator(messages_qs, 10)
    page_number = request.GET.get('page')
    messages_list = paginator.get_page(page_number)
    trips = Trip.objects.filter(driver=request.user.profile)
    trip_request_id = request.GET.get('trip_request')
    receiver_id = None
    if trip_request_id:
        trip_request = get_object_or_404(TripRequest, id=trip_request_id)
        receiver_id = trip_request.passenger.id
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver') or receiver_id
        content = request.POST.get('content', '').strip()
        trip_id = request.POST.get('trip')
        receiver = User.objects.get(id=receiver_id)
        trip = Trip.objects.get(id=trip_id) if trip_id else None
        Message.objects.create(sender=request.user, receiver=receiver, content=content, trip=trip)
        messages.success(request, "Message sent!")
        return redirect('core:chat')
    context = {
        'users': users,
        'messages': messages_list,
        'trips': trips,
        'receiver_id': receiver_id,
        'notifications': get_notifications(request.user),
    }
    return render(request, 'core/chat.html', context)

@login_required
def profile(request):
    profile = request.user.profile
    verification_request = VerificationRequest.objects.filter(user=request.user).first()
    trip_requests = TripRequest.objects.filter(passenger=request.user)
    trips = Trip.objects.filter(driver=profile)
    bookings = Booking.objects.filter(passenger=request.user)
    posts = Post.objects.filter(user=request.user)
    clans = Clan.objects.filter(members=request.user)
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile.phone = request.POST.get('phone', '').strip()
            profile.bio = request.POST.get('bio', '').strip()
            profile_pic = request.FILES.get('profile_pic')
            profile.is_driver = 'is_driver' in request.POST
            if profile_pic:
                profile.profile_pic = profile_pic
            profile.save()
            messages.success(request, "Profile updated!")
        elif 'request_verification' in request.POST:
            if not verification_request or verification_request.status != 'pending':
                user_type = request.POST.get('user_type')
                nida_doc = request.FILES.get('nida_doc')
                license_doc = request.FILES.get('license_doc') if user_type == 'driver' else None
                if not nida_doc or (user_type == 'driver' and not license_doc):
                    messages.error(request, "NIDA and license (if driver) required!")
                else:
                    VerificationRequest.objects.create(
                        user=request.user,
                        user_type=user_type,
                        nida_doc=nida_doc,
                        license_doc=license_doc
                    )
                    messages.success(request, "Verification request submitted!")
            else:
                messages.error(request, "Pending verification request exists!")
        return redirect('core:profile')
    context = {
        'profile': profile,
        'verification_request': verification_request,
        'trip_requests': trip_requests,
        'trips': trips,
        'bookings': bookings,
        'posts': posts,
        'clans': clans,
        'notifications': get_notifications(request.user),
    }
    return render(request, 'core/profile.html', context)

@login_required
def book_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, status='open')
    if request.method == 'POST':
        seats = int(request.POST.get('seats', 0))
        cargo_weight = Decimal(request.POST.get('cargo_weight', '0'))
        bid = Decimal(request.POST.get('bid', '0')) if trip.auction_mode else None
        confirm_payment = 'confirm_payment' in request.POST
        if seats <= 0 or seats > trip.seats:
            messages.error(request, "Invalid number of seats!")
        elif cargo_weight < 0 or float(cargo_weight) > trip.cargo_capacity:
            messages.error(request, "Invalid cargo weight!")
        elif trip.auction_mode and bid <= 0:
            messages.error(request, "Invalid bid amount!")
        elif not confirm_payment:
            messages.error(request, "Please confirm payment!")
        else:
            total_cost = (Decimal(seats) * trip.price_per_seat) + (cargo_weight * trip.price_per_kg)
            if trip.auction_mode:
                total_cost = bid
            booking = Booking.objects.create(
                passenger=request.user,
                trip=trip,
                seats=seats,
                cargo_weight=float(cargo_weight),
                bid=bid,
                total_cost=total_cost
            )
            trip.seats -= seats
            trip.cargo_capacity -= float(cargo_weight)
            trip.save()
            Notification.objects.create(
                user=trip.driver.user,
                message=f"{request.user.username} booked your trip from {trip.start} to {trip.end}"
            )
            messages.success(request, "Trip booked!")
            return redirect('core:profile')
    context = {
        'trip': trip,
        'notifications': get_notifications(request.user),
    }
    return render(request, 'core/booking.html', context)

@login_required
@user_passes_test(is_driver)
def new_trip(request):
    if request.method == 'POST':
        start = request.POST.get('start', '').strip()
        end = request.POST.get('end', '').strip()
        seats = int(request.POST.get('seats', 0))
        cargo_capacity = float(request.POST.get('cargo_capacity', 0))
        price_per_seat = Decimal(request.POST.get('price_per_seat', '0'))
        price_per_kg = Decimal(request.POST.get('price_per_kg', '0'))
        departure = request.POST.get('departure')
        auction_mode = 'auction_mode' in request.POST
        departure_dt = timezone.datetime.strptime(departure, '%Y-%m-%dT%H:%M')
        departure_dt = timezone.make_aware(departure_dt)
        if departure_dt < timezone.now():
            messages.error(request, "Departure time cannot be in the past!")
        elif seats <= 0 or cargo_capacity < 0 or price_per_seat < 0 or price_per_kg < 0:
            messages.error(request, "Invalid input values!")
        else:
            Trip.objects.create(
                driver=request.user.profile,
                start=start,
                end=end,
                seats=seats,
                cargo_capacity=cargo_capacity,
                price_per_seat=price_per_seat,
                price_per_kg=price_per_kg,
                departure=departure_dt,
                auction_mode=auction_mode
            )
            messages.success(request, "Trip created!")
            return redirect('core:profile')
    context = {
        'notifications': get_notifications(request.user),
    }
    return render(request, 'core/new_trip.html', context)

@login_required
def request_trip(request):
    if request.method == 'POST':
        start = request.POST.get('start', '').strip()
        end = request.POST.get('end', '').strip()
        preferred_date = request.POST.get('preferred_date')
        seats_needed = int(request.POST.get('seats_needed', 0))
        cargo_weight = float(request.POST.get('cargo_weight', 0))
        if seats_needed <= 0 or cargo_weight < 0:
            messages.error(request, "Invalid input values!")
        else:
            TripRequest.objects.create(
                passenger=request.user,
                start=start,
                end=end,
                preferred_date=preferred_date,
                seats_needed=seats_needed,
                cargo_weight=cargo_weight
            )
            messages.success(request, "Trip request submitted!")
            return redirect('core:profile')
    context = {
        'notifications': get_notifications(request.user),
    }
    return render(request, 'core/request_trip.html', context)

@login_required
@user_passes_test(is_driver)
def fulfill_trip_request(request, request_id):
    trip_request = get_object_or_404(TripRequest, id=request_id, status='pending')
    if request.method == 'POST':
        seats = int(request.POST.get('seats', 0))
        cargo_capacity = float(request.POST.get('cargo_capacity', 0))
        price_per_seat = Decimal(request.POST.get('price_per_seat', '0'))
        price_per_kg = Decimal(request.POST.get('price_per_kg', '0'))
        departure = request.POST.get('departure')
        auction_mode = 'auction_mode' in request.POST
        departure_dt = timezone.datetime.strptime(departure, '%Y-%m-%dT%H:%M')
        departure_dt = timezone.make_aware(departure_dt)
        if departure_dt < timezone.now():
            messages.error(request, "Departure time cannot be in the past!")
        elif seats < trip_request.seats_needed or cargo_capacity < trip_request.cargo_weight:
            messages.error(request, "Insufficient seats or cargo capacity!")
        else:
            trip = Trip.objects.create(
                driver=request.user.profile,
                start=trip_request.start,
                end=trip_request.end,
                seats=seats,
                cargo_capacity=cargo_capacity,
                price_per_seat=price_per_seat,
                price_per_kg=price_per_kg,
                departure=departure_dt,
                auction_mode=auction_mode
            )
            trip_request.status = 'fulfilled'
            trip_request.trip = trip
            trip_request.save()
            Notification.objects.create(
                user=trip_request.passenger,
                message=f"Your trip request from {trip_request.start} to {trip_request.end} has been fulfilled!"
            )
            messages.success(request, "Trip request fulfilled!")
            return redirect('core:home')
    context = {
        'trip_request': trip_request,
        'notifications': get_notifications(request.user),
    }
    return render(request, 'core/fulfill_trip_request.html', context)

@login_required
def join_clan(request, clan_id):
    clan = get_object_or_404(Clan, id=clan_id)
    if request.user not in clan.members.all():
        clan.members.add(request.user)
        messages.success(request, f"Joined {clan.name}!")
    return redirect('core:home')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.POST.get('next', 'core:home'))
        messages.error(request, "Invalid credentials!")
    return render(request, 'core/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out!")
    return redirect('core:login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username taken!")
        else:
            user = User.objects.create_user(username=username, password=password)
            Profile.objects.create(user=user, phone=phone)
            messages.success(request, "Registered! Please log in.")
            return redirect('core:login')
    return render(request, 'core/register.html')

@login_required
def cancel_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, driver=request.user.profile)
    if request.method == 'POST':
        trip.status = 'cancelled'
        trip.save()
        for booking in trip.bookings.all():
            booking.status = 'cancelled'
            booking.save()
            Notification.objects.create(
                user=booking.passenger,
                message=f"Your booking for {trip.start} to {trip.end} has been cancelled."
            )
        messages.success(request, "Trip cancelled!")
        return redirect('core:profile')
    context = {
        'trip': trip,
        'notifications': get_notifications(request.user),
    }
    return render(request, 'core/cancel_trip.html', context)

@login_required
def rate_trip(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, passenger=request.user, status='completed')
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comments = request.POST.get('comments', '')
        TripRating.objects.create(booking=booking, rating=rating, comments=comments)
        driver = booking.trip.driver
        ratings = TripRating.objects.filter(booking__trip__driver=driver)
        driver.hype_score = sum(r.rating for r in ratings) / ratings.count()
        driver.save()
        messages.success(request, "Trip rated!")
        return redirect('core:profile')
    context = {
        'booking': booking,
        'notifications': get_notifications(request.user),
    }
    return render(request, 'core/rate_trip.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    verification_requests = VerificationRequest.objects.filter(status='pending')
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        comments = request.POST.get('comments', '')
        verification_request = get_object_or_404(VerificationRequest, id=request_id)
        if action == 'approve':
            verification_request.status = 'approved'
            verification_request.user.profile.verified = True
            if verification_request.user_type == 'driver':
                verification_request.user.profile.is_driver = True
            verification_request.user.profile.save()
        elif action == 'reject':
            verification_request.status = 'rejected'
            verification_request.comments = comments
        verification_request.save()
        messages.success(request, f"Verification {action}d!")
        return redirect('core:admin_dashboard')
    context = {
        'verification_requests': verification_requests,
    }
    return render(request, 'core/admin_dashboard.html', context)

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return redirect('core:profile')