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
        fields = ('url', 'id', 'name', 'supplier_url', 'wiki')

class ItemNoteSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.ItemNote
        fields = ('url', 'id', 'text', 'item', 'date_added')

class ItemPictureSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.ItemPicture
        fields = ('url', 'id', 'image')

class QuoteSerializer(HyperlinkedModelSerializer):
    supplier = SupplierSerializer()

    class Meta:
        model = models.Quote
        fields = ('url', 'id', 'supplier', 'amount', 'date', 'quote_url', 'notes', 'item')

class FlatQuoteSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.Quote
        fields = ('url', 'id', 'supplier', 'amount', 'date', 'quote_url', 'notes', 'item')

class InstanceSerializer(HyperlinkedModelSerializer):
    supplier = SupplierSerializer()
    status = ItemStatusSerializer()
    home = ItemHomeSerializer()

    class Meta:
        model = models.Instance
        fields = ('url', 'id', 'comment', 'purchase_date', 'purchase_price', 'supplier', 'status',
                  'home', 'item')

class FlatInstanceSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.Instance
        fields = ('url', 'id', 'comment', 'purchase_date', 'purchase_price', 'supplier', 'status',
                  'home', 'item')

class ItemSerializer(HyperlinkedModelSerializer):
    category = ItemCategorySerializer()
    owner = ItemOwnerSerializer()
    responsible_position = ItemResponsiblePositionSerializer()

    class Meta:
        model = models.Item
        fields = ('url', 'id', 'name', 'details', 'category', 'owner', 'responsible_position',
                  'notes', 'pictures', 'quotes', 'instances', 'wiki')

class FlatItemSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.Item
        fields = ('url', 'id', 'name', 'details', 'category', 'owner', 'responsible_position',
                  'notes', 'pictures', 'quotes', 'instances', 'wiki')


