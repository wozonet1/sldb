<template>
  <div class="font-sans bg-white dark:bg-neutral-white-dark text-gray-800 dark:text-gray-200 min-h-screen   flex flex-col transition-colors duration-300">
    <!-- 顶部导航栏 -->
    <Header />
    
    <!-- 主要内容区 -->
    <main class="flex-grow">
      <RouterView />
    </main>
    
    <!-- 页脚 -->
    <Footer />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'

// 初始化路由
const router = useRouter()

// 页面加载完成后执行
onMounted(() => {
  console.log('应用已加载完成')
})
</script>