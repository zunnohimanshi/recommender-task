from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dataapi.urls')),  # ✅ This is enough to enable /submit/
    path('test/', lambda request: HttpResponse("Test OK ✅")),
]
