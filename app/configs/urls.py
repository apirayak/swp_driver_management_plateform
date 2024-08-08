"""configs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from core_services.views import (
    login_view,
    driver_info_view,
    driver_dashboard_view,
    job_running_view,
    mile_update_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="/login/"), name="logout"),
    path(
        "driver-info/", driver_info_view, name="driver_info"
    ),  # Add your actual view for driver info
    path("driver-dashboard/", driver_dashboard_view, name="driver_dashboard"),
    path("job-running/", job_running_view, name="job_running"),
    path("mile-update/", mile_update_view, name="mile_update"),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
