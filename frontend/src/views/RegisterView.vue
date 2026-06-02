<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import { UserPlus, User, Mail, Lock, Loader2 } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await axios.post('http://localhost:8000/api/auth/register/', {
      username: username.value,
      email: email.value,
      password: password.value
    })
    authStore.setAuth(response.data.token, response.data.user)
    router.push('/')
  } catch (err: any) {
    error.value = err.response?.data?.username?.[0] || 'Ошибка регистрации'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-view">
    <div class="auth-card">
      <div class="auth-header">
        <div class="icon-bg">
          <UserPlus :size="32" class="primary-icon" />
        </div>
        <h1>Создать аккаунт</h1>
        <p>Присоединяйтесь к сообществу GreenLife</p>
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div v-if="error" class="error-msg">{{ error }}</div>
        
        <div class="input-group">
          <label for="username">Имя пользователя</label>
          <div class="input-wrapper">
            <User :size="18" class="input-icon" />
            <input v-model="username" type="text" id="username" placeholder="Выберите имя пользователя" required />
          </div>
        </div>

        <div class="input-group">
          <label for="email">Электронная почта</label>
          <div class="input-wrapper">
            <Mail :size="18" class="input-icon" />
            <input v-model="email" type="email" id="email" placeholder="Введите ваш email" required />
          </div>
        </div>

        <div class="input-group">
          <label for="password">Пароль</label>
          <div class="input-wrapper">
            <Lock :size="18" class="input-icon" />
            <input v-model="password" type="password" id="password" placeholder="Придумайте пароль" required />
          </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="loading">
          <Loader2 v-if="loading" class="spinner" :size="20" />
          <span v-else>Зарегистрироваться</span>
        </button>
      </form>

      <div class="auth-footer">
        <p>Уже есть аккаунт? <RouterLink to="/login">Войти</RouterLink></p>
      </div>
    </div>
  </div>
</template>

<style scoped src="./RegisterView.css"></style>
