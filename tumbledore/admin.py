from django.contrib import admin

from tumbledore.models import *


class TumblelogPostInline(admin.StackedInline):
    model = TumblelogPost


class TumblelogWidgetPlacementInline(admin.TabularInline):
    model = TumblelogWidgetPlacement


class TumblelogAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'mount_on', 'theme', 'created_at')
    list_filter = ('theme',)
    list_editable = ('theme',)
    date_hierarchy = 'created_at'
    inlines = (TumblelogWidgetPlacementInline, TumblelogPostInline)
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': ('name', 'mount_on', 'theme', 'posts_per_page')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('description', 'extra_styles', 'extra_scripts')
        }),
    )
admin.site.register(Tumblelog, TumblelogAdmin)


class TumblelogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'tumblelog', 'is_published', 'is_sticky', 'created_at', 'published_at')
    list_filter = ('author', 'tumblelog', 'is_published', 'is_sticky')
    list_editable = ('is_published', 'is_sticky')
    date_hierarchy = 'published_at'
    prepopulated_fields = {"slug": ("title",)}
    save_on_top = True
admin.site.register(TumblelogPost, TumblelogPostAdmin)


class TumblelogWidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    date_hierarchy = 'created_at'
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
admin.site.register(TumblelogWidget, TumblelogWidgetAdmin)


class TumblelogWidgetPlacementAdmin(admin.ModelAdmin):
    list_display = ('widget', 'tumblelog', 'order')
    list_editable = ('order',)
admin.site.register(TumblelogWidgetPlacement, TumblelogWidgetPlacementAdmin)