<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { ShoppingCart, ArrowLeft, Loader2, Star, CheckCircle } from 'lucide-vue-next'
import { useCartStore, type Plant } from '../stores/cart'

const route = useRoute()
const cartStore = useCartStore()
const plant = ref<Plant | null>(null)
const loading = ref(true)

const fetchPlant = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/plants/${route.params.id}/`)
    plant.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке растения:', error)
  } finally {
    loading.value = false
  }
}

const stripHtml = (html: string) => {
  const tmp = document.createElement("DIV");
  tmp.innerHTML = html;
  return tmp.textContent || tmp.innerText || "";
}

onMounted(fetchPlant)
</script>

<template>
  <div class="plant-detail">
    <button @click="$router.back()" class="back-link">
      <ArrowLeft :size="20" /> Назад в магазин
    </button>

    <div v-if="loading" class="loading-state">
      <Loader2 class="spinner" :size="48" />
    </div>

    <div v-else-if="!plant" class="error-state">
      <p>Растение не найдено.</p>
    </div>

    <div v-else>
      <div class="main-info">
        <div class="image-gallery">
          <img :src="plant.image || 'https://via.placeholder.com/600x600?text=Нет+картинки'" :alt="plant.name" class="main-image" />
        </div>

        <div class="details">
          <span class="category-badge">{{ plant.category?.name || 'Растения' }}</span>
          <h1 class="plant-name">{{ plant.name }}</h1>
          
          <div v-if="plant.tags && plant.tags.length > 0" class="tags-container">
            <span v-for="tag in plant.tags" :key="tag.id" class="tag-badge">#{{ tag.name }}</span>
          </div>

          <div class="rating">
            <div class="stars">
              <Star v-for="i in 5" :key="i" :size="16" fill="#fbbf24" color="#fbbf24" />
            </div>
            <span class="reviews">(42 отзыва)</span>
          </div>

          <div class="price-section">
            <span class="price">{{ plant.price }} ₽</span>
            <span v-if="plant.is_in_stock" class="stock-status in-stock">
              <CheckCircle :size="16" /> В наличии
            </span>
          </div>

          <p class="description">{{ plant.description || 'Описание этого растения скоро появится.' }}</p>

          <button @click="cartStore.addToCart(plant!)" class="add-to-cart-btn">
            <ShoppingCart :size="20" /> Добавить в корзину
          </button>

          <div class="features">
            <div class="feature">
              <strong>Свет:</strong> Непрямой солнечный свет
            </div>
            <div class="feature">
              <strong>Полив:</strong> Раз в неделю
            </div>
            <div class="feature">
              <strong>Сложность:</strong> Для новичков
            </div>
          </div>
        </div>
      </div>

      <section v-if="plant.articles && plant.articles.length > 0" class="articles-section">
        <h2>Статьи об этом растении</h2>
        <div class="articles-grid">
          <div v-for="article in plant.articles" :key="article.id" class="article-card">
            <h3>{{ article.title }}</h3>
            <p>{{ stripHtml(article.content).substring(0, 100) }}...</p>
            <RouterLink :to="{ name: 'article-detail', params: { id: article.id, slug: article.slug } }" class="read-more">
              Читать далее
            </RouterLink>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped src="./PlantDetailView.css"></style>
