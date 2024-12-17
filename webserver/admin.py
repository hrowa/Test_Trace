# Register your models here.

from django.contrib import admin
from django.utils.html import format_html
from .models import Scene, Geometry


class GeometryInline(admin.TabularInline):
    model = Geometry
    extra = 0
    fields = ["name", "is_visible", "vertex_count", "uv_channel_count", "child_count", "layer_name"]
    readonly_fields = ["name", "is_visible", "vertex_count", "uv_channel_count", "child_count", "layer_name"]


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    readonly_fields = ["scene_name", "scene_size_kb", "timestamp", "image"]
    inlines = [GeometryInline]
    search_fields = ["scene_name"]  # поиск по имени сцены
    list_filter = ["scene_size_kb", "timestamp"]

    list_display = ["scene_name","infographic_button"]

    def infographic_button(self, obj):

        url = f"/scenes/{obj.id}/dashboard/"
        return format_html('<a class="button" href="{}">Инфографика</a>', url)