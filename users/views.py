from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from users.forms import CustomUserCreationForm, LoginUserForm
from users.models import User
from works.models import Company, Vacancy


class SignUpView(View):

    def post(self, request):
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password2'])
            new_user.save()

            new_user = authenticate(
                email=user_form.cleaned_data['email'], password=user_form.cleaned_data['password2']
            )

            login(request, new_user)
            return redirect('home')
        else:
            return render(request, 'jobs/home.html', {'user_form': user_form})


class LoginUserView(LoginView):

    def post(self, request):
        login_form = LoginUserForm(request.POST)
        try:
            user = authenticate(email=request.POST['email'], password=request.POST['password2'])
            login(request, user)
            return redirect('home')
        except:
            login_form.errors_message = "Enter the correct email and password for authorization"
            return render(request, 'jobs/home.html', {'login_form': login_form})


class LogoutUserView(LogoutView):

    def get(self, request):
        logout(request)
        return redirect('home')


class UserProfile(TemplateView):
    template_name = 'jobs/user_profile.html'

    def get(self, request, user_id):
        my_companies = Company.objects.order_by('-updated_at').filter(creator=request.user)
        my_vacancies = Vacancy.objects.order_by('-updated_at').filter(creator=request.user)
        params = {'my_companies': my_companies,
                  'my_vacancies': my_vacancies}
        return render(request, self.template_name, params)
