from django.urls import path

from .views import IndexView, SearchView

# link paths with views
app_name = 'itemviewer'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', SearchView.as_view(), name="search_results")
]
