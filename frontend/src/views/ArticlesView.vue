<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Newspaper, Calendar, User, Loader2 } from 'lucide-vue-next'
import type { Article } from '../stores/cart'

const articles = ref<Article[]>([])
const loading = ref(true)

const fetchArticles = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/articles/')
    articles.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке статей:', error)
  } finally {
    loading.value = false
  }
}

const stripHtml = (html: string) => {
  const tmp = document.createElement("DIV");
  tmp.innerHTML = html;
  return tmp.textContent || tmp.innerText || "";
}

onMounted(fetchArticles)
</script>

<template>
  <div class="articles-view">
    <div class="page-header">
      <h1>Журнал GreenLife</h1>
      <p>Советы, хитрости и истории из мира растений.</p>
    </div>

    <div v-if="loading" class="loading-state">
      <Loader2 class="spinner" :size="48" />
    </div>

    <div v-else class="articles-grid">
      <article v-for="article in articles" :key="article.id" class="article-card">
        <div class="article-meta">
          <span class="category">Статья</span>
        </div>
        <h2 class="article-title">{{ article.title }}</h2>
        <p class="article-excerpt">{{ stripHtml(article.content).substring(0, 150) }}...</p>
        <div class="article-footer">
          <div class="author-info">
            <User :size="14" />
            <span>{{ article.author }}</span>
          </div>
          <div class="date-info">
            <Calendar :size="14" />
            <span>{{ new Date(article.published_at).toLocaleDateString() }}</span>
          </div>
        </div>
        <RouterLink :to="{ name: 'article-detail', params: { id: article.id, slug: article.slug } }" class="read-btn">
          Читать статью
        </RouterLink>
      </article>
    </div>
  </div>
</template>

<style scoped src="./ArticlesView.css"></style>
