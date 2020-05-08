from django.shortcuts import render, get_object_or_404
from .models import Item
from django.views.generic import ListView, TemplateView, DetailView
from django.db.models import Q


class IndexView(ListView):
    template_name = 'itemviewer/index.html'
    context_object_name = 'latest_items'

    def get_queryset(self):
        return Item.objects.order_by('-id')[:25]
    # latest_items = Item.objects.order_by('-id')[:25]
    # context = {'latest_items': latest_items}
    # context = {}
    # if 'search' in request.GET:
    #     latest_items = Item.objects.order_by('-id')[:25]
    #     context = {'latest_items': latest_items}
    # return render(request, 'itemviewer/index.html', context)


class DetailView(DetailView):
    template_name = 'itemviewer/detail.html'
    context_object_name = 'item'

    def get_queryset(self):
        return Item.objects


class SearchView(ListView):
    model = Item
    template_name = 'itemviewer/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        item_list = Item.objects.filter(
            Q(typeline__icontains=query)
        )[:100]
        return item_list
