from django.contrib.auth.models import User
from store.models import Plant, Order, OrderItem, Category
import random
import decimal

users = []
for i in range(1, 11):
    username = f'user_{i}'
    email = f'random_{random.randint(1000, 9999)}@example.com'
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, email=email, password='test')
        users.append(user)
    else:
        users.append(User.objects.get(username=username))

plants = list(Plant.objects.all())
if not plants:
    print("Ошибка: В БД нет растений. Сначала запустите seed_db.py")
else:
    for user in users:
        for j in range(random.randint(1, 3)):
            order = Order.objects.create(
                customer_name=user.username,
                customer_email=user.email,
                address=f'Улица {random.randint(1, 100)}, д. {random.randint(1, 50)}',
                city=random.choice(['Москва', 'Санкт-Петербург', 'Казань', 'Екатеринбург']),
                status=random.choice(['P', 'PR', 'S', 'D']),
                phone=f'+7999{random.randint(1000000, 9999999)}'
            )
            order_plants = random.sample(plants, random.randint(1, min(4, len(plants))))
            for p in order_plants:
                OrderItem.objects.create(
                    order=order,
                    plant=p,
                    price=p.price,
                    quantity=random.randint(1, 3)
                )
    print(f"Успешно создано 10 пользователей и заказы для них. Пароль: test")
