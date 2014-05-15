from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context

class CollectionListView(ListView):
	pass

class CollectionView(DetailView):
	pass

class RecordView(DetailView):
	pass