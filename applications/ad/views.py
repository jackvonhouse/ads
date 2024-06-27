from rest_framework import viewsets, permissions
from applications.ad.models import Ad
from applications.ad.serializers import AdSerializer
from applications.permissions import IsOwnerOrReadOnly


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
