from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices, FavoriteAds
from api_with_restrictions import settings


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
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # Проверяем, что у пользователя не больше 10 открытых объявлений
        opened_count = Advertisement.objects.filter(
            creator_id=self.context["request"].user.id,
            status=AdvertisementStatusChoices.OPEN
        ).count()
        if opened_count > settings.MAX_OPENED_ADVERTISEMENTS_COUNT:
            raise serializers.ValidationError("The number of open advertisements has been exceeded")

        return data


class FavoriteAdsSerializer(serializers.ModelSerializer):
    """Serializer для избранных объявлений."""

    user = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = FavoriteAds
        fields = ('id', 'user', 'ad',)

    def create(self, validated_data):
        """Метод для создания"""

        create_res = FavoriteAds.objects.update_or_create(
            user=self.context["request"].user,
            ad=validated_data["ad"]
        )
        return create_res[0]

    def validate_ad(self, ad):
        """
        Метод для валидации объявления
        """

        if ad.creator == self.context["request"].user:
            raise serializers.ValidationError("You cannot add your ad to favorites")
        return ad
