from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from .models import DriverProfile, DriverJobRun
from django.utils.dateparse import parse_date
from datetime import datetime


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
def job_running_view(request):
    user = request.user
    month = request.GET.get("month", "01")
    year = request.GET.get("year", "2024")

    # Fetch job run data based on the selected month and year
    job_run_data = DriverJobRun.objects.filter(
        user=user, date__year=year, date__month=month
    ).order_by("date")

    # Serialize job_run_data to JSON
    job_run_data = serialize(
        "json", job_run_data, use_natural_primary_keys=True
    )

    context = {
        "job_run_data": job_run_data,
        "month": month,
        "year": year,
    }
    return render(request, "jobRunning.html", context)


def submit_job_running(request):
    if request.method == "POST":
        month = request.POST.get("month")
        year = request.POST.get("year")

        # Define daysInMonth dictionary
        daysInMonth = {
            "01": 31,
            "02": 28,
            "03": 31,
            "04": 30,
            "05": 31,
            "06": 30,
            "07": 31,
            "08": 31,
            "09": 30,
            "10": 31,
            "11": 30,
            "12": 31,
        }

        month = request.POST.get("month")
        year = request.POST.get("year")

        # Check if it's a leap year for February
        if month == "02" and (
            (int(year) % 4 == 0 and int(year) % 100 != 0)
            or (int(year) % 400 == 0)
        ):
            daysInMonth["02"] = 29

        num_days = daysInMonth.get(
            month, 31
        )  # Default to 31 if month is invalid

        for day in range(1, num_days + 1):
            round_key = f"round_{day}"
            remarks_key = f"remarks_{day}"

            round_value = request.POST.get(round_key, "").strip()
            remarks_value = request.POST.get(remarks_key, "").strip()

            if (
                round_value or remarks_value
            ):  # Save only if either value is not empty
                date_str = f"{year}-{month}-{str(day).zfill(2)}"
                date = datetime.strptime(date_str, "%Y-%m-%d").date()

                # Create and save the DriverJobRun instance
                driver_job_run, _ = DriverJobRun.objects.update_or_create(
                    user=request.user,
                    date=date,
                )

                driver_job_run.round_info = round_value
                driver_job_run.remarks = remarks_value
                driver_job_run.save()

        return redirect(
            job_running_view
        )  # Redirect to a success page or wherever you need
    else:
        print(request)

    return HttpResponse("Invalid request method.", status=405)


@login_required
def driver_dashboard_view(request):
    return render(request, "driverMenu.html")


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
