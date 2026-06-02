from store.models import Category, Plant, Article, Order, OrderItem, Tag
import decimal
import random
from django.utils import timezone

tag_names = ['Для новичков', 'Тенелюбивое', 'Редкое', 'Быстрорастущее', 'Очищает воздух', 'Цветущее', 'Лекарственное']
tags = []
for name in tag_names:
    t, _ = Tag.objects.get_or_create(name=name)
    tags.append(t)

categories_names = [
    ('Комнатные растения', 'indoor-plants'), ('Суккуленты', 'succulents'), 
    ('Для офиса', 'office-plants'), ('Кактусы', 'cactus'), ('Бонсай', 'bonsai')
]
cats = []
for name, slug in categories_names:
    c, _ = Category.objects.update_or_create(slug=slug, defaults={'name': name})
    cats.append(c)

plant_translations = [
    ('Фикус Лирата', 'ficus-lyrata'), ('Монстера Делициоза', 'monstera-deliciosa'), 
    ('Алоэ Вера', 'aloe-vera'), ('Сансевиерия', 'snake-plant'), 
    ('Замиокулькас', 'zz-plant'), ('Эхеверия', 'echeveria'), 
    ('Крассула', 'jade-plant'), ('Спатифиллум', 'peace-lily'), 
    ('Хлорофитум', 'spider-plant'), ('Нефролепис', 'boston-fern'), 
    ('Фикус Эластика', 'rubber-plant'), ('Плющ обыкновенный', 'english-ivy'), 
    ('Орхидея Фаленопсис', 'orchid'), ('Бамбук счастья', 'bamboo'), 
    ('Лаванда', 'lavender')
]

for name, slug in plant_translations:
    p, _ = Plant.objects.update_or_create(
        slug=slug,
        defaults={
            'name': name,
            'category': random.choice(cats),
            'price': decimal.Decimal(random.randint(500, 5000)),
            'is_in_stock': True,
            'description': f'Прекрасное растение {name} для вашего дома.',
            'image': f'plants/{slug}.webp'
        }
    )
    p.tags.set(random.sample(tags, random.randint(2, 3)))

for i in range(1, 11):
    art, _ = Article.objects.update_or_create(
        slug=f'article-{i}',
        defaults={
            'title': f'Как ухаживать за растениями, часть {i}',
            'content': f'<p>Подробное руководство номер {i}.</p>',
            'author': 'Мастер Садовод',
            'is_active': True
        }
    )
    art.tags.set(random.sample(tags, random.randint(1, 2)))

print(f"БД обновлена: {Tag.objects.count()} тегов создано и привязано к {Plant.objects.count()} растениям.")
