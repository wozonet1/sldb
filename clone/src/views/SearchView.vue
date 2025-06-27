<template>
  <div class="space-y-8">
    <h1 class="text-3xl font-bold">{{ $t('search.title') }}</h1>
    
    <!-- 搜索表单 -->
    <div class="bg-white rounded-xl shadow-md p-6">
      <form @submit.prevent="searchGenes">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="gene1" class="block text-sm font-medium text-gray-700 mb-1">{{ $t('search.gene1') }}</label>
            <input 
              type="text" 
              id="gene1" 
              v-model="searchForm.gene1" 
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary transition-colors"
              :placeholder="$t('search.inputPlaceholder')"
            >
          </div>
          
          <div>
            <label for="gene2" class="block text-sm font-medium text-gray-700 mb-1">{{ $t('search.gene2') }}</label>
            <input 
              type="text" 
              id="gene2" 
              v-model="searchForm.gene2" 
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary transition-colors"
              :placeholder="$t('search.inputPlaceholder')"
            >
          </div>
          

        </div>
        
        <div class="mt-6 flex justify-end">
          <button 
            type="submit" 
            class="px-6 py-2 bg-accent text-white rounded-lg hover:bg-accent-hover transition-colors"
          >
            <i class="fa fa-search mr-2"></i>{{ $t('search.searchButton') }}
          </button>
        </div>
      </form>
    </div>
    <!-- 搜索结果：单个对象的特殊展示 -->
    <div 
      v-if="
        !Array.isArray(searchResults) && 
        Object.keys(searchResults).length > 0 && 
        !loading && 
        searchPerformed
      " 
      class="bg-white rounded-xl shadow-md p-6 space-y-4"
    >
      <h2 class="text-xl font-semibold">{{ $t('search.results') }} </h2>
      <div class="space-y-2">
        <p><strong>{{ $t('search.table.gene1') }}:</strong> {{ searchResults.GeneA }}</p>
        <p><strong>{{ $t('search.table.gene2') }}:</strong> {{ searchResults.GeneB }}</p>
        <p><strong>{{ $t('search.table.predictionScore') }}:</strong> {{ searchResults.Prediction }}</p>
        <p><strong>{{ $t('search.table.predictingRelation') }}:</strong> {{ searchResults['Predicting relation']?.slice(-3) === '_SL' ? 'SL' : 'nonSL' }}</p>
        <p><strong>{{ $t('search.table.source') }}:</strong> {{ searchResults['Predicting relation']?.slice(3) === 'new' ? 'Struct2SL' : 'SynlethDB' }}</p>
      </div>
    </div>

   <!-- 多结果表格 + 分页 -->
    <div v-else-if="Array.isArray(searchResults)" class="bg-white rounded-xl shadow-md overflow-hidden">
      <div class="p-6 border-b border-gray-200">
        <h2 class="text-xl font-semibold">
          {{ $t('search.results') }} ({{ searchResults.length }})
        </h2>
      </div>

      <!-- 表格：只渲染当前页数据 -->
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <!-- 原有表头代码... -->
          <tbody class="bg-white divide-y divide-gray-200">
            <tr 
              v-for="(result, index) in paginatedResults" 
              :key="index" 
              class="hover:bg-gray-50 transition-colors"
            >
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ result['Gene A'] }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ result['Gene B'] }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ result['Prediction score'] }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ result['Predicting relation']?.slice(-3) === '_SL' ? 'SL' : 'nonSL' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页组件 -->
      <Pagination 
        :total-items="searchResults.length" 
        :page-size="10" 
        :current-page="currentPage" 
        @goToPage="goToPage" 
        @goToPrevious="goToPreviousPage" 
        @goToNext="goToNextPage" 
      />
    </div>
    <!-- 加载中状态 -->
    <div v-else-if="loading" class="bg-white rounded-xl shadow-md p-8 text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mx-auto mb-4"></div>
      <p class="text-gray-500">{{ $t('search.loading') }}</p>
    </div>
    
    <!-- 无结果提示 -->
    <div v-else-if="!loading && searchPerformed && (!searchResults || searchResults.length === 0)" class="bg-white rounded-xl shadow-md p-8 text-center">
      <div class="text-5xl text-gray-300 mb-4">
        <i class="fa fa-search"></i>
      </div>
      <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ $t('search.noResults.title') }}</h3>
      <p class="text-gray-500 mb-6">{{ $t('search.noResults.suggestion') }}</p>
      <button 
        class="px-6 py-2 bg-accent text-white rounded-lg hover:bg-accent-hover transition-colors shadow-md"
        @click="resetSearch"
      >
        {{ $t('search.noResults.reset') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, defineProps, computed } from 'vue'
import { useRouter } from 'vue-router' // 导入 useRouter 钩子
import { useI18n } from 'vue-i18n' // 导入 useI18n 钩子
import axios from 'axios'
import Pagination from '@/components/Pagination.vue' // 导入分页组件

// 获取i18n实例
const { t } = useI18n()

const props = defineProps({
  geneA: { type: String, default: '' },
  geneB: { type: String, default: '' }
})

const router = useRouter() // 使用 useRouter 钩子获取路由实例

const searchForm = reactive({
  gene1: props.geneA || '',
  gene2: props.geneB || ''
})

const searchResults = ref([])
const loading = ref(false)
const searchPerformed = ref(false)

// 分页相关变量
const currentPage = ref(1)
const pageSize = ref(10)
const totalPages = computed(() => Math.ceil(searchResults.value.length / pageSize.value) || 1)

// 计算当前页显示的结果
const paginatedResults = computed(() => {
  if (!searchResults.value || searchResults.value.length === 0) {
    return []
  }
  
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return searchResults.value.slice(start, end)
})

// 计算显示的页码范围
const displayedPageNumbers = computed(() => {
  const range = []
  const maxVisiblePages = 5
  
  if (totalPages.value <= 0) {
    return range
  }
  
  const startPage = Math.max(1, currentPage.value - Math.floor(maxVisiblePages / 2))
  const endPage = Math.min(totalPages.value, startPage + maxVisiblePages - 1)
  
  for (let i = startPage; i <= endPage; i++) {
    range.push(i)
  }
  
  return range
})

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
  currentPage.value = 1 // 重置为第一页

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
  currentPage.value = 1
  router.push({ query: {} }) // Clear query parameters
}

// 页码变更
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

// 上一页
const goToPreviousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

// 下一页
const goToNextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}
</script>