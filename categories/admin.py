from django.contrib import admin

from models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_color')

    def display_color(self, obj):
        return '<div style="width: 48px; height:16px; background-color: %s"></div>' % obj.color
    display_color.short_description = 'Color'
    display_color.allow_tags = True
    display_color.admin_order_field = 'color'

admin.site.register(Category, CategoryAdmin)
