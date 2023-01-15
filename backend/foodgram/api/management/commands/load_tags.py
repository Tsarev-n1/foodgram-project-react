from django.core.management import BaseCommand

from ...models import Tag


class Command(BaseCommand):
    help = 'Создаем теги'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'hex_code': '#E26C2D', 'slug': 'breakfast'},
            {'name': 'Обед', 'hex_code': '#49B64E', 'slug': 'lunch'},
            {'name': 'Ужин', 'hex_code': '#8775D2', 'slug': 'dinner'}]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        self.stdout.write(self.style.SUCCESS('Все теги загружены!'))
