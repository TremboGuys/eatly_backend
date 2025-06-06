def make_user_active(validated_data, instance):
    user = instance.objects.create(**validated_data)

    user.user.role_register = 1

    user.save()

    return user