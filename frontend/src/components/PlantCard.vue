<script setup lang="ts">
import { ShoppingCart, Eye } from 'lucide-vue-next'
import { useCartStore, type Plant } from '../stores/cart'

const props = defineProps<{
  plant: Plant
}>()

const cartStore = useCartStore()

const handleAddToCart = (e: Event) => {
  e.preventDefault()
  e.stopPropagation()
  cartStore.addToCart(props.plant)
}
</script>

<template>
  <div class="plant-card">
    <RouterLink :to="{ name: 'plant-detail', params: { id: plant.id, slug: plant.slug } }" class="card-link">
      <div class="image-container">
        <img :src="plant.image || 'https://via.placeholder.com/300x300?text=No+Image'" :alt="plant.name" class="plant-image" />
        <div class="overlay">
          <Eye :size="24" />
        </div>
      </div>
      <div class="card-info">
        <span class="category">{{ plant.category?.name || 'Plants' }}</span>
        <h3 class="name">{{ plant.name }}</h3>
        
        <div v-if="plant.tags && plant.tags.length > 0" class="tags-list">
          <span v-for="tag in plant.tags.slice(0, 2)" :key="tag.id" class="tag-item">#{{ tag.name }}</span>
        </div>

        <div class="card-footer">
          <span class="price">{{ plant.price }} ₽</span>
          <button @click="handleAddToCart" class="add-btn" title="Добавить в корзину">
            <ShoppingCart :size="18" />
          </button>
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<style scoped src="./PlantCard.css"></style>
