from django.contrib import admin

from models import *
from imagekit.admin import AdminThumbnail

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
    list_display = ('title', 'author', 'date_created', 'display_category', 'rank')
    inlines = (ImageFileInlineAdmin, ImageLinkInlineAdmin, YouTubeVideoInlineAdmin)
    save_as = True
    view_on_site = True

    def display_category(self, obj):
        if obj.category is not None:
            return '<li type="square" style="color:%s"><span style="color:black">%s</span></li>' % (obj.category.color, obj.category.name)
        return 'General'
    display_category.short_description = 'Category'
    display_category.allow_tags = True

class ImageFileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'admin_thumbnail', 'announcement')
    admin_thumbnail = AdminThumbnail(image_field='image_file_thumbnail')

class ImageLinkAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'admin_thumbnail', 'announcement')
    admin_thumbnail = AdminThumbnail(image_field='image_file_thumbnail')

class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'announcement')


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(ImageFile, ImageFileAdmin)
admin.site.register(ImageLink, ImageLinkAdmin)
admin.site.register(YouTubeVideo, YouTubeVideoAdmin)
