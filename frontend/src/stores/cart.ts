import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from './auth'

export interface Tag { id: number; name: string }
export interface Article { id: number; title: string; slug: string; content: string; author: string; published_at: string; image: string }
export interface Plant { id: number; name: string; slug: string; price: string; image: string; description?: string; is_in_stock?: boolean; category?: { name: string }; tags?: Tag[]; articles?: Article[] }

export interface CartItem {
  id?: number
  plant: Plant
  quantity: number
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])
  const authStore = useAuthStore()

  const totalItems = computed(() => items.value.reduce((sum, item) => sum + item.quantity, 0))
  const totalPrice = computed(() => 
    items.value.reduce((sum, item) => sum + parseFloat(item.plant.price) * item.quantity, 0)
  )

  async function fetchCart() {
    if (!authStore.isAuthenticated) {
      items.value = JSON.parse(localStorage.getItem('cart') || '[]')
      return
    }
    try {
      const response = await axios.get('http://localhost:8000/api/cart/')
      items.value = response.data.items || []
    } catch (error) {
      console.error('Error fetching cart:', error)
    }
  }

  async function addToCart(plant: Plant) {
    if (!authStore.isAuthenticated) {
      const existingItem = items.value.find(i => i.plant.id === plant.id)
      if (existingItem) {
        existingItem.quantity++
      } else {
        items.value.push({ plant, quantity: 1 })
      }
      saveLocal()
      return
    }
    
    try {
      const response = await axios.post('http://localhost:8000/api/cart/add_item/', {
        plant_id: plant.id,
        quantity: 1
      })
      items.value = response.data.items
    } catch (error) {
      console.error('Error adding to cart:', error)
    }
  }

  async function removeFromCart(plantId: number) {
    if (!authStore.isAuthenticated) {
      items.value = items.value.filter(i => i.plant.id !== plantId)
      saveLocal()
      return
    }
    await updateQuantity(plantId, 0)
  }

  async function updateQuantity(plantId: number, quantity: number) {
    if (!authStore.isAuthenticated) {
      const item = items.value.find(i => i.plant.id === plantId)
      if (item) {
        item.quantity = quantity
        if (item.quantity <= 0) items.value = items.value.filter(i => i.plant.id !== plantId)
      }
      saveLocal()
      return
    }

    try {
      const response = await axios.post('http://localhost:8000/api/cart/update_item/', {
        plant_id: plantId,
        quantity: quantity
      })
      items.value = response.data.items
    } catch (error) {
      console.error('Error updating quantity:', error)
    }
  }

  async function clearCart() {
    if (!authStore.isAuthenticated) {
      items.value = []
      saveLocal()
      return
    }
    try {
      const response = await axios.post('http://localhost:8000/api/cart/clear/')
      items.value = response.data.items
    } catch (error) {
      console.error('Error clearing cart:', error)
    }
  }

  function saveLocal() {
    localStorage.setItem('cart', JSON.stringify(items.value))
  }

  return { items, totalItems, totalPrice, fetchCart, addToCart, removeFromCart, updateQuantity, clearCart }
})
