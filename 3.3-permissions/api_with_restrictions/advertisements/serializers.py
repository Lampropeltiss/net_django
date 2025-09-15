from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        method = self.context["request"].method
        current_creator = self.context["request"].user
        current_status = data.get("status", "OPEN")
        open_posts_limit = 10

        if method == "POST":
            adv_amount = Advertisement.objects.filter(creator=current_creator).filter(status='OPEN').count()
            if adv_amount >= open_posts_limit and current_status == "OPEN":
                raise ValidationError("You have reached the limit of opened posts. "
                                      "Try to create a draft post instead.")

        return data
