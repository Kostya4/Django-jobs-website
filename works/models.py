from django.db import models
from django.urls import reverse


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    schedule = models.ForeignKey('Schedule', on_delete=models.PROTECT)
    experience = models.ForeignKey('Experience', on_delete=models.PROTECT)
    employment = models.ForeignKey('Employment', on_delete=models.PROTECT)
    work_sphere = models.ForeignKey('Sphere', on_delete=models.PROTECT)

    low_salary = models.IntegerField(blank=True, null=True)
    high_salary = models.IntegerField(blank=True, null=True)
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=11, blank=True)
    telegram_name = models.CharField(max_length=30, blank=True)
    linkedIn_name = models.CharField(max_length=30, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='vacancies')
    creator = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='all_vacancies')

    def __str__(self):
        return self.title

    def get_salary(self):
        if self.low_salary and self.high_salary:
            return f"From {self.low_salary} to {self.high_salary} {self.currency if not None else ' '}"
        elif self.low_salary:
            return f"From {self.low_salary} {self.currency if None else ' '}"
        elif self.high_salary:
            return f"Up to {self.high_salary} {self.currency if None else ' '}"
        else:
            return False

    def get_absolute_url(self):
        return reverse("vacancy-detail", args=[self.id])

    def get_contacts(self):
        all_contacts = [str(self.email), str(self.phone_number), str(self.telegram_name), str(self.linkedIn_name)]
        contacts = [contact for contact in all_contacts if len(contact) != 0]
        contacts_str = ','.join(contacts)
        return contacts_str

    @classmethod
    def quantity_of_vacancies(cls):
        return len(Vacancy.objects.all())


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    office_loc = models.CharField(max_length=50)

    description = models.TextField(max_length=5000)
    logo = models.ImageField(null=True, blank=True, upload_to='companies', default='')

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='companies')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("company-detail", args=[self.id])

    @classmethod
    def quantity_of_companies(cls):
        return len(Company.objects.all())


class Schedule(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Experience(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Employment(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Sphere(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
