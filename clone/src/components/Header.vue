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
        <div class="flex items-center">
          <nav class="hidden md:flex space-x-8">
            <router-link 
              to="/" 
              class="text-white hover:text-white transition-all duration-200 
                    hover:outline  hover:outline-accent/30  hover:bg-accent-hover
                    hover:outline-offset-2 px-2 py-1 rounded"
            >{{ $t('header.home') }}</router-link>
            <router-link 
              to="/search" 
              class="text-white hover:text-white transition-all duration-200 
                    hover:outline  hover:outline-accent/30  hover:bg-accent-hover
                    hover:outline-offset-2 px-2 py-1 rounded"
            >{{ $t('header.search') }}</router-link>
            
            <router-link 
              to="/about" 
              class="text-white hover:text-white transition-all duration-200 
                    hover:outline  hover:outline-accent/30  hover:bg-accent-hover
                    hover:outline-offset-2 px-2 py-1 rounded"
            >{{ $t('header.about') }}</router-link>
          </nav>
          
          <!-- 语言切换按钮 -->
          <div class="relative ml-8">
            <button 
              @click="toggleLanguageMenu" 
              @blur="closeLanguageMenu"
              class="text-white hover:text-white transition-all duration-200 
                    hover:outline hover:outline-accent/30 hover:bg-accent-hover
                    hover:outline-offset-2 px-2 py-1 rounded flex items-center"
            >
              <span>{{ $t('header.language') }}</span>
              <i class="fas fa-chevron-down ml-1 text-xs"></i>
            </button>
            
            <!-- 语言下拉菜单 -->
            <div 
              v-if="languageMenuOpen" 
              class="absolute right-0 mt-2 w-40 bg-white rounded-md shadow-lg py-1 z-50 animate-fade-in"
            >
              <button 
                @click="changeLanguage('zh')" 
                class="block w-full text-left px-4 py-2 text-gray-800 hover:bg-gray-100"
                :class="{ 'bg-gray-100': currentLanguage === 'zh' }"
              >
                中文
              </button>
              <button 
                @click="changeLanguage('en')" 
                class="block w-full text-left px-4 py-2 text-gray-800 hover:bg-gray-100"
                :class="{ 'bg-gray-100': currentLanguage === 'en' }"
              >
                English
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'

// 获取i18n实例
const { t, locale } = useI18n()

// 导航菜单状态（移动端）
const menuOpen = ref(false)

// 语言菜单状态
const languageMenuOpen = ref(false)

// 当前语言
const currentLanguage = computed(() => locale.value)

// 切换菜单显示状态
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

// 切换语言菜单显示状态
const toggleLanguageMenu = () => {
  languageMenuOpen.value = !languageMenuOpen.value
}

// 关闭语言菜单
const closeLanguageMenu = () => {
  // 使用setTimeout避免点击菜单项时菜单立即关闭
  setTimeout(() => {
    languageMenuOpen.value = false
  }, 200)
}

// 切换语言
const changeLanguage = (lang) => {
  locale.value = lang
  localStorage.setItem('language', lang)
  languageMenuOpen.value = false
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