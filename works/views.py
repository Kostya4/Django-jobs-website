from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from .models import Vacancy, Company
from .forms import CompanyCreateForm, VacancyCreateForm


class HomePageView(TemplateView):
    template_name = 'jobs/home.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


class CompaniesView(TemplateView):
    template_name = 'jobs/companies.html'

    def get(self, request):
        companies = Company.objects.all()
        params = {
            "companies": companies
        }

        return render(request, self.template_name, params)


class VacanciesView(TemplateView):
    template_name = 'jobs/vacancies.html'

    def get(self, request):
        vacancies = Vacancy.objects.all()
        params = {
            'vacancies': vacancies
        }
        return render(request, self.template_name, params)


class AboutView(TemplateView):
    template_name = 'jobs/about_us.html'

    def get(self, request):
        return render(request, self.template_name)


class CreateCompanyView(View):

    def post(self, request):
        company_form = CompanyCreateForm(request.POST)

        if company_form.is_valid():
            new_company = company_form.save(commit=False)
            new_company.creator = request.user
            new_company = company_form.save()
            return redirect('create-vacancy', new_company.id)
        else:
            return redirect('about')


class ChooseCompanyView(View):

    def post(self, request):
        try:
            company = Company.objects.get(name=request.POST['name'])
            return redirect('create-vacancy', company.id)
        except:
            return redirect('home')


class CreateVacancyView(TemplateView):
    template_name = 'registration/vacancy_registration.html'

    def get(self, request, company_id):

        company_name = Company.objects.get(id=company_id)

        params = {
            'company_name': company_name
        }
        return render(request, self.template_name, params)

    def post(self, request, company_id):
        vacancy_form = VacancyCreateForm(request.POST)

        if vacancy_form.is_valid():
            company_name = Company.objects.get(id=company_id)
            new_vacancy = vacancy_form.save(commit=False)
            new_vacancy.creator = request.user
            new_vacancy.company = company_name
            new_vacancy = new_vacancy.save()
            return redirect('company-detail', company_id)
        else:
            return redirect('create-vacancy', {'errors': vacancy_form.errors})


class CompanyDetailView(TemplateView):
    template_name = 'jobs/company_detail.html'

    def get(self, request, id):
        company = Company.objects.get(id=id)

        params = {
            'company': company
        }

        return render(request, self.template_name, params)


class VacancyDetailView(TemplateView):
    template_name = 'jobs/vacancy_detail.html'

    def get(self, request, id):
        vacancy = Vacancy.objects.get(id=id)

        params = {
            'vacancy': vacancy
        }

        return render(request, self.template_name, params)
