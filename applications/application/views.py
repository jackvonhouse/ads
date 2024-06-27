from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.application.models import Application
from applications.notification.models import Notification
from applications.application.serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        application = self.get_object()
        application.is_accepted = True
        application.save()

        Notification.objects.create(
            user=application.user,
            message=f'Ваша заявка на объявление "{application.ad.title}" была принята'
        )

        return Response({'status': 'Заявка принята'})
