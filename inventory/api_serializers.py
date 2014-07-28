from rest_framework.serializers import HyperlinkedModelSerializer

from inventory import models

class ItemCategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.ItemCategory
        fields = ('url', 'id', 'name', 'description',)

class ItemStatusSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.ItemStatus
        fields = ('url', 'id', 'name')

class ItemOwnerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.ItemOwner
        fields = ('url', 'id', 'name', 'email')

class ItemResponsiblePositionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.ItemResponsiblePosition
        fields = ('url', 'id', 'name')

class ItemHomeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.ItemHome
        fields = ('url', 'id', 'name')

class SupplierSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.Supplier
        fields = ('url', 'id', 'name', 'supplier_url')

class ItemNoteSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.ItemNote
        fields = ('url', 'id', 'text', 'item')

class ItemPictureSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.ItemPicture
        fields = ('url', 'id', 'image')

class QuoteSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.Quote
        fields = ('url', 'id', 'supplier', 'amount', 'date', 'quote_url', 'notes', 'item')

class ItemSerializer(HyperlinkedModelSerializer):
    category = ItemCategorySerializer()
    status = ItemStatusSerializer()
    owner = ItemOwnerSerializer()
    responsible_position = ItemResponsiblePositionSerializer()
    home = ItemHomeSerializer()
    supplier = SupplierSerializer()

    class Meta:
        model = models.Item
        fields = ('url', 'id', 'name', 'details', 'purchase_date', 'purchase_price',
                  'category', 'status', 'owner', 'responsible_position', 'home', 'supplier',
                  'notes', 'pictures', 'quotes')

class FlatItemSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.Item
        fields = ('url', 'id', 'name', 'details', 'purchase_date', 'purchase_price',
                  'category', 'status', 'owner', 'responsible_position', 'home', 'supplier')

