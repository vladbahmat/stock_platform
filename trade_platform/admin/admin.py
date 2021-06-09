from django.contrib import admin

from trade_platform.models import Profile, Currency, Trade, Item, Offer, WatchList, Inventory, WorkShift, Position, \
    WorkShiftPlan, Location, UserConfig
from trade_platform.admin.admin_methods import change_workshifts_relation

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
    autocomplete_fields = ['item',]

    def items(self, obj):
        return "\n".join([p.code for p in obj.item.all()])



change_workshifts_relation.short_description = "Mark selected stories as published"

class WorkShiftPlanAdmin(admin.ModelAdmin):
    actions = [change_workshifts_relation]

trade_platform_models = (Profile, Currency, Trade, Offer, Inventory, WorkShift, Position, Location,
                         UserConfig)
admin.site.register(trade_platform_models)
admin.site.register(WorkShiftPlan, WorkShiftPlanAdmin)
admin.site.register(WatchList, WatchListAdmin)
admin.site.register(Item, ItemAdmin)
