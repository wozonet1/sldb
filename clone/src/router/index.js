import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SearchView from '../views/SearchView.vue'
import BrowseView from '../views/BrowseView.vue'
import AboutView from '../views/AboutView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/search',
    name: 'Search',
    component: SearchView,
    props: (route) => ({ geneA: route.query.geneA, geneB: route.query.geneB })
  },
  {
    path: '/browse',
    name: 'Browse',
    component: BrowseView
  },
  {
    path: '/about',
    name: 'About',
    component: AboutView
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router