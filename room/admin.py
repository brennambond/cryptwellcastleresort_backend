from django.contrib import admin
from .models import Wing, Category, Room


@admin.register(Wing)
class WingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'image')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price_per_night',
                    'wing', 'category', 'beds', 'bedrooms', 'bathrooms', 'guests', 'created_at', 'image')
    list_filter = ('wing', 'category')
    search_fields = ('title', 'description', 'price_per_night', 'wing',
                     'category', 'beds', 'bedrooms', 'bathrooms', 'guests')
