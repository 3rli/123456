<script setup lang="ts">
import { useCartStore } from '../stores/cart'
import { ShoppingBag, Trash2, Plus, Minus, ArrowRight } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()
const cartStore = useCartStore()

const handleCheckout = () => {
  router.push('/checkout')
}
</script>

<template>
  <div class="cart-view">
    <h1 class="page-title">Корзина покупок</h1>

    <div v-if="cartStore.items.length === 0" class="empty-cart">
      <div class="empty-icon">
        <ShoppingBag :size="64" />
      </div>
      <h2>Ваша корзина пуста</h2>
      <p>Похоже, вы еще не добавили ни одного растения в свою коллекцию.</p>
      <RouterLink to="/" class="continue-btn">Начать покупки</RouterLink>
    </div>

    <div v-else class="cart-content">
      <div class="cart-items">
        <div v-for="item in cartStore.items" :key="item.plant.id" class="cart-item">
          <img :src="item.plant.image || 'https://via.placeholder.com/100x100?text=Растение'" :alt="item.plant.name" class="item-image" />
          
          <div class="item-details">
            <h3 class="item-name">{{ item.plant.name }}</h3>
            <p class="item-category">{{ item.plant.category?.name || 'Растение' }}</p>
            <span class="item-price-unit">{{ item.plant.price }} ₽ за шт.</span>
          </div>

          <div class="item-quantity">
            <button @click="cartStore.updateQuantity(item.plant.id, item.quantity - 1)" class="qty-btn">
              <Minus :size="16" />
            </button>
            <span class="qty-value">{{ item.quantity }}</span>
            <button @click="cartStore.updateQuantity(item.plant.id, item.quantity + 1)" class="qty-btn">
              <Plus :size="16" />
            </button>
          </div>

          <div class="item-total">
            {{ (parseFloat(item.plant.price) * item.quantity).toFixed(0) }} ₽
          </div>

          <button @click="cartStore.removeFromCart(item.plant.id)" class="remove-btn" title="Удалить">
            <Trash2 :size="20" />
          </button>
        </div>
      </div>

      <div class="cart-summary">
        <h2>Итого</h2>
        <div class="summary-row">
          <span>Сумма</span>
          <span>{{ cartStore.totalPrice.toFixed(0) }} ₽</span>
        </div>
        <div class="summary-row">
          <span>Доставка</span>
          <span class="free">Бесплатно</span>
        </div>
        <div class="summary-row total">
          <span>Всего</span>
          <span>{{ cartStore.totalPrice.toFixed(0) }} ₽</span>
        </div>
        
        <button @click="handleCheckout" class="checkout-btn">
          Оформить заказ <ArrowRight :size="20" />
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped src="./CartView.css"></style>
