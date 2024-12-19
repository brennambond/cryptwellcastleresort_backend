from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Wing, Room, Category
from .serializers import WingSerializer, RoomSerializer, CategorySerializer
from rest_framework import status


@api_view(['GET'])
def wings_list(request):
    wings = Wing.objects.all().order_by('name')
    serializer = WingSerializer(wings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def wing_detail(request, pk):
    wing = get_object_or_404(Wing, pk=pk)
    serializer = WingSerializer(wing)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def categories_list(request):
    categories = Category.objects.all().order_by('name')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def rooms_list(request):
    wing_id = request.GET.get('wing', None)
    category_id = request.GET.get('category', None)

    rooms = Room.objects.all().order_by('title')

    if wing_id:
        rooms = rooms.filter(wing__id=wing_id)

    if category_id:
        rooms = rooms.filter(category__id=category_id)

    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    serializer = RoomSerializer(room)
    return Response(serializer.data, status=status.HTTP_200_OK)
