from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (
    ClientUser,
    Feedback,
    Invoice,
    Master,
    MasterDaySchedule,
    Order,
    Salon,
    Service,
    ServiceType,
)


@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "full_name")
    search_fields = ("phone_number", "full_name")
    list_filter = ("full_name",)


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ("title", "address")


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "price", "duration")


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ("full_name", "specialty")


class ServiceInline(admin.TabularInline):
    model = MasterDaySchedule.services.through
    extra = 0
    verbose_name = "Услуга"
    verbose_name_plural = "Услуги"


@admin.register(MasterDaySchedule)
class MasterDayScheduleAdmin(admin.ModelAdmin):
    list_filter = ("workday", "salon", "master", )
    search_fields = ("workday", "salon", "master")
    exclude = ("services",)
    inlines = [ServiceInline]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("updated_at", "client", "status")
    list_filter = ("status",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("date", "status", "client", "salon", "master", "service")
    list_filter = ("date", "status", "client", "salon", "master", "service")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("date", "client")
    list_filter = ("date", "client")


admin.site.unregister(Group)
