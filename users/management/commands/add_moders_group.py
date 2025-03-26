# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from users.models import CustomUser


class Command(BaseCommand):
    help = "Команда для создания группы модераторов"

    def handle(self, *args, **options):

        group, created = Group.objects.get_or_create(name="moders")
        if created:
            self.stdout.write(self.style.SUCCESS(f"Создана группа: {group.name}"))
        else:
            self.stdout.write(self.style.WARNING(f"Группа {group.name} уже существует"))

        moderator = CustomUser.objects.get(email="moderator@mail.com")

        moderator.groups.add(group)
        self.stdout.write(
            self.style.SUCCESS(
                f'Пользователь "{moderator.email}" добавлен в группу "{group.name}".'
            )
        )
