
<template>
  <div class="w-full px-4">
    <form @submit.prevent="handleSearch" class="flex shadow-lg max-w-[800px] mx-auto">
      <input 
        type="text" 
        v-model="searchQuery" 
        class="flex-grow px-6 py-3 bg-white border border-gray-200 rounded-l-lg focus:ring-2 focus:ring-primary focus:border-primary transition-colors text-gray-800"
        :placeholder="placeholder"
        aria-label="搜索基因对"
      >
      <button 
        type="submit" 
        class="px-8 py-3 bg-[#ff9f7f] text-white rounded-r-lg hover:bg-[#ff8c66] transition-colors"
      >
        Search
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  placeholder: {
    type: String,
    default: '搜索基因对...(例如: TSPAN1)'
  }
})

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
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
}
</script>