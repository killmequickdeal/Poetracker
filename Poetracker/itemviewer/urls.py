from django.urls import path

from .views import IndexView, DetailView, SearchView

app_name = 'itemviewer'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', DetailView.as_view(), name='detail'),
    path('search/', SearchView.as_view(), name="search_results")
]
