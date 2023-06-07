from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from .models import Vacancy, Company
from .forms import CompanyCreateForm, VacancyCreateForm


class HomePageView(TemplateView):
    template_name = 'jobs/home.html'

    def get(self, request):
        q_companies = Company.quantity_of_companies()
        q_vacancies = Vacancy.quantity_of_vacancies()

        params = {'q_companies': q_companies,
                  'q_vacancies': q_vacancies,
                  }
        return render(request, self.template_name, params)


class VacanciesView(TemplateView):
    template_name = 'jobs/vacancies.html'

    def get(self, request):
        vacancies = Vacancy.objects.all()
        params = {
            'vacancies': vacancies,
        }
        return render(request, self.template_name, params)


class CompaniesView(TemplateView):
    template_name = 'jobs/companies.html'

    def get(self, request):
        companies = Company.objects.all()
        params = {
            "companies": companies,
        }

        return render(request, self.template_name, params)


class AboutView(TemplateView):
    template_name = 'jobs/about_us.html'

    def get(self, request):
        params = {
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


class CompanyDetailView(TemplateView):
    template_name = 'jobs/company_detail.html'

    def get(self, request, id):
        company = Company.objects.get(id=id)

        params = {
            'company': company
        }

        return render(request, self.template_name, params)


class CreateCompanyView(View):

    def post(self, request):
        company_form = CompanyCreateForm(request.POST, request.FILES)
        if company_form.is_valid():
            new_company = company_form.save(commit=False)
            new_company.creator = request.user
            new_company = company_form.save()
            return redirect('create-vacancy', new_company.id)
        else:
            return render(request, 'jobs/home.html', {'company_form': company_form})


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
            new_vacancy.save()
            return redirect('vacancy-detail', new_vacancy.id)
        else:
            return render(request, 'registration/vacancy_registration.html', {'vacancy_form': vacancy_form})


class ChooseCompanyView(View):

    def post(self, request):
        try:
            company = Company.objects.get(name=request.POST['name'])
            return redirect('create-vacancy', company.id)
        except:
            messages.info(request, 'The company you selected does not exist, but you can always create one')
            return redirect(self.request.META.get('HTTP_REFERER'), messages)


class CompanySearchView(TemplateView):
    template_name = 'jobs/companies.html'

    def post(self, request):
        search = request.POST['company_name']
        search_list = search.split()
        if len(search_list) > 0:
            companies_by_all = Company.objects.none()
            for keyword in search_list:
                company = Company.objects.filter(name__icontains=keyword)
                companies_by_all = companies_by_all.union(company)
            if len(companies_by_all) == 0:
                params = {
                    'request_msg': f"Sorry, we didn't find anything similar to '{search}'"
                }
                return render(request, self.template_name, params)

        else:
            companies_by_all = Company.objects.all()

        params = {
            'companies': companies_by_all,
            'request_msg': f"All matches on request '{search}'" if len(search_list) != 0 else False
        }
        return render(request, self.template_name, params)


class VacancySearchView(TemplateView):
    template_name = 'jobs/vacancies.html'

    def post(self, request):
        vacancies_list = list()

        if keyword := request.POST.get('work_sphere', False):
            vacancies_by_sphere = set(Vacancy.objects.filter(work_sphere=int(keyword)))
            vacancies_list.append(vacancies_by_sphere)
        if keyword := request.POST.get('schedule', False):
            vacancies_by_schedule = set(Vacancy.objects.filter(schedule=int(keyword)))
            vacancies_list.append(vacancies_by_schedule)
        if keyword := request.POST.get('experience', False):
            vacancies_by_experience = set(Vacancy.objects.filter(experience=int(keyword)))
            vacancies_list.append(vacancies_by_experience)
        if keyword := request.POST.get('employment', False):
            vacancies_by_employment = set(Vacancy.objects.filter(employment=int(keyword)))
            vacancies_list.append(vacancies_by_employment)
        if keyword := request.POST.get('low_salary', False):
            vacancies_by_salary = set(Vacancy.objects.filter(low_salary__gte=int(keyword)))
            vacancies_list.append(vacancies_by_salary)

        if vacancies_list:
            vacancies_by_all = set.intersection(*vacancies_list)
            if vacancies_by_all:
                params = {
                    "vacancies": vacancies_by_all
                }

            else:
                request_msg = 'No matches for your filter'
                params = {
                    'request_msg': request_msg
                }
        else:
            params = {
                'vacancies': Vacancy.objects.all()
            }
        return render(request, self.template_name, params)


class DetailSearchView(TemplateView):
    template_name = 'jobs/vacancies.html'

    def sorted_by_name(self, keyword):
        return Vacancy.objects.filter(title__icontains=keyword)

    def sorted_by_company(self, keyword):
        companies = Company.objects.filter(name__icontains=keyword)
        all_vacancies = Vacancy.objects.none()
        if len(companies) > 0:
            for company in companies:
                vacancies = Vacancy.objects.filter(company=company.id)
                all_vacancies = all_vacancies.union(vacancies)
        return all_vacancies

    def sorted_by_description(self, keyword):
        return Vacancy.objects.filter(title__icontains=keyword)

    def post(self, request):
        search = request.POST['search']
        search_list = search.split()
        if len(search_list) > 0:
            vacancies_by_all = Vacancy.objects.none()
            for keyword in search_list:
                if request.POST.get('job_title', False):
                    vacancies_by_name = self.sorted_by_name(keyword)
                    vacancies_by_all = vacancies_by_all.union(vacancies_by_name)
                if request.POST.get('company_title', False):
                    vacancies_by_company = self.sorted_by_company(keyword)
                    vacancies_by_all = vacancies_by_all.union(vacancies_by_company)
                if request.POST.get('job_description', False):
                    vacancies_by_description = self.sorted_by_description(keyword)
                    vacancies_by_all = vacancies_by_all.union(vacancies_by_description)
            if len(vacancies_by_all) == 0:
                params = {
                    'request_msg': f"Sorry, we didn't find anything similar to '{search}'"
                }
                return render(request, self.template_name, params)
        else:
            vacancies_by_all = Vacancy.objects.all()

        params = {
            'vacancies': vacancies_by_all,
            'request_msg': f"All matches on request '{search}'" if len(search_list) != 0 else False
        }
        return render(request, self.template_name, params)
