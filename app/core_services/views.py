from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role.role_name == "operator":
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
