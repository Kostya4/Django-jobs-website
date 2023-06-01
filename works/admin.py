from django.contrib import admin
from .models import Vacancy, Company, Experience, Employment, Sphere, Schedule, Currency


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'schedule', 'experience', 'employment', 'work_sphere']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'office_loc', 'description', 'logo']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Sphere)
class SphereAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name']
