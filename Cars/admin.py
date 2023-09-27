from django.contrib import admin
from .models import (
    ContactUs, Colors, Category, Cars, CarsImages, Additional, GearBoxs,
    BanType, Fuel, Vacancies, VacancyMuraciet, Faq, CarsOrder, FastOrder,
    OrderCancel,
)


class ImageInline(admin.TabularInline):
    model = CarsImages
    extra = 1


class CarsAdmin(admin.ModelAdmin):

    model = Cars
    inlines = (ImageInline, )
    search_fields = ("code",)


class CarsOrderAdmin(admin.ModelAdmin):

    model = CarsOrder
    search_fields = ("code",)
    list_display = ("full_name", "drop_date", "code", "status")
    list_display_links = ("full_name", "drop_date", "status")


class OrderCancelAdmin(admin.ModelAdmin):

    model = CarsOrder
    list_display = ("full_name", "order_code", "status")
    search_fields = ("order_code",)
    list_display_links = ("full_name", "status")


admin.site.register(ContactUs)
admin.site.register(Colors)
admin.site.register(Category)
admin.site.register(Cars,CarsAdmin)
admin.site.register(CarsImages)
admin.site.register(Additional)
admin.site.register(GearBoxs)
admin.site.register(BanType)
admin.site.register(Fuel)
admin.site.register(Vacancies)
admin.site.register(VacancyMuraciet)
admin.site.register(Faq)
admin.site.register(FastOrder)
admin.site.register(CarsOrder, CarsOrderAdmin)
admin.site.register(OrderCancel, OrderCancelAdmin)