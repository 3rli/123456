<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import { User, Package, LogOut, ChevronRight, Loader2, Trash2, Edit2 } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()

const orders = ref<any[]>([])
const loading = ref(true)

const fetchOrders = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/orders/')
    orders.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке заказов:', error)
  } finally {
    loading.value = false
  }
}

const deleteOrder = async (id: number) => {
  if (!confirm('Вы уверены, что хотите удалить заказ #' + id + '?')) return
  try {
    await axios.delete(`http://localhost:8000/api/orders/${id}/`)
    orders.value = orders.value.filter(o => o.id !== id)
  } catch (error) {
    console.error('Ошибка при удалении заказа:', error)
  }
}

const renameOrder = async (order: any) => {
  const newName = prompt('Введите новое имя клиента:', order.customer_name)
  if (!newName) return
  try {
    const response = await axios.patch(`http://localhost:8000/api/orders/${order.id}/`, {
      customer_name: newName
    })
    const idx = orders.value.findIndex(o => o.id === order.id)
    if (idx !== -1) {
      orders.value[idx].customer_name = response.data.customer_name
    }
  } catch (error) {
    console.error('Ошибка при переименовании заказа:', error)
  }
}

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
  } else {
    fetchOrders()
  }
})

const getStatusClass = (status: string) => {
  switch (status) {
    case 'P': return 'status-pending'
    case 'S': return 'status-shipped'
    case 'D': return 'status-delivered'
    case 'C': return 'status-cancelled'
    default: return ''
  }
}

const getStatusLabel = (status: string) => {
  switch (status) {
    case 'P': return 'В ожидании'
    case 'PR': return 'В обработке'
    case 'S': return 'Отправлено'
    case 'D': return 'Доставлено'
    case 'C': return 'Отменено'
    default: return status
  }
}
</script>

<template>
  <div class="profile-view">
    <h1 class="page-title">Личный кабинет</h1>

    <div class="profile-layout">
      <aside class="profile-sidebar">
        <div class="user-card">
          <div class="avatar-placeholder">
            <User :size="48" />
          </div>
          <h2 class="user-name">{{ authStore.user?.username }}</h2>
          <p class="user-email">{{ authStore.user?.email || 'Email не указан' }}</p>
        </div>

        <nav class="profile-nav">
          <button class="nav-item active">
            <Package :size="20" /> Мои заказы
          </button>
          <button @click="handleLogout" class="nav-item logout">
            <LogOut :size="20" /> Выйти
          </button>
        </nav>
      </aside>

      <div class="profile-main">
        <div class="section-card">
          <h3>История заказов</h3>
          
          <div v-if="loading" class="loading-state">
            <Loader2 class="spinner" :size="32" />
          </div>

          <div v-else-if="orders.length === 0" class="empty-orders">
            <p>У вас пока нет оформленных заказов.</p>
            <RouterLink to="/" class="shop-now">Перейти к покупкам</RouterLink>
          </div>

          <div v-else class="orders-list">
            <div v-for="order in orders" :key="order.id" class="order-item">
              <div class="order-header">
                <div>
                  <span class="order-number">Заказ #{{ order.id }}</span>
                  <span class="customer-name-display"> ({{ order.customer_name }})</span>
                </div>
                <div class="order-actions">
                   <button @click="renameOrder(order)" class="order-action-btn" title="Изменить имя"><Edit2 :size="16" /></button>
                   <button @click="deleteOrder(order.id)" class="order-action-btn delete" title="Удалить"><Trash2 :size="16" /></button>
                </div>
              </div>
              
              <div class="order-body">
                <div class="order-info">
                  <span :class="['status-badge', getStatusClass(order.status)]">
                    {{ getStatusLabel(order.status) }}
                  </span>
                  <span class="order-date">{{ new Date(order.created_at).toLocaleDateString() }}</span>
                </div>
                <div class="order-price">
                  {{ order.get_total_cost }} ₽
                </div>
              </div>

              <div class="order-footer-actions">
                <button @click="router.push({ name: 'order-success', params: { id: order.id } })" class="view-details-link">
                  Подробнее о заказе <ChevronRight :size="16" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped src="./ProfileView.css"></style>
