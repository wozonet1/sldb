<template>
  <header class="bg-primary shadow-md sticky top-0 z-50">
    <div class="container mx-auto px-8 pt-4 pb-4"> <!-- 用 pt/pb 替代 h-16 -->
      <div class="flex items-center justify-between">
        <!-- Logo及副标题区域 -->
        <div class="flex flex-col items-start"> 
          <router-link to="/" class="flex items-center">
            <span class="text-4xl font-bold text-white">Struct2SL</span>
          </router-link>
          <!-- 新增副标题 -->
          <p class="text-white text-lg opacity-90">Synthetic Lethality Prediction</p> 
        </div>
        
<!-- 导航链接 -->
<nav class="hidden md:flex space-x-8">
  <router-link 
    to="/" 
    class="text-white hover:text-white transition-all duration-200 
           hover:outline  hover:outline-accent/30  hover:bg-accent-hover
           hover:outline-offset-2 px-2 py-1 rounded"
  >首页</router-link>
  <router-link 
    to="/search" 
    class="text-white hover:text-white transition-all duration-200 
           hover:outline  hover:outline-accent/30  hover:bg-accent-hover
           hover:outline-offset-2 px-2 py-1 rounded"
  >搜索</router-link>
  
  <router-link 
    to="/about" 
    class="text-white hover:text-white transition-all duration-200 
           hover:outline  hover:outline-accent/30  hover:bg-accent-hover
           hover:outline-offset-2 px-2 py-1 rounded"
  >关于</router-link>
</nav>
        
        <!-- 用户操作区 
        <div class="flex items-center space-x-4">
          <button class="hidden md:block px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90 transition-colors">
            登录
          </button>
          <button class="md:hidden text-gray-700">
            <i class="fa fa-bars text-xl"></i>
          </button>
        </div>-->
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'

// 导航菜单状态（移动端）
const menuOpen = ref(false)

// 切换菜单显示状态
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}
</script>

<style scoped>

/* 自定义动画 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* 应用动画 */
.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}
</style>  