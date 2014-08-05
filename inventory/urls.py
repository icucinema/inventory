from django.conf.urls import patterns, include, url

from rest_framework import routers

from inventory import api_views
from inventory import api_router
from inventory import views

api_router = api_router.APIRouter()
api_router.register(r'item', api_views.ItemViewSet)
api_router.register(r'itemcategory', api_views.ItemCategoryViewSet)
api_router.register(r'itemstatus', api_views.ItemStatusViewSet)
api_router.register(r'itemowner', api_views.ItemOwnerViewSet)
api_router.register(r'itemresponsibleposition', api_views.ItemResponsiblePositionViewSet)
api_router.register(r'itemhome', api_views.ItemHomeViewSet)
api_router.register(r'supplier', api_views.SupplierViewSet)
api_router.register(r'itemnote', api_views.ItemNoteViewSet)
api_router.register(r'itempicture', api_views.ItemPictureViewSet)
api_router.register(r'quote', api_views.QuoteViewSet)
api_router.register(r'instance', api_views.InstanceViewSet)

urlpatterns = patterns('',
        url(r'^$', views.IndexView.as_view(), name='root'),
        url(r'^asset/(?P<asset_id>\d+)$', views.asset_view),
        url(r'^(?P<partial>partials/[a-z]+\.html)$', views.angular_partial_view),
)
api_urlpatterns = api_router.urls


