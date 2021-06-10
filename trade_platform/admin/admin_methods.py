from trade_platform.models import  WorkShift


def change_workshifts_relation(modeladmin, request, queryset):
    plan_ids = queryset.values_list('id', flat=True)
    WorkShift.objects.filter(workshit_plan__id__in=plan_ids).update(workshit_plan=None)
    # for object in queryset:
    #     object.workshifts.clear()
    #     object.save()
    #print(queryset.update(workshifts=None)v