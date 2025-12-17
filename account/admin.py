from django.contrib import admin
from .models import SubscriptionPlan, Company, User

# === Django admin dashbord
admin.site.register(SubscriptionPlan)
admin.site.register(Company)
admin.site.register(User)
