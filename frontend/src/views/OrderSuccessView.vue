<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { CheckCircle, Package, Truck, Calendar, MapPin, ArrowRight, Loader2, ArrowLeft } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const order = ref<any>(null)
const loading = ref(true)

const fetchOrder = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/orders/${route.params.id}/`)
    order.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке заказа:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchOrder)
</script>

<template>
  <div class="success-view">
    <div v-if="loading" class="loading-state">
      <Loader2 class="spinner" :size="48" />
    </div>

    <div v-else-if="!order" class="error-state">
      <h2>Заказ не найден</h2>
      <RouterLink to="/">Вернуться на главную</RouterLink>
    </div>

    <div v-else class="success-content">
      <button @click="router.push('/profile')" class="back-link">
        <ArrowLeft :size="20" /> Вернуться в профиль
      </button>

      <div class="success-header">
        <div class="check-icon">
          <CheckCircle :size="64" />
        </div>
        <h1>Спасибо за ваш заказ!</h1>
        <p>Заказ <strong>#{{ order.id }}</strong> был успешно оформлен.</p>
        <p class="sub-text">Мы отправили подтверждение на {{ order.customer_email }}</p>
      </div>

      <div class="order-details-grid">
        <div class="card order-info-card">
          <h3><Package :size="20" /> Состав заказа</h3>
          <div class="items-list">
            <div v-for="item in order.items" :key="item.id" class="order-item">
              <img :src="item.plant.image" class="item-img" />
              <div class="item-meta">
                <p class="name">{{ item.plant.name }}</p>
                <p class="qty">Количество: {{ item.quantity }} шт.</p>
              </div>
              <p class="price">{{ (parseFloat(item.price) * item.quantity).toFixed(0) }} ₽</p>
            </div>
          </div>
          <div class="total-row">
            <span>Итого к оплате</span>
            <span class="total-price">{{ order.get_total_cost }} ₽</span>
          </div>
        </div>

        <div class="shipping-details">
          <div class="card">
            <h3><Truck :size="20" /> Детали доставки</h3>
            <div class="info-group">
              <div class="info-item">
                <MapPin :size="18" />
                <div>
                  <p class="label">Адрес</p>
                  <p>{{ order.address }}, {{ order.city }}</p>
                </div>
              </div>
              <div class="info-item">
                <Calendar :size="18" />
                <div>
                  <p class="label">Ожидаемая дата доставки</p>
                  <p>{{ new Date(order.delivery_date).toLocaleDateString() }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="actions">
            <RouterLink to="/" class="continue-btn">
              Продолжить покупки <ArrowRight :size="20" />
            </RouterLink>
            <RouterLink to="/profile" class="orders-btn">
              Все мои заказы
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped src="./OrderSuccessView.css"></style>
