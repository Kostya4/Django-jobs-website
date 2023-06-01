from django.urls import path
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("companies/", CompaniesView.as_view(), name='companies'),
    path("vacancies/", VacanciesView.as_view(), name='vacancies'),
    path("about/", AboutView.as_view(), name='about'),
    path("create-company/", CreateCompanyView.as_view(), name='create-company'),
    path("choose-company/", ChooseCompanyView.as_view(), name='choose-company'),
    path('company-<int:company_id>/create-vacancy/', CreateVacancyView.as_view(), name='create-vacancy'),
    path('companies/company-<int:id>/', CompanyDetailView.as_view(), name='company-detail'),
    path('vacancies/vacancy-<int:id>/', VacancyDetailView.as_view(), name='vacancy-detail'),
]
