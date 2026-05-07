from django.urls import path
from .views import JobListView , ApplyToJobView

urlpatterns = [
    path("jobs/<int:id>/apply" , ApplyToJobView.as_view()),
    path("jobs/" , JobListView.as_view())
] 
