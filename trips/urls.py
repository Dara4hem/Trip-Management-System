from django.urls import path
from .views import TripListCreateView, TripDetailView, TripLogEntriesView, TripPDFView

urlpatterns = [
    path("trips/", TripListCreateView.as_view(), name="trip-list"),
    path("trips/<int:pk>/", TripDetailView.as_view(), name="trip-detail"), 
    path("trips/<int:pk>/logs/", TripLogEntriesView.as_view(), name="trip-logs"),
    path("trips/<int:pk>/pdf/", TripPDFView.as_view(), name="trip-pdf"),
]
