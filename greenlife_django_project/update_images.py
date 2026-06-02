from store.models import Plant, Article
import os

plants = Plant.objects.all()
images = [
    'plants/2026/03/19/1.jpg',
    'plants/2026/03/19/2.jpg',
    'plants/2026/03/19/3.jpg',
    'plants/2026/03/19/4.jpg',
    'plants/2026/03/19/5.jpg',
    'plants/2026/03/19/6.png',
]

for i, plant in enumerate(plants):
    if i < len(images):
        plant.image = images[i]
        plant.save()

article = Article.objects.first()
if article:
    article.image = 'articles/2026/03/19/7.png'
    article.save()

print(f"Updated {plants.count()} plants and 1 article with images.")
