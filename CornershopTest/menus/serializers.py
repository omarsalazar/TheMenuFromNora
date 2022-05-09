from rest_framework import serializers
from django.db import transaction

from CornershopTest.menus.models import Menu, Options


class OptionsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = ("id", "name", "content")
        read_only_fields = ("id",)


class MenuModelSerializer(serializers.ModelSerializer):
    options = OptionsModelSerializer(many=True)

    class Meta:
        fields = ("options", "date", "id")
        model = Menu


class CreateMenuModelSerializer(serializers.ModelSerializer):
    options = serializers.ListField(write_only=True, required=False)
    dishes = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ("date", "options", "dishes")

    def get_dishes(self, obj):
        return OptionsModelSerializer(instance=obj.options.all(), many=True).data

    def create(self, validated_data):
        with transaction.atomic():
            options = validated_data.pop("options")
            menu = super().create(validated_data)
            options_obj = Options.objects.filter(id__in=options)
            for option in options_obj:
                menu.options.add(option)
                menu.save()
            return menu

    def update(self, instance, validated_data):
        with transaction.atomic():
            try:
                instance.options.clear()
                options = validated_data.pop("options")
                options_obj = Options.objects.filter(id__in=options)
                for option in options_obj:
                    instance.options.add(option)
                    instance.save()
                return instance
            except Exception as e:
                raise e
