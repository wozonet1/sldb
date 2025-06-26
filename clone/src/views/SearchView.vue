<template>
  <div class="space-y-8">
    <h1 class="text-3xl font-bold">搜索基因对</h1>
    
    <!-- 搜索表单 -->
    <div class="bg-white rounded-xl shadow-md p-6">
      <form @submit.prevent="searchGenes">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="gene1" class="block text-sm font-medium text-gray-700 mb-1">基因 1</label>
            <input 
              type="text" 
              id="gene1" 
              v-model="searchForm.gene1" 
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary transition-colors"
              placeholder="输入基因名称"
            >
          </div>
          
          <div>
            <label for="gene2" class="block text-sm font-medium text-gray-700 mb-1">基因 2(可选)</label>
            <input 
              type="text" 
              id="gene2" 
              v-model="searchForm.gene2" 
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary transition-colors"
              placeholder="输入基因名称"
            >
          </div>
          

        </div>
        
        <div class="mt-6 flex justify-end">
          <button 
            type="submit" 
            class="px-6 py-2 bg-[#ff9f7f] text-white rounded-lg hover:bg-[#ff8c66] transition-colors"
          >
            <i class="fa fa-search mr-2"></i>搜索
          </button>
        </div>
      </form>
    </div>
    
    <!-- 搜索结果 -->
    <div v-if="searchResults.length > 0" class="bg-white rounded-xl shadow-md overflow-hidden">
      <div class="p-6 border-b border-gray-200">
        <h2 class="text-xl font-semibold">搜索结果 ({{ searchResults.length }})</h2>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">基因 1</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">基因 2</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">预测分数</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">预测关系</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(result, index) in searchResults" :key="index" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ result['Gene A'] }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ result['Gene B'] }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ result['Prediction score'] }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ result['Predicting relation'] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- 分页 -->
      <div class="p-6 border-t border-gray-200 flex items-center justify-between">
        <div class="flex-1 flex justify-between sm:hidden">
          <button class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">上一页</button>
          <button class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">下一页</button>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              显示第 <span class="font-medium">1</span> 到 <span class="font-medium">10</span> 条，共 <span class="font-medium">{{ searchResults.length }}</span> 条结果
            </p>
          </div>
          <div>
            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
              <button class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                <span class="sr-only">上一页</span>
                <i class="fa fa-chevron-left"></i>
              </button>
              <button class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-primary text-sm font-medium text-white">1</button>
              <button class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">2</button>
              <button class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">3</button>
              <span class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">...</span>
              <button class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50">10</button>
              <button class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                <span class="sr-only">下一页</span>
                <i class="fa fa-chevron-right"></i>
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 无结果提示 -->
    <div v-else-if="!loading && searchPerformed" class="bg-white rounded-xl shadow-md p-8 text-center">
      <div class="text-5xl text-gray-300 mb-4">
        <i class="fa fa-search"></i>
      </div>
      <h3 class="text-xl font-semibold text-gray-900 mb-2">未找到匹配结果</h3>
      <p class="text-gray-500 mb-6">尝试使用不同的搜索条件或关键词</p>
      <button 
        class="px-6 py-2 bg-[#ff9f7f] text-white rounded-lg hover:bg-[#ff8c66] transition-colors shadow-md"
        @click="resetSearch"
      >
        重置搜索
      </button>
    </div>
    
    <!-- 加载中状态 -->
    <div v-else-if="loading" class="bg-white rounded-xl shadow-md p-8 text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mx-auto mb-4"></div>
      <p class="text-gray-500">正在搜索...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, defineProps  } from 'vue'
import {  router} from 'vue-router'
import axios from 'axios'


const props = defineProps({
  geneA: { type: String, default: '' },
  geneB: { type: String, default: '' }
})

const searchForm = reactive({
  gene1: props.geneA || '',
  gene2: props.geneB || ''
})

const searchResults = ref([])
const loading = ref(false)
const searchPerformed = ref(false)

watch([() => props.geneA, () => props.geneB], ([geneA, geneB]) => {
  searchForm.gene1 = geneA || ''
  searchForm.gene2 = geneB || ''
  if (searchForm.gene1 || searchForm.gene2) {
    searchGenes()
  }
})

onMounted(() => {
  if (searchForm.gene1 || searchForm.gene2) {
    searchGenes()
  }
})

// 执行搜索
const searchGenes = async () => {
  loading.value = true
  searchPerformed.value = true
  searchResults.value = [] // 清空之前的搜索结果

  // 更新路由查询参数
  router.push({
    query: {
      geneA: searchForm.gene1 || undefined,
      geneB: searchForm.gene2 || undefined
    }
  })

  try {
    const response = await axios.get('http://localhost:5555/predict', {
      params: {
        geneA: searchForm.gene1,
        geneB: searchForm.gene2
      }
    })
    searchResults.value = response.data
  } catch (error) {
    console.error('Error fetching search results:', error)
    searchResults.value = []
  } finally {
    loading.value = false
  }
}

// 重置搜索
const resetSearch = () => {
  searchForm.gene1 = ''
  searchForm.gene2 = ''
  searchResults.value = []
  searchPerformed.value = false
  router.push({ query: {} }) // Clear query parameters
}
</script>