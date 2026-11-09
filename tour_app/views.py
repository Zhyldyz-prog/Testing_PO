from django.shortcuts import render, redirect, get_object_or_404
from .models import Tour, Booking, TourComment


def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'tour_app/tour_list.html', {'tours': tours})


def create_booking(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        if Booking.objects.filter(user=request.user, booking_date=date, booking_time=time).exists():
            return render(request, 'tour_app/tour_list.html', {
                'tours': Tour.objects.all(),
                'error': 'Вы уже забронировали тур на это время!'
            }, status=400)
            
        Booking.objects.create(user=request.user, tour=tour, booking_date=date, booking_time=time)
        return redirect('tour_list')
    return redirect('tour_list')


def add_comment(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            TourComment.objects.create(tour=tour, user=request.user, text=text)
        return redirect('tour_list')
    return redirect('tour_list')