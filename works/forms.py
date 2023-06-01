from django import forms
from works.models import Company, Vacancy


class CompanyCreateForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ("name", "office_loc", "description", "logo")


class VacancyCreateForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = ("title", "description", "schedule", "experience", "employment", "work_sphere", "low_salary",
                  "high_salary", "currency", "location", "email", "phone_number", "telegram_name", "linkedIn_name")
