<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { ArrowLeft, Calendar, User, Loader2 } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const article = ref<any>(null)
const loading = ref(true)

const fetchArticle = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/articles/${route.params.id}/`)
    article.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке статьи:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchArticle)
</script>

<template>
  <div class="article-detail">
    <button @click="router.back()" class="back-link">
      <ArrowLeft :size="20" /> Назад к статьям
    </button>

    <div v-if="loading" class="loading-state">
      <Loader2 class="spinner" :size="48" />
    </div>

    <div v-else-if="!article" class="error-state">
      <h2>Статья не найдена</h2>
      <RouterLink to="/articles">Вернуться к списку</RouterLink>
    </div>

    <div v-else class="article-content">
      <header class="article-header">
        <h1 class="title">{{ article.title }}</h1>
        <div class="meta">
          <div class="meta-item">
            <User :size="16" />
            <span>{{ article.author }}</span>
          </div>
          <div class="meta-item">
            <Calendar :size="16" />
            <span>{{ new Date(article.published_at).toLocaleDateString() }}</span>
          </div>
        </div>
      </header>

      <div v-if="article.image" class="article-image-container">
        <img :src="article.image" :alt="article.title" class="article-image" />
      </div>

      <div class="content" v-html="article.content"></div>
    </div>
  </div>
</template>

<style scoped src="./ArticleDetailView.css"></style>
