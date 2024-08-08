from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import DriverProfile


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Check user role and redirect accordingly
            if user.role.role_name == "driver":
                return redirect(
                    "driver_dashboard"
                )  # Update with your actual view name
            elif user.role.role_name == "operator":
                return redirect(
                    "operator_menu"
                )  # Update with your actual view name
            else:
                return redirect(
                    "user_menu"
                )  # Update with your actual view name
        else:
            return render(
                request,
                "login.html",
                {"error": "Invalid username or password."},
            )

    return render(request, "login.html")


@login_required
def driver_dashboard_view(request):
    return render(request, "driver_dashboard.html")


@login_required
def job_running_view(request):
    return render(request, "jobRunning.html")


@login_required
def mile_update_view(request):
    return render(request, "mileUpdate.html")


@login_required
def driver_info_view(request):
    # Fetch the driver profile for the logged-in user
    try:
        driver_profile = DriverProfile.objects.get(user=request.user)
    except DriverProfile.DoesNotExist:
        # Handle case where profile doesn't exist
        driver_profile = None

    return render(
        request, "driverInfo.html", {"driver_profile": driver_profile}
    )
