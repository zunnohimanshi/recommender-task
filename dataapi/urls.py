from django.urls import path
from .views import SubmitDataView

urlpatterns = [
    path('submit/', SubmitDataView.as_view(), name='submit'),
]
