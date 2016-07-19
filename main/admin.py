from django.contrib import admin
from django import forms

from models import *

from django.forms import ModelChoiceField

admin.site.site_header = 'Centennial Admin'
admin.site.site_title = 'Centennial Admin'
admin.site.index_title = 'Home'

#TODO: add functions to admin (through actions bar: pin, unpin, clean ranks, etc.)

class CustomUserChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class CustomUserProfileAdminForm(forms.ModelForm):
    user = CustomUserChoiceField(queryset=User.objects.all())

    class Meta:
        model = UserProfile
        fields = ('user', 'mobile')

class UserProfileAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('get_full_name', 'mobile')

    form = CustomUserProfileAdminForm

    def get_full_name(self, obj):
        return obj
    get_full_name.short_description = 'name'
    get_full_name.admin_order_field = 'user__last_name'

class StudentProfileAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('user_profile', 'student_id', 'grade_level')

class TeacherProfileAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('user_profile', 'room')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_color')

    def display_color(self, obj):
        return '<div style="width: 48px; height:16px; background-color: %s"></div>' % obj.color
    display_color.short_description = 'Color'
    display_color.allow_tags = True

class ImageFileInlineAdmin(admin.TabularInline):
    model = ImageFile
    fields = ('image_file',)

    def get_extra(self, request, obj=None, **kwargs):
        return 0

class ImageLinkInlineAdmin(admin.TabularInline):
    model = ImageLink
    fields = ('image_link',)

    def get_extra(self, request, obj=None, **kwargs):
        return 0

class YouTubeVideoInlineAdmin(admin.TabularInline):
    model = YouTubeVideo
    fields = ('youtube_video',)

    def get_extra(self, request, obj=None, **kwargs):
        return 0

class AnnouncementAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('title', 'author', 'date_created', 'display_category', 'rank')
    inlines = (ImageFileInlineAdmin, ImageLinkInlineAdmin, YouTubeVideoInlineAdmin)

    def display_category(self, obj):
        if obj.category is not None:
            return '<li type="square" style="color:%s"><span style="color:black">%s</span></li>' % (obj.category.color, obj.category.name)
        return 'General'
    display_category.short_description = 'Category'
    display_category.allow_tags = True

class EventAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('name', 'date_start', 'time_start', 'date_end', 'time_end', 'is_multi_day', 'display_category')

    def display_category(self, obj):
        if obj.category is not None:
            return '<li type="square" style="color:%s"><span style="color:black">%s</span></li>' % (obj.category.color, obj.category.name)
        return 'General'
    display_category.short_description = 'Category'
    display_category.allow_tags = True

class ChoiceInlineAdmin(admin.TabularInline):
    model = Choice
    fields = ('content',)

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.choices.count() > 0:
            return 0
        return 4

class PollAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('content', 'date_open', 'is_open', 'date_close', 'display_category', 'rank')
    inlines = (ChoiceInlineAdmin,)

    def display_category(self, obj):
        if obj.category is not None:
            return '<li type="square" style="color:%s"><span style="color:black">%s</span></li>' % (obj.category.color, obj.category.name)
        return 'General'
    display_category.short_description = 'Category'
    display_category.allow_tags = True

class ChoiceAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('content', 'poll', 'vote_count')

class VoteAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('voter', 'choice', 'poll')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(TeacherProfile, TeacherProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(ImageFile)
admin.site.register(ImageLink)
admin.site.register(YouTubeVideo)
