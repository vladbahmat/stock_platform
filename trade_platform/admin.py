from django.contrib import admin

from trade_platform.models import Profile, Currency, Trade, Item, Offer, WatchList, Inventory


class ItemAdmin(admin.ModelAdmin):
    search_fields = ('code',)
    list_editable = ['currency', 'description']
    list_display = ['code', 'name', 'currency', 'description']
    list_filter = ['currency']
    ordering = ['code']
    radio_fields = {'currency': admin.HORIZONTAL}


class WatchListAdmin(admin.ModelAdmin):
    search_fields = ('person__user__username__exact',)
    list_display = ['person', 'items', ]
    list_filter = ['item', 'person']
    ordering = ['person__user__username']
    readonly_fields = ('person',)

    def items(self, obj):
        return "\n".join([p.code for p in obj.item.all()])


myModels = [Profile, Currency, Trade, Offer, Inventory]
admin.site.register(myModels)
admin.site.register(WatchList, WatchListAdmin)
admin.site.register(Item, ItemAdmin)
