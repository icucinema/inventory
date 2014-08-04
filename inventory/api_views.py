from rest_framework import viewsets, filters, views
from rest_framework.decorators import action, link
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from django.db import transaction

from inventory.api_serializers import *
from inventory.models import *

import reversion

class ReversionModelViewSet(viewsets.ModelViewSet):
    def create(self, request):
        with transaction.atomic(), reversion.create_revision():
            reversion.set_user(request.user)
            return super(viewsets.ModelViewSet, self).create(request)

    def update(self, request, pk=None):
        with transaction.atomic(), reversion.create_revision():
            reversion.set_user(request.user)
            return super(viewsets.ModelViewSet, self).update(request, pk)
 
    def partial_update(self, request, pk=None):
        with transaction.atomic(), reversion.create_revision():
            reversion.set_user(request.user)
            return super(viewsets.ModelViewSet, self).partial_update(request, pk)

    def destroy(self, request, pk=None):
        with transaction.atomic(), reversion.create_revision():
            reversion.set_user(request.user)
            return super(viewsets.ModelViewSet, self).destroy(request, pk)

def serialize_queryset(self, serializer_class, queryset):
    self.serializer_class = serializer_class 
    self.paginate_by = None
    self.object_list = queryset

    page = self.paginate_queryset(self.object_list)
    if page is not None:
        serializer = self.get_pagination_serializer(page)
    else:
        serializer = self.get_serializer(self.object_list, many=True)

    return Response(serializer.data)

class ItemViewSet(ReversionModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name','details')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        return FlatItemSerializer

    @action(methods=['GET'])
    def notes(self, request, pk=None):
        item = self.get_object()
        return serialize_queryset(self, ItemNoteSerializer, item.notes.all())

    @action(methods=['GET'])
    def pictures(self, request, pk=None):
        item = self.get_object()
        return serialize_queryset(self, ItemPictureSerializer, item.pictures.all())

    @action(methods=['GET'])
    def quotes(self, request, pk=None):
        item = self.get_object()
        return serialize_queryset(self, QuoteSerializer, item.quotes.all())

class ItemCategoryViewSet(ReversionModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer

class ItemStatusViewSet(ReversionModelViewSet):
    queryset = ItemStatus.objects.all()
    serializer_class = ItemStatusSerializer

class ItemOwnerViewSet(ReversionModelViewSet):
    queryset = ItemOwner.objects.all()
    serializer_class = ItemOwnerSerializer

class ItemResponsiblePositionViewSet(ReversionModelViewSet):
    queryset = ItemResponsiblePosition.objects.all()
    serializer_class = ItemResponsiblePositionSerializer

class ItemHomeViewSet(ReversionModelViewSet):
    queryset = ItemHome.objects.all()
    serializer_class = ItemHomeSerializer

class SupplierViewSet(ReversionModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)

class ItemNoteViewSet(ReversionModelViewSet):
    queryset = ItemNote.objects.all()
    serializer_class = ItemNoteSerializer

class ItemPictureViewSet(ReversionModelViewSet):
    queryset = ItemPicture.objects.all()
    serializer_class = ItemPictureSerializer
    parser_classes = (FormParser, MultiPartParser,)

    def put(self, request):
        with transaction.atomic(), reversion.create_revision():
            reversion.set_user(request.user)

            file_obj = request.FILES['file']
            print request.DATA['item']
            lowerName = file_obj.name.lower()
            extension = None

            if lowerName[-3:] == "png":
                extension = "png"
            elif lowerName[-3:] == "jpg":
                extension = "jpg"
            elif lowerName[-4:] == "jpeg":
                extension = "jpg"

            if extension is None:
                return Response(status=400)

            instance = ItemPicture(item = Item.objects.get(pk=request.DATA['item']), image = request.FILES['file'])
            instance.save()

            return Response(status=204)

class QuoteViewSet(ReversionModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        return FlatQuoteSerializer


