from rest_framework import viewsets, filters
from rest_framework.decorators import action, link
from rest_framework.response import Response

from inventory.api_serializers import *

from inventory.models import *

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

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name','details')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        return FlatItemSerializer

class ItemCategoryViewSet(viewsets.ModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer

class ItemStatusViewSet(viewsets.ModelViewSet):
    queryset = ItemStatus.objects.all()
    serializer_class = ItemStatusSerializer

class ItemOwnerViewSet(viewsets.ModelViewSet):
    queryset = ItemOwner.objects.all()
    serializer_class = ItemOwnerSerializer

class ItemResponsiblePositionViewSet(viewsets.ModelViewSet):
    queryset = ItemResponsiblePosition.objects.all()
    serializer_class = ItemResponsiblePositionSerializer

class ItemHomeViewSet(viewsets.ModelViewSet):
    queryset = ItemHome.objects.all()
    serializer_class = ItemHomeSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class ItemNoteViewSet(viewsets.ModelViewSet):
    queryset = ItemNote.objects.all()
    serializer_class = ItemNoteSerializer

class ItemPictureViewSet(viewsets.ModelViewSet):
    queryset = ItemPicture.objects.all()
    serializer_class = ItemPictureSerializer

class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

