
<template>
  <div class="w-full px-4">
    <form @submit.prevent="handleSearch" class="flex shadow-lg max-w-[800px] mx-auto">
      <input 
        type="text" 
        v-model="searchQuery" 
        class="flex-grow px-6 py-3 bg-white dark:bg-neutral-700 border border-gray-200 dark:border-gray-600 rounded-l-lg focus:ring-2 focus:ring-primary dark:focus:ring-primary-dark focus:border-primary dark:focus:border-primary-dark transition-colors text-gray-800 dark:text-gray-200"
        :placeholder="getPlaceholder()"
        aria-label="搜索基因对"
      >
      <button 
        type="submit" 
        class="px-8 py-3 bg-accent dark:bg-accent-dark text-white rounded-r-lg hover:bg-accent-hover dark:hover:bg-accent transition-colors"
      >
        {{ $t('search.searchButton') }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// 获取双语占位符（通过i18n翻译）
const getPlaceholder = () => {
  return t('search.inputPlaceholder')  // 对应i18n中的翻译键
}
const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  try{
  if (searchQuery.value.trim()) {
    // 拆分基因（支持空格、逗号、分号分隔）
    const genes = searchQuery.value
      .split(/[\s,;]+/)       // 按空格/逗号/分号拆分
      .filter(gene => gene)   // 过滤空值
    
    // 跳转到搜索页并传递参数
    router.push({
      name: 'Search',  
      query: {
        geneA: genes[0] || '',
        geneB: genes[1] || ''  // 支持双基因搜索
      }
    })
  }
}catch (error) {
    console.error('搜索时发生错误:', error)
    // 可以在这里添加错误处理逻辑，比如显示提示信息
  }
}
</script>