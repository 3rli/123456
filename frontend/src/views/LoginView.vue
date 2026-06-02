<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import { LogIn, User, Lock, Loader2 } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await axios.post('http://localhost:8000/api/auth/login/', {
      username: username.value,
      password: password.value
    })
    const token = response.data.token
    
    axios.defaults.headers.common['Authorization'] = `Token ${token}`
    const userResponse = await axios.get('http://localhost:8000/api/auth/me/')
    
    authStore.setAuth(token, userResponse.data)
    router.push('/')
  } catch (err: any) {
    error.value = 'Неверное имя пользователя или пароль'
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
          <LogIn :size="32" class="primary-icon" />
        </div>
        <h1>С возвращением!</h1>
        <p>Войдите в свой аккаунт GreenLife</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div v-if="error" class="error-msg">{{ error }}</div>
        
        <div class="input-group">
          <label for="username">Имя пользователя</label>
          <div class="input-wrapper">
            <User :size="18" class="input-icon" />
            <input v-model="username" type="text" id="username" placeholder="Введите имя пользователя" required />
          </div>
        </div>

        <div class="input-group">
          <label for="password">Пароль</label>
          <div class="input-wrapper">
            <Lock :size="18" class="input-icon" />
            <input v-model="password" type="password" id="password" placeholder="Введите пароль" required />
          </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="loading">
          <Loader2 v-if="loading" class="spinner" :size="20" />
          <span v-else>Войти</span>
        </button>
      </form>

      <div class="auth-footer">
        <p>Нет аккаунта? <RouterLink to="/register">Зарегистрироваться</RouterLink></p>
      </div>
    </div>
  </div>
</template>

<style scoped src="./LoginView.css"></style>
