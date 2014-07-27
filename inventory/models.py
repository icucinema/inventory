from django.db import models

# Various item attributes

class ItemCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=254)

    def __unicode__(self):
        return self.name

class ItemStatus(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class ItemOwner(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)

    def __unicode__(self):
        return self.name

class ItemResponsiblePosition(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class ItemHome(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

# Supplier

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=1000, blank=True)

    def __unicode__(self):
        return self.name

# Item

class Item(models.Model):
    name = models.CharField(max_length=254)
    details = models.TextField(blank=True)
    purchase_date = models.DateField(blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(ItemCategory)
    status = models.ForeignKey(ItemStatus)
    owner = models.ForeignKey(ItemOwner)
    reponsible_position = models.ForeignKey(ItemResponsiblePosition)
    home = models.ForeignKey(ItemHome)
    supplier = models.ForeignKey(Supplier)

    def __unicode__(self):
        return u'['+str(self.id)+u'] '+self.name

# Things that can be attached to an item

class ItemNote(models.Model):
    text = models.TextField()
    item = models.ForeignKey(Item)

    def __unicode__(self):
        return u"Note ["+str(self.id)+u"] on Item ["+str(self.item.id)+u"]"

class ItemPicture(models.Model):
    image = models.ImageField(upload_to="inventory_image")    
    item = models.ForeignKey(Item)

    def __unicode__(self):
        return u"Picture ["+str(self.id)+u"] on Item ["+str(self.item.id)+u"]"

# Quote

class Quote(models.Model):
    supplier = models.ForeignKey(Supplier)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateField()
    url = models.URLField(max_length=1000,blank=True)
    notes = models.TextField(blank=True)
    item = models.ForeignKey(Item)

    def __unicode__(self):
        return u"Quote ["+str(self.id)+u"] on Item ["+str(self.item.id)+u"]"


