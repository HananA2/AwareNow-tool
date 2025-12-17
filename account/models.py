from django.db import models
from django.contrib.auth.models import AbstractUser

# ==== Contract Model => 3 contract saved in DB ====
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    max_users = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    has_platform_support = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# ==== Company Model ====
class Company(models.Model):
    name = models.CharField(max_length=255)
    email_domain = models.CharField(max_length=255)

    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT
    )

    license_start_date = models.DateField()
    license_end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=(
            ('ACTIVE', 'Active'),
            ('EXPIRED', 'Expired'),
            ('SUSPENDED', 'Suspended'),
        ),
        default='ACTIVE'
    )

    def __str__(self):
        return self.name

# ==== User Model ====
class User(AbstractUser):
    ROLE_CHOICES = (
        ('PLATFORM_ADMIN', 'Platform Admin'),
        ('COMPANY_ADMIN', 'Company Admin'),
        ('EMPLOYEE', 'Employee'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    company = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    department = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    activation_token = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )