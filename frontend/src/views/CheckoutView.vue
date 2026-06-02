<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'
import { MapPin, Phone, Calendar, ArrowLeft, Loader2, CreditCard } from 'lucide-vue-next'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

const formData = ref({
  customer_name: authStore.user?.username || '',
  customer_email: authStore.user?.email || '',
  phone: '',
  address: '',
  city: '',
  delivery_date: ''
})

const loading = ref(false)

onMounted(() => {
  if (cartStore.items.length === 0) {
    router.push('/cart')
  }
})

const placeOrder = async () => {
  loading.value = true
  try {
    const orderData = {
      ...formData.value,
      items: cartStore.items.map(item => ({
        plant_id: item.plant.id,
        price: item.plant.price,
        quantity: item.quantity
      }))
    }
    
    const response = await axios.post('http://localhost:8000/api/orders/', orderData)
    const orderId = response.data.id
    cartStore.clearCart()
    router.push({ name: 'order-success', params: { id: orderId } })
  } catch (error) {
    console.error('Ошибка при создании заказа:', error)
    alert('Не удалось оформить заказ. Пожалуйста, проверьте введенные данные.')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="checkout-view">
    <button @click="router.back()" class="back-link">
      <ArrowLeft :size="20" /> Назад в корзину
    </button>

    <h1 class="page-title">Оформление заказа</h1>

    <div class="checkout-layout">
      <div class="checkout-form-section">
        <div class="card">
          <h3>Информация о доставке</h3>
          <form @submit.prevent="placeOrder" class="checkout-form">
            <div class="form-grid">
              <div class="input-group">
                <label for="customer_name">Полное имя</label>
                <input v-model="formData.customer_name" id="customer_name" type="text" required placeholder="Иван Иванов" />
              </div>
              <div class="input-group">
                <label for="customer_email">Электронная почта</label>
                <input v-model="formData.customer_email" id="customer_email" type="email" required placeholder="ivan@example.com" />
              </div>
              <div class="input-group">
                <label for="phone">Номер телефона</label>
                <div class="input-wrapper">
                  <Phone :size="18" class="icon" />
                  <input v-model="formData.phone" id="phone" type="tel" required placeholder="+7 999 000 00 00" />
                </div>
              </div>
              <div class="input-group">
                <label for="delivery_date">Дата доставки</label>
                <div class="input-wrapper">
                  <Calendar :size="18" class="icon" />
                  <input v-model="formData.delivery_date" id="delivery_date" type="date" required />
                </div>
              </div>
            </div>

            <div class="input-group full-width">
              <label for="address">Адрес (улица, дом, квартира)</label>
              <div class="input-wrapper">
                <MapPin :size="18" class="icon" />
                <input v-model="formData.address" id="address" type="text" required placeholder="ул. Ленина, д. 1, кв. 10" />
              </div>
            </div>

            <div class="input-group">
              <label for="city">Город</label>
              <input v-model="formData.city" id="city" type="text" required placeholder="Москва" />
            </div>

            <div class="payment-section">
              <h3>Способ оплаты</h3>
              <div class="payment-card selected">
                <CreditCard :size="24" />
                <span>Оплата при получении</span>
              </div>
            </div>

            <button type="submit" class="place-order-btn" :disabled="loading">
              <Loader2 v-if="loading" class="spinner" :size="20" />
              <span v-else>Подтвердить заказ — {{ cartStore.totalPrice.toFixed(0) }} ₽</span>
            </button>
          </form>
        </div>
      </div>

      <aside class="order-summary-aside">
        <div class="card summary-card">
          <h3>Ваш заказ</h3>
          <div class="summary-items">
            <div v-for="item in cartStore.items" :key="item.plant.id" class="summary-item">
              <img :src="item.plant.image" class="item-thumb" />
              <div class="item-info">
                <p class="name">{{ item.plant.name }}</p>
                <p class="qty">Кол-во: {{ item.quantity }}</p>
              </div>
              <p class="price">{{ (parseFloat(item.plant.price) * item.quantity).toFixed(0) }} ₽</p>
            </div>
          </div>
          <div class="summary-totals">
            <div class="row">
              <span>Сумма</span>
              <span>{{ cartStore.totalPrice.toFixed(0) }} ₽</span>
            </div>
            <div class="row">
              <span>Доставка</span>
              <span class="free">Бесплатно</span>
            </div>
            <div class="row total">
              <span>Итого</span>
              <span>{{ cartStore.totalPrice.toFixed(0) }} ₽</span>
            </div>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<style scoped src="./CheckoutView.css"></style>
