# store_monitoring/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store_monitor/', include('store_monitor.urls')),
]
