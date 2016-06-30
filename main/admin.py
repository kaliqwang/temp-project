from django.contrib import admin
from django import forms

from models import *

from django.forms import ModelChoiceField

admin.site.site_header = 'Centennial Admin'
admin.site.site_title = 'Centennial Admin'
admin.site.index_title = 'Home'

class CustomUserChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

class CustomStudentProfileAdminForm(forms.ModelForm):
    user = CustomUserChoiceField(queryset=User.objects.all())

    class Meta:
        model = StudentProfile
        fields = ('user', 'student_id', 'grade_level', 'schedule')

class CategoryAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('name', 'display_color')

class ClassAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('subject', 'teacher', 'room', 'period', 'is_honors', 'is_ap', 'is_dual')

class StudentProfileAdmin(admin.ModelAdmin):
    def get_full_name(self, obj):
        return obj
    get_full_name.short_description = 'name'
    get_full_name.admin_order_field = 'user__first_name'

    form = CustomStudentProfileAdminForm
    fieldsets = (
        ('Details', {'fields': ('user', 'student_id', 'grade_level', 'schedule')}),
    )
    list_select_related = True
    list_display = ('get_full_name', 'student_id', 'grade_level')

class TeacherProfileAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('user', 'room')

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

class YoutubeVideoInlineAdmin(admin.TabularInline):
    model = YoutubeVideo
    fields = ('youtube_video',)

    def get_extra(self, request, obj=None, **kwargs):
        return 0

class AnnouncementAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('title', 'category', 'author', 'date_created', 'rank')
    inlines = (ImageFileInlineAdmin, ImageLinkInlineAdmin, YoutubeVideoInlineAdmin)

class EventAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('name', 'category', 'location', 'date_start', 'time_start', 'date_end', 'time_end')

class ChoiceInlineAdmin(admin.TabularInline):
    model = Choice
    fields = ('content',)
    extra = 4

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.choices.count() > 0:
            return 0
        return self.extra

class PollAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Details', {'fields': ('content', 'category', 'author', 'rank', 'is_open')}),
    )
    list_select_related = True
    list_display = ('content', 'display_category', 'author', 'date_created', 'rank', 'is_open')
    inlines = (ChoiceInlineAdmin,)

class ChoiceAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('poll', 'content')
    # Also display the chosen_by count

#add functions to admin (through actions bar: pin, unpin, clean ranks, etc.)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subject)
admin.site.register(Class, ClassAdmin)
admin.site.register(Schedule)
admin.site.register(ImageFile)
admin.site.register(ImageLink)
admin.site.register(YoutubeVideo)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(TeacherProfile, TeacherProfileAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)
