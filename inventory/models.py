from django.db import models, transaction
from django.conf import settings

import reversion

import os
import uuid

# Various item attributes

class ItemCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=254)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class ItemStatus(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class ItemOwner(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class ItemResponsiblePosition(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class ItemHome(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

# Supplier

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    supplier_url = models.URLField(max_length=1000, blank=True)
    wiki = models.CharField(blank=True, max_length=254)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

# Item

class Item(models.Model):
    name = models.CharField(max_length=254)
    details = models.TextField(blank=True)
    category = models.ForeignKey(ItemCategory)
    owner = models.ForeignKey(ItemOwner)
    responsible_position = models.ForeignKey(ItemResponsiblePosition)
    wiki = models.CharField(blank=True, max_length=254)
  
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'['+str(self.id)+u'] '+self.name

# Instance

class Instance(models.Model):
    comment = models.CharField(max_length=254, blank=True)
    purchase_date = models.DateField(blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    status = models.ForeignKey(ItemStatus)
    home = models.ForeignKey(ItemHome)
    supplier = models.ForeignKey(Supplier)
    item = models.ForeignKey(Item, related_name='instances')

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return u'['+str(self.id)+u'] '+self.comment

# Things that can be attached to an item

class ItemNote(models.Model):
    text = models.TextField()
    item = models.ForeignKey(Item, related_name='notes')
    date_added = models.DateField()

    class Meta:
        ordering = ['-date_added']

    def __unicode__(self):
        return u"Note ["+str(self.id)+u"] on Item ["+str(self.item.id)+u"]"

class ItemPicture(models.Model):
    def picture_file_name(self, filename):
        lowerName = filename.lower()
        if lowerName[-3:] == "png":
            extension = "png"
        elif lowerName[-3:] == "jpg":
            extension = "jpg"
        elif lowerName[-4:] == "jpeg":
            extension = "jpg"

        return "inventory"+os.sep+"item_pictures"+os.sep+str(uuid.uuid4())+"."+extension

    image = models.ImageField(upload_to=picture_file_name)
    item = models.ForeignKey(Item, related_name='pictures')

    def __unicode__(self):
        return u"Picture ["+str(self.id)+u"] on Item ["+str(self.item.id)+u"]"

# Quote

class Quote(models.Model):
    supplier = models.ForeignKey(Supplier)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateField()
    quote_url = models.URLField(max_length=1000,blank=True)
    notes = models.TextField(blank=True)
    item = models.ForeignKey(Item, related_name='quotes')

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return u"Quote ["+str(self.id)+u"] on Item ["+str(self.item.id)+u"]"

