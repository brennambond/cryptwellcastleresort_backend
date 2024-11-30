from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import AccessToken

from .models import Room, Reservation, Wing, Category
from .serializers import RoomsListSerializer, RoomsDetailSerializer, ReservationsListSerializer, WingsListSerializer, CategoryListSerializer, WingsDetailSerializer


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def rooms_list(request):
    rooms = Room.objects.all()

    wing = request.GET.get('wing', '')
    category = request.GET.get('category', '')
    checkin_date = request.GET.get('checkIn', '')
    checkout_date = request.GET.get('checkOut', '')
    beds = request.GET.get('numBeds', '')
    bedrooms = request.GET.get('numBedrooms', '')
    bathrooms = request.GET.get('numBathrooms', '')
    guests = request.GET.get('numGuests', '')

    if checkin_date and checkout_date:
        exact_matches = Reservation.objects.filter(
            start_date=checkin_date) | Reservation.objects.filter(end_date=checkout_date)
        overlap_matches = Reservation.objects.filter(
            start_date__lte=checkout_date, end_date__gte=checkin_date)
        all_matches = []

        for reservation in exact_matches | overlap_matches:
            all_matches.append(reservation.room_id)

        rooms = rooms.exclude(id__in=all_matches)

    if guests:
        rooms = rooms.filter(guests__gte=guests)

    if beds:
        rooms = rooms.filter(beds__gte=beds)

    if bedrooms:
        rooms = rooms.filter(bedrooms__gte=bedrooms)

    if bathrooms:
        rooms = rooms.filter(bathrooms__gte=bathrooms)

    if wing and wing != 'undefined':
        rooms = rooms.filter(wing=wing)

    if category and category != 'undefined':
        rooms = rooms.filter(category=category)

    serializer = RoomsListSerializer(rooms, many=True)

    return JsonResponse({
        'data': serializer.data
    })


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def wings_list(request):
    wings = Wing.objects.all()
    serializer = WingsListSerializer(wings, many=True)

    return JsonResponse({
        'data': serializer.data
    })


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def rooms_detail(request, pk):

    room = Room.objects.get(pk=pk)

    serializer = RoomsDetailSerializer(room, many=False)

    return JsonResponse(serializer.data)


@api_view(['POST'])
def book_room(request, pk):
    try:
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        number_of_nights = request.POST.get('number_of_nights', '')
        total_price = request.POST.get('total_price', '')
        guests = request.POST.get('guests', '')

        room = Room.objects.get(pk=pk)

        Reservation.objects.create(
            room=room,
            start_date=start_date,
            end_date=end_date,
            number_of_nights=number_of_nights,
            total_price=total_price,
            guests=guests,
            created_by=request.user
        )

        return JsonResponse({'success': True})
    except Exception as e:
        print('Error', e)

        return JsonResponse({'success': False})


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def room_reservations(request, pk):
    room = Room.objects.get(pk=pk)
    reservations = room.reservations.all()

    serializer = ReservationsListSerializer(reservations, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def wings_detail(request, pk):

    wing = Wing.objects.get(pk=pk)

    serializer = WingsDetailSerializer(wing, many=False)

    return JsonResponse(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def categories_list(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)

    return JsonResponse({
        'data': serializer.data
    })
