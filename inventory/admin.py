from django.contrib import admin

import reversion

from inventory.models import *

class ItemPictureInline(admin.TabularInline):
    model = ItemPicture
    extra = 1

class ItemNoteInline(admin.TabularInline):
    model = ItemNote
    extra = 0

class QuoteInline(admin.TabularInline):
    model = Quote
    extra = 0

class ItemAdmin(reversion.VersionAdmin):
    inlines = [
            ItemPictureInline,
            ItemNoteInline,
            QuoteInline,
            ]

admin.site.register(Item, ItemAdmin)

admin.site.register(ItemCategory)
admin.site.register(ItemStatus)
admin.site.register(ItemOwner)
admin.site.register(ItemResponsiblePosition)
admin.site.register(ItemHome)
admin.site.register(Supplier)
admin.site.register(ItemNote)
admin.site.register(ItemPicture)
admin.site.register(Quote)


