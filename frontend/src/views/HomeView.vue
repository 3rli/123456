<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import PlantCard from '../components/PlantCard.vue'
import type { Plant } from '../stores/cart'
import { Search, Loader2, BarChart3, Star, Newspaper, ArrowRight } from 'lucide-vue-next'

interface Category { id: number; name: string; slug: string }
interface ShopStats { 
  stats: { total_plants: number; avg_price: number; total_stock_value: number };
  popular: Plant[];
  authors: string[];
  active_articles: number;
}

const plants = ref<Plant[]>([])
const categories = ref<Category[]>([])
const shopStats = ref<ShopStats | null>(null)
const loading = ref(true)
const selectedCategory = ref('')
const searchQuery = ref('')

const fetchData = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (selectedCategory.value) params.category = selectedCategory.value
    if (searchQuery.value) params.q = searchQuery.value
    
    const [plantsRes, catsRes, statsRes] = await Promise.all([
      axios.get('http://localhost:8000/api/plants/', { params }),
      axios.get('http://localhost:8000/api/categories/'),
      axios.get('http://localhost:8000/api/shop-stats/')
    ])
    
    plants.value = plantsRes.data
    categories.value = catsRes.data
    shopStats.value = statsRes.data
  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)

const handleCategoryChange = (slug: string) => {
  selectedCategory.value = slug
  fetchData()
}

const handleSearch = () => {
  fetchData()
}
</script>

<template>
  <div class="home-view">
    <div class="hero">
      <h1>Привнесите природу в свой дом</h1>
      <p>Откройте для себя широкий выбор растений, чтобы превратить ваше жилое пространство в зеленый оазис.</p>
    </div>
    <div v-if="shopStats" class="widgets-grid">
      <div class="widget-card stats-widget">
        <div class="widget-header">
          <BarChart3 :size="20" />
          <h3>Статистика магазина</h3>
        </div>
        <div class="stats-list">
          <div class="stat-item">
            <span class="label">Всего растений:</span>
            <span class="value">{{ shopStats.stats.total_plants }}</span>
          </div>
          <div class="stat-item">
            <span class="label">Средняя цена:</span>
            <span class="value">{{ shopStats.stats.avg_price?.toFixed(0) }} ₽</span>
          </div>
          <div class="stat-item">
            <span class="label">Общая стоимость:</span>
            <span class="value">{{ shopStats.stats.total_stock_value?.toFixed(0) }} ₽</span>
          </div>
        </div>
        <RouterLink to="/stats" class="widget-link">Подробная статистика <ArrowRight :size="14" /></RouterLink>
      </div>

      <div class="widget-card popular-widget">
        <div class="widget-header">
          <Star :size="20" />
          <h3>Самые популярные</h3>
        </div>
        <ol class="popular-list">
          <li v-for="plant in shopStats.popular" :key="plant.id">
            <RouterLink :to="{ name: 'plant-detail', params: { id: plant.id, slug: plant.slug } }">
              {{ plant.name }} — {{ plant.price }} ₽
            </RouterLink>
          </li>
        </ol>
      </div>

      <div class="widget-card journal-widget">
        <div class="widget-header">
          <Newspaper :size="20" />
          <h3>Журнал GreenLife</h3>
        </div>
        <div class="journal-info">
          <p>У нас есть <strong>{{ shopStats.active_articles }}</strong> активных руководств по уходу.</p>
          <p class="authors-list">Авторы: {{ shopStats.authors.join(', ') }}</p>
        </div>
        <RouterLink to="/articles" class="widget-link">Читать журнал <ArrowRight :size="14" /></RouterLink>
      </div>
    </div>

    <div class="controls">
      <div class="categories-filter">
        <button :class="['filter-btn', { active: selectedCategory === '' }]" @click="handleCategoryChange('')">Все</button>
        <button v-for="cat in categories" :key="cat.id" :class="['filter-btn', { active: selectedCategory === cat.slug }]" @click="handleCategoryChange(cat.slug)">{{ cat.name }}</button>
      </div>

      <div class="search-box">
        <input v-model="searchQuery" type="text" placeholder="Поиск растений..." @keyup.enter="handleSearch" />
        <button @click="handleSearch" class="search-btn"><Search :size="20" /></button>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <Loader2 class="spinner" :size="48" />
      <p>Загрузка каталога...</p>
    </div>

    <div v-else-if="plants.length === 0" class="empty-state">
      <p>Растения не найдены. Попробуйте другой запрос или категорию.</p>
    </div>

    <div v-else class="plants-grid">
      <PlantCard v-for="plant in plants" :key="plant.id" :plant="plant" />
    </div>
  </div>
</template>

<style scoped src="./HomeView.css"></style>
