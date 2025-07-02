from django.contrib import admin
from django.utils.html import format_html
from .models import Wing, Category, Room


@admin.register(Wing)
class WingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'preview_image')
    search_fields = ('name',)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "No image"

    preview_image.short_description = "Image"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'price_per_night', 'wing', 'category',
        'beds', 'bedrooms', 'bathrooms', 'guests', 'created_at', 'preview_image'
    )
    list_filter = ('wing', 'category')
    search_fields = (
        'title', 'description', 'price_per_night', 'wing__name',
        'category__name', 'beds', 'bedrooms', 'bathrooms', 'guests'
    )

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "No image"

    preview_image.short_description = "Image"
