# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ItemCategory'
        db.create_table(u'inventory_itemcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=254)),
        ))
        db.send_create_signal(u'inventory', ['ItemCategory'])

        # Adding model 'ItemStatus'
        db.create_table(u'inventory_itemstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'inventory', ['ItemStatus'])

        # Adding model 'ItemOwner'
        db.create_table(u'inventory_itemowner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
        ))
        db.send_create_signal(u'inventory', ['ItemOwner'])

        # Adding model 'ItemResponsiblePosition'
        db.create_table(u'inventory_itemresponsibleposition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'inventory', ['ItemResponsiblePosition'])

        # Adding model 'ItemHome'
        db.create_table(u'inventory_itemhome', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'inventory', ['ItemHome'])

        # Adding model 'Supplier'
        db.create_table(u'inventory_supplier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=1000, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Supplier'])

        # Adding model 'Item'
        db.create_table(u'inventory_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('purchase_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('purchase_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=14, decimal_places=2, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.ItemCategory'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.ItemStatus'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.ItemOwner'])),
            ('reponsible_position', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.ItemResponsiblePosition'])),
            ('home', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.ItemHome'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Supplier'])),
        ))
        db.send_create_signal(u'inventory', ['Item'])

        # Adding model 'ItemNote'
        db.create_table(u'inventory_itemnote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'])),
        ))
        db.send_create_signal(u'inventory', ['ItemNote'])

        # Adding model 'ItemPicture'
        db.create_table(u'inventory_itempicture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'])),
        ))
        db.send_create_signal(u'inventory', ['ItemPicture'])

        # Adding model 'Quote'
        db.create_table(u'inventory_quote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Supplier'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=2)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=1000, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'])),
        ))
        db.send_create_signal(u'inventory', ['Quote'])


    def backwards(self, orm):
        # Deleting model 'ItemCategory'
        db.delete_table(u'inventory_itemcategory')

        # Deleting model 'ItemStatus'
        db.delete_table(u'inventory_itemstatus')

        # Deleting model 'ItemOwner'
        db.delete_table(u'inventory_itemowner')

        # Deleting model 'ItemResponsiblePosition'
        db.delete_table(u'inventory_itemresponsibleposition')

        # Deleting model 'ItemHome'
        db.delete_table(u'inventory_itemhome')

        # Deleting model 'Supplier'
        db.delete_table(u'inventory_supplier')

        # Deleting model 'Item'
        db.delete_table(u'inventory_item')

        # Deleting model 'ItemNote'
        db.delete_table(u'inventory_itemnote')

        # Deleting model 'ItemPicture'
        db.delete_table(u'inventory_itempicture')

        # Deleting model 'Quote'
        db.delete_table(u'inventory_quote')


    models = {
        u'inventory.item': {
            'Meta': {'object_name': 'Item'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.ItemCategory']"}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'home': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.ItemHome']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.ItemOwner']"}),
            'purchase_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'purchase_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '14', 'decimal_places': '2', 'blank': 'True'}),
            'reponsible_position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.ItemResponsiblePosition']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.ItemStatus']"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Supplier']"})
        },
        u'inventory.itemcategory': {
            'Meta': {'object_name': 'ItemCategory'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'inventory.itemhome': {
            'Meta': {'object_name': 'ItemHome'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'inventory.itemnote': {
            'Meta': {'object_name': 'ItemNote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'inventory.itemowner': {
            'Meta': {'object_name': 'ItemOwner'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'inventory.itempicture': {
            'Meta': {'object_name': 'ItemPicture'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"})
        },
        u'inventory.itemresponsibleposition': {
            'Meta': {'object_name': 'ItemResponsiblePosition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'inventory.itemstatus': {
            'Meta': {'object_name': 'ItemStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'inventory.quote': {
            'Meta': {'object_name': 'Quote'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Supplier']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000', 'blank': 'True'})
        },
        u'inventory.supplier': {
            'Meta': {'object_name': 'Supplier'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000', 'blank': 'True'})
        }
    }

    complete_apps = ['inventory']