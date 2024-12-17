from django.db import models

class Scene(models.Model):
    scene_name = models.CharField(max_length=255)
    scene_size_kb = models.FloatField()
    timestamp = models.FloatField()  # Timestamp stored as an integer
    image = models.CharField(max_length=255)

    def __str__(self):
        return self.scene_name

class Geometry(models.Model):
    scene = models.ForeignKey(Scene, related_name="geometries", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    is_visible = models.BooleanField(null=True, blank=True)
    vertex_count = models.IntegerField(null=True, blank=True)
    uv_channel_count = models.IntegerField(null=True, blank=True)
    child_count = models.IntegerField(null=True, blank=True)
    layer_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
