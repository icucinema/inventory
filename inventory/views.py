from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.staticfiles.storage import staticfiles_storage

from inventory.models import Instance

# Create your views here.

class IndexView(TemplateView):
    template_name = 'inventory/index.html'

def angular_partial_view(request, partial):

    exit_url = staticfiles_storage.url('inventory/' + partial)
    if exit_url.startswith('http:'):
        exit_url = 'https:' + exit_url[5:]

    return HttpResponseRedirect(exit_url)

def asset_view(request, asset_id):
    print asset_id

    i = Instance.objects.get(pk=int(asset_id))

    print reverse('inventory:root')

    return HttpResponseRedirect(reverse('inventory:root')+"#/item/"+str(i.item.id))

