from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SceneSerializer

from django.shortcuts import render, get_object_or_404
from .models import Scene, Geometry


def dashboard(request, scene_id):
    scene = get_object_or_404(Scene, pk=scene_id)

    scene_objects = scene.scene_name
    geometry_objects = scene.geometries.all()

    scene_name = scene_objects
    labels = [geometry.name for geometry in geometry_objects]
    vertex_counts = [geometry.vertex_count if geometry.vertex_count is not None else "" for geometry in geometry_objects]
    child_counts = [geometry.child_count if geometry.child_count is not None else "" for geometry in geometry_objects]
    uv_channel_counts = [geometry.uv_channel_count if geometry.uv_channel_count is not None else "" for geometry in geometry_objects]

    context = {
        "scene_name": scene_name,
        "labels": labels,
        "vertex_counts": vertex_counts,
        "child_counts": child_counts,
        "uv_channel_counts": uv_channel_counts,
    }

    return render(request, "dashboard.html", context)

class SaveSceneDataView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SceneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Data saved successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

