from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CompanyForm
from django.contrib.auth.decorators import login_required
import uuid
from .forms import SuperAdminForm
from .models import Company
from .services import send_activation_email


# ==== admin platform login ====
@login_required
def platform_dashboard(request):
    return render(request, "account/platform_dashboard.html")

def platform_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and user.is_superuser:
            login(request, user)
            return redirect("account:platform-dashboard")

        return render(request, "account/login.html", {
            "error": "Invalid credentials or not a platform admin"
        })

    return render(request, "account/login.html")

# ==== admin platform create company ====
@login_required
def create_company(request):
    if not request.user.is_superuser:
        return redirect("account:platform-login")

    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            # create superadmin for company
            return redirect("account:create-super-admin", company_id=company.id)
    else:
        form = CompanyForm()

    return render(request, "account/create_company.html", {"form": form})

@login_required
def create_super_admin(request, company_id):
    if not request.user.is_superuser:
        return redirect("account:platform-login")

    company = Company.objects.get(id=company_id)

    if request.method == "POST":
        form = SuperAdminForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "COMPANY_ADMIN"
            user.company = company
            user.is_active = False
            user.set_unusable_password()
            user.activation_token = uuid.uuid4()
            user.save()

            send_activation_email(user)

            return render(request, "account/super_admin_created.html", {
                "email": user.email
            })
    else:
        form = SuperAdminForm()

    return render(request, "account/create_super_admin.html", {
        "form": form,
        "company": company
    })



# import uuid
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib.auth import get_user_model
# from django.utils import timezone
# from django.core.mail import send_mail
# from django.views.decorators.csrf import csrf_exempt

# User = get_user_model()

# def send_activation_email(user):
#     activation_link = f"http://127.0.0.1:8000/account/activate/{user.activation_token}/"

#     send_mail(
#         subject="Activate your AwareNow account",
#         message=f"Click the link to activate your account:\n{activation_link}",
#         from_email=None,
#         recipient_list=[user.email],
#     )

# @csrf_exempt
# def activate_account(request, token):
#     try:
#         user = User.objects.get(activation_token=token)
#     except User.DoesNotExist:
#         return HttpResponse("Invalid activation link", status=400)

#     if request.method == "POST":
#         password = request.POST.get("password")
#         department = request.POST.get("department")

#         if not password or not department:
#             return HttpResponse("All fields are required", status=400)

#         user.set_password(password)
#         user.department = department
#         user.is_active = True
#         user.activation_token = None
#         user.save()

#         return HttpResponse("Account activated successfully. You can now log in.")

#     # GET request (صفحة بسيطة جدًا)
#     return HttpResponse("""
#         <h2>Activate Account</h2>
#         <form method="post">
#             <input type="password" name="password" placeholder="Password" required /><br><br>
#             <input type="text" name="department" placeholder="Department" required /><br><br>
#             <button type="submit">Activate</button>
#         </form>
#     """)

