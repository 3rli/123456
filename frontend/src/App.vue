<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { ShoppingCart, User, Sprout, Menu, X } from 'lucide-vue-next'
import { useCartStore } from './stores/cart'
import { useAuthStore } from './stores/auth'

const cartStore = useCartStore()
const authStore = useAuthStore()
const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

onMounted(() => {
  authStore.fetchMe()
  cartStore.fetchCart()
})
</script>

<template>
  <div class="app-container">
    <a href="#main-content" class="skip-link">Перейти к основному контенту</a>
    <header class="main-header">
      <div class="container header-content">
        <RouterLink to="/" class="logo" @click="closeMenu">
          <Sprout class="logo-icon" />
          <span>GreenLife</span>
        </RouterLink>
        
        <nav :class="['main-nav', { 'is-mobile-open': isMenuOpen }]">
          <RouterLink to="/" class="nav-link" @click="closeMenu">Магазин</RouterLink>
          <RouterLink to="/articles" class="nav-link" @click="closeMenu">Статьи</RouterLink>
          
          <div class="mobile-auth-links" v-if="isMenuOpen">
            <template v-if="authStore.isAuthenticated">
              <RouterLink to="/profile" class="nav-link" @click="closeMenu">Профиль ({{ authStore.user?.username }})</RouterLink>
            </template>
            <template v-else>
              <RouterLink to="/login" class="nav-link" @click="closeMenu">Вход</RouterLink>
              <RouterLink to="/register" class="nav-link" @click="closeMenu">Регистрация</RouterLink>
            </template>
          </div>
        </nav>

        <div class="header-actions">
          <div class="desktop-auth">
            <template v-if="authStore.isAuthenticated">
              <RouterLink to="/profile" class="user-info-btn">
                <User :size="18" />
                <span>{{ authStore.user?.username }}</span>
              </RouterLink>
            </template>
            <template v-else>
              <RouterLink to="/login" class="nav-btn login-btn">Вход</RouterLink>
              <RouterLink to="/register" class="nav-btn register-btn">Регистрация</RouterLink>
            </template>
          </div>

          <RouterLink to="/cart" class="action-btn cart-btn" title="Корзина" @click="closeMenu">
            <ShoppingCart :size="20" />
            <span v-if="cartStore.totalItems > 0" class="cart-badge">{{ cartStore.totalItems }}</span>
          </RouterLink>

          <button class="menu-toggle" @click="toggleMenu" aria-label="Toggle menu">
            <Menu v-if="!isMenuOpen" :size="24" />
            <X v-else :size="24" />
          </button>
        </div>
      </div>
    </header>

    <main id="main-content" class="main-content">
      <div class="container">
        <RouterView v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </RouterView>
      </div>
    </main>

    <footer class="main-footer">
      <div class="container footer-content">
        <p>&copy; 2026 Магазин GreenLife. Все права защищены.</p>
        <div class="footer-links">
          <a href="#">О нас</a>
          <a href="#">Контакты</a>
          <a href="#">Политика конфиденциальности</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<style src="./App.css"></style>
