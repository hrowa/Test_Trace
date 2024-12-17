from rest_framework import serializers
from .models import Scene, Geometry


class GeometrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Geometry
        fields = ["name", "is_visible", "vertex_count", "uv_channel_count", "child_count", "layer_name"]


class SceneSerializer(serializers.ModelSerializer):
    geometry = serializers.JSONField(write_only=True)

    class Meta:
        model = Scene
        fields = ["scene_name", "scene_size_kb", "timestamp", "image", "geometry"]

    def create(self, validated_data):
        geometry_data = validated_data.pop("geometry", {})
        scene = Scene.objects.create(**validated_data)
        for key, geom in geometry_data.items():
            Geometry.objects.create(scene=scene, **geom)

        return scene
