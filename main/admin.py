from django.contrib import admin
from main.models import *


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'full_name', 'tel_number', 'work_experience']


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'first_name', 'tel_number', 'permission', 'cr_on']


@admin.register(ServiceCosts)
class ServiceCostsAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost']


@admin.register(Styles)
class StylesAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['bot_user', 'employee', 'active']


@admin.register(Order)
class StylesAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkSchedule)
class StylesAdmin(admin.ModelAdmin):
    pass

@admin.register(MessageStep)
class MessageStepAdmin(admin.ModelAdmin):
    pass
