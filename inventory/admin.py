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

class ItemCategoryAdmin(reversion.VersionAdmin):
    pass

class ItemStatusAdmin(reversion.VersionAdmin):
    pass

class ItemOwnerAdmin(reversion.VersionAdmin):
    pass

class ItemResponsiblePositionAdmin(reversion.VersionAdmin):
    pass

class ItemHomeAdmin(reversion.VersionAdmin):
    pass

class SupplierAdmin(reversion.VersionAdmin):
    pass

class ItemNoteAdmin(reversion.VersionAdmin):
    pass

class ItemPictureAdmin(reversion.VersionAdmin):
    pass

class QuoteAdmin(reversion.VersionAdmin):
    pass


admin.site.register(Item, ItemAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(ItemStatus, ItemStatusAdmin)
admin.site.register(ItemOwner, ItemOwnerAdmin)
admin.site.register(ItemResponsiblePosition, ItemResponsiblePositionAdmin)
admin.site.register(ItemHome, ItemHomeAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(ItemNote, ItemNoteAdmin)
admin.site.register(ItemPicture, ItemPictureAdmin)
admin.site.register(Quote, QuoteAdmin)

