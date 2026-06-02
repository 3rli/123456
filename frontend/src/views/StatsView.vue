<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { BarChart3, TrendingUp, Tag, Loader2, ArrowLeft } from 'lucide-vue-next'

interface ShopStats { 
  stats: { total_plants: number; avg_price: number; total_stock_value: number };
  popular: any[];
  revenue: { name: string; revenue: number }[];
  categories: { name: string; num_plants: number }[];
  authors: string[];
  active_articles: number;
}

const shopStats = ref<ShopStats | null>(null)
const loading = ref(true)

const fetchStats = async () => {
  loading.value = true
  try {
    const response = await axios.get('http://localhost:8000/api/shop-stats/')
    shopStats.value = response.data
  } catch (error) {
    console.error('Error fetching stats:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchStats)
</script>

<template>
  <div class="stats-view">
    <div class="header">
      <RouterLink to="/" class="back-link"><ArrowLeft :size="20" /> Назад</RouterLink>
      <h1>Статистика магазина</h1>
    </div>

    <div v-if="loading" class="loading-state">
      <Loader2 class="spinner" :size="48" />
      <p>Загрузка статистики...</p>
    </div>

    <div v-else-if="shopStats" class="stats-container">
      <div class="summary-cards">
        <div class="summary-card">
          <div class="card-icon"><BarChart3 /></div>
          <div class="card-content">
            <span class="label">Всего растений</span>
            <span class="value">{{ shopStats.stats.total_plants }}</span>
          </div>
        </div>
        <div class="summary-card">
          <div class="card-icon"><TrendingUp /></div>
          <div class="card-content">
            <span class="label">Средняя цена</span>
            <span class="value">{{ shopStats.stats.avg_price?.toFixed(0) }} ₽</span>
          </div>
        </div>
        <div class="summary-card">
          <div class="card-icon"><Tag /></div>
          <div class="card-content">
            <span class="label">Общая стоимость</span>
            <span class="value">{{ shopStats.stats.total_stock_value?.toFixed(0) }} ₽</span>
          </div>
        </div>
      </div>

      <div class="details-grid">
        <section class="details-section">
          <h2>Популярные растения</h2>
          <ul class="stats-list">
            <li v-for="plant in shopStats.popular" :key="plant.id">
              <span class="name">{{ plant.name }}</span>
              <span class="count">{{ plant.order_count }} заказов</span>
            </li>
          </ul>
        </section>

        <section class="details-section">
          <h2>Выручка по растениям</h2>
          <ul class="stats-list">
            <li v-for="item in shopStats.revenue" :key="item.name">
              <span class="name">{{ item.name }}</span>
              <span class="count">{{ item.revenue.toFixed(0) }} ₽</span>
            </li>
          </ul>
        </section>

        <section class="details-section">
          <h2>Категории</h2>
          <ul class="stats-list">
            <li v-for="cat in shopStats.categories" :key="cat.name">
              <span class="name">{{ cat.name }}</span>
              <span class="count">{{ cat.num_plants }} видов</span>
            </li>
          </ul>
        </section>

        <section class="details-section journal-summary">
          <h2>Журнал</h2>
          <div class="journal-stats">
            <p>Активных статей: <strong>{{ shopStats.active_articles }}</strong></p>
            <p>Наши авторы: <strong>{{ shopStats.authors.join(', ') }}</strong></p>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.header {
  margin-bottom: 40px;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  text-decoration: none;
  margin-bottom: 16px;
  font-weight: 500;
}

.back-link:hover {
  color: #4CAF50;
}

h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin: 0;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 0;
  color: #666;
}

.spinner {
  animation: rotate 2s linear infinite;
  margin-bottom: 16px;
  color: #4CAF50;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.summary-card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  display: flex;
  align-items: center;
  gap: 20px;
}

.card-icon {
  background: #e8f5e9;
  color: #4CAF50;
  padding: 12px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-content {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 4px;
}

.value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 32px;
}

.details-section {
  background: white;
  padding: 32px;
  border-radius: 20px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

h2 {
  font-size: 1.25rem;
  color: #2c3e50;
  margin: 0 0 24px 0;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 12px;
}

.stats-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.stats-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f8f8f8;
}

.stats-list li:last-child {
  border-bottom: none;
}

.name {
  color: #444;
  font-weight: 500;
}

.count {
  color: #4CAF50;
  font-weight: 600;
  background: #f1f8f1;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
}

.journal-summary {
  display: flex;
  flex-direction: column;
}

.journal-stats p {
  margin: 12px 0;
  color: #444;
}

.journal-stats strong {
  color: #4CAF50;
}
</style>
