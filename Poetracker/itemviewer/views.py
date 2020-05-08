from .models import Item
from django.views.generic import ListView, TemplateView
from django.db.models import Q


# define the index view
class IndexView(TemplateView):
    template_name = 'itemviewer/index.html'


class SearchView(ListView):
    model = Item
    template_name = 'itemviewer/search_results.html'

    def get_queryset(self):
        name_query = self.request.GET.get('name')
        type_query = self.request.GET.get('type')
        league_query = self.request.GET.get('league')
        item_list = Item.objects.filter(
            Q(typeline__icontains=type_query) & Q(name__icontains=name_query) & Q(league__icontains=league_query)
        )[:500]
        return item_list
