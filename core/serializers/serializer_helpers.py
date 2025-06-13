def make_user_active(validated_data, instance):
    instanceUser = instance.objects.create(**validated_data)

    instanceUser.user.is_active = True

    instanceUser.user.save()

    return instanceUser