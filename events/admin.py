from django.contrib import admin

from models import *

class EventAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('name', 'date_start', 'time_start', 'date_end', 'time_end', 'is_multi_day', 'display_category')
    save_as = True
    view_on_site = True

    def display_category(self, obj):
        if obj.category is not None:
            return '<li type="square" style="color:%s"><span style="color:black">%s</span></li>' % (obj.category.color, obj.category.name)
        return 'General'
    display_category.short_description = 'Category'
    display_category.allow_tags = True
    display_category.admin_order_field = 'category__name'

admin.site.register(Event, EventAdmin)
