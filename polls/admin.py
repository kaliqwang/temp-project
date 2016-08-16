from django.contrib import admin

from .models import *

class ChoiceInlineAdmin(admin.TabularInline):
    model = Choice
    fields = ('content',)

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.choices.count() > 0:
            return 0
        return 4

class PollAdmin(admin.ModelAdmin):
    # list_select_related = True
    list_display = ('content', 'date_open', 'is_open', 'date_close', 'display_category', 'rank')
    inlines = (ChoiceInlineAdmin,)
    save_as = True
    view_on_site = True

    def display_category(self, obj):
        if obj.category is not None:
            return '<li type="square" style="color:%s"><span style="color:black">%s</span></li>' % (obj.category.color, obj.category.name)
        return 'General'
    display_category.short_description = 'Category'
    display_category.allow_tags = True
    display_category.admin_order_field = 'category__name'

class ChoiceAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('content', 'poll', 'vote_count')

class VoteAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('voter', 'choice', 'poll')

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Vote, VoteAdmin)
