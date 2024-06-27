from rest_framework import serializers
from applications.application.models import Application
from applications.notification.models import Notification


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

    def create(self, validated_data):
        application = super().create(validated_data)

        Notification.objects.create(
            user=application.ad.user,
            message=f'Новая заявка на Ваше объявление от {application.user.username}',
        )

        return application
