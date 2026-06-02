import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PlantDetailView from '../views/PlantDetailView.vue'
import ArticlesView from '../views/ArticlesView.vue'
import ProfileView from '../views/ProfileView.vue'
import CartView from '../views/CartView.vue'

import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

import CheckoutView from '../views/CheckoutView.vue'
import OrderSuccessView from '../views/OrderSuccessView.vue'
import ArticleDetailView from '../views/ArticleDetailView.vue'
import StatsView from '../views/StatsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/stats',
      name: 'stats',
      component: StatsView
    },
    {
      path: '/articles',
      name: 'articles',
      component: ArticlesView
    },
    {
      path: '/article/:id/:slug',
      name: 'article-detail',
      component: ArticleDetailView,
      props: true
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: CheckoutView
    },
    {
      path: '/order-success/:id',
      name: 'order-success',
      component: OrderSuccessView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/plant/:id/:slug',
      name: 'plant-detail',
      component: PlantDetailView,
      props: true
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartView
    }
  ],
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
