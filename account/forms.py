from django import forms
from .models  import Company, SubscriptionPlan, User

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "name",
            "email_domain",
            "subscription_plan",
            "license_start_date",
            "license_end_date",
        ]

        widgets = {
            "license_start_date": forms.DateInput(attrs={"type": "date"}),
            "license_end_date": forms.DateInput(attrs={"type": "date"}),
        }


class SuperAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
