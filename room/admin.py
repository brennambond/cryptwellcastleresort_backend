from django.contrib import admin
from .models import Room, Wing, Category

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'wing', 'category',
                    'price_per_night', 'guests', 'availability_status')
    list_filter = ('wing', 'category', 'availability_status')
    search_fields = ('title',)


@admin.register(Wing)
class WingAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
