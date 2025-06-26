<template>
  <div class="space-y-8">
    <h1 class="text-3xl font-bold">浏览基因对</h1>
    
    <!-- 筛选条件 -->
    <div class="bg-white rounded-xl shadow-md p-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label for="cancerTypeFilter" class="block text-sm font-medium text-gray-700 mb-1">癌症类型</label>
          <select 
            id="cancerTypeFilter" 
            v-model="filterOptions.cancerType" 
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary transition-colors"
          >
            <option value="">所有类型</option>
            <option value="breast">乳腺癌</option>
            <option value="lung">肺癌</option>
            <option value="colorectal">结直肠癌</option>
            <option value="prostate">前列腺癌</option>
            <option value="ovarian">卵巢癌</option>
          </select>
        </div>
        
        <div>
          <label for="evidenceLevelFilter" class="block text-sm font-medium text-gray-700 mb-1">证据水平</label>
          <select 
            id="evidenceLevelFilter" 
            v-model="filterOptions.evidenceLevel" 
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary transition-colors"
          >
            <option value="">所有水平</option>
            <option value="high">高</option>
            <option value="medium">中</option>
            <option value="low">低</option>
          </select>
        </div>
        
        <div>
          <label for="sortBy" class="block text-sm font-medium text-gray-700 mb-1">排序方式</label>
          <select 
            id="sortBy" 
            v-model="filterOptions.sortBy" 
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary transition-colors"
          >
            <option value="gene1">基因1 (A-Z)</option>
            <option value="-gene1">基因1 (Z-A)</option>
            <option value="gene2">基因2 (A-Z)</option>
            <option value="-gene2">基因2 (Z-A)</option>
            <option value="evidenceLevel">证据水平 (高到低)</option>
            <option value="-evidenceLevel">证据水平 (低到高)</option>
          </select>
        </div>
      </div>
    </div>
    
    <!-- 基因对列表 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="(genePair, index) in filteredGenePairs" 
        :key="index" 
        class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="font-semibold text-lg">{{ genePair.gene1 }} - {{ genePair.gene2 }}</h3>
              <p class="text-sm text-gray-500">{{ genePair.cancerType }}</p>
            </div>
            <span 
              :class="{
                'px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-800': genePair.evidenceLevel === 'high',
                'px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800': genePair.evidenceLevel === 'medium',
                'px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800': genePair.evidenceLevel === 'low'
              }"
            >
              {{ genePair.evidenceLevel }}
            </span>
          </div>
          
          <div class="mb-4">
            <p class="text-sm text-gray-600">
              {{ genePair.description }}
            </p>
          </div>
          
          <div class="flex justify-between items-center">
            <div class="text-sm text-gray-500">
              <span class="flex items-center">
                <i class="fa fa-flask mr-1"></i> {{ genePair.experiments }} 实验
              </span>
            </div>
            <button class="text-primary hover:text-primary/80 transition-colors">
              查看详情 <i class="fa fa-arrow-right ml-1"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 加载更多 -->
    <div class="text-center mt-8">
      <button 
        class="px-6 py-3 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors shadow-sm"
        @click="loadMore"
      >
        加载更多 <i class="fa fa-spinner ml-2" :class="{ 'animate-spin': loading }"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'

// 筛选选项
const filterOptions = reactive({
  cancerType: '',
  evidenceLevel: '',
  sortBy: 'gene1'
})

// 基因对数据
const allGenePairs = ref([
  { 
    gene1: 'BRCA1', 
    gene2: 'BRCA2', 
    cancerType: '乳腺癌', 
    evidenceLevel: 'high',
    description: 'BRCA1和BRCA2是著名的乳腺癌相关基因，它们在DNA修复中起关键作用，两者功能上相互依赖。',
    experiments: 24
  },
  { 
    gene1: 'TP53', 
    gene2: 'MDM2', 
    cancerType: '结直肠癌', 
    evidenceLevel: 'high',
    description: 'TP53是一种重要的抑癌基因，MDM2是其主要负调控因子，两者之间的失衡与多种癌症相关。',
    experiments: 18
  },
  { 
    gene1: 'KRAS', 
    gene2: 'NRAS', 
    cancerType: '肺癌', 
    evidenceLevel: 'medium',
    description: 'KRAS和NRAS是RAS基因家族的成员，在细胞增殖和存活信号通路中起关键作用，突变通常互斥。',
    experiments: 15
  },
  { 
    gene1: 'PIK3CA', 
    gene2: 'PTEN', 
    cancerType: '乳腺癌', 
    evidenceLevel: 'medium',
    description: 'PIK3CA编码PI3K激酶的催化亚基，而PTEN是一种肿瘤抑制因子，负调控PI3K/AKT信号通路。',
    experiments: 12
  },
  { 
    gene1: 'EGFR', 
    gene2: 'KRAS', 
    cancerType: '肺癌', 
    evidenceLevel: 'low',
    description: 'EGFR和KRAS在肺癌中经常被研究，EGFR突变的肿瘤通常对EGFR抑制剂敏感，而KRAS突变则不然。',
    experiments: 9
  },
  { 
    gene1: 'BRCA1', 
    gene2: 'PALB2', 
    cancerType: '卵巢癌', 
    evidenceLevel: 'high',
    description: 'PALB2与BRCA1和BRCA2相互作用，共同参与DNA双链断裂修复，PALB2功能丧失可导致对PARP抑制剂敏感。',
    experiments: 20
  }
])

// 当前显示的基因对数
const displayCount = ref(6)

// 加载状态
const loading = ref(false)

// 计算筛选后的基因对
const filteredGenePairs = computed(() => {
  // 筛选
  let filtered = allGenePairs.value.filter(genePair => {
    const cancerTypeMatch = filterOptions.cancerType ? genePair.cancerType.toLowerCase() === filterOptions.cancerType.toLowerCase() : true
    const evidenceLevelMatch = filterOptions.evidenceLevel ? genePair.evidenceLevel === filterOptions.evidenceLevel : true
    return cancerTypeMatch && evidenceLevelMatch
  })
  
  // 排序
  const sortField = filterOptions.sortBy.startsWith('-') ? filterOptions.sortBy.substring(1) : filterOptions.sortBy
  const sortDirection = filterOptions.sortBy.startsWith('-') ? -1 : 1
  
  filtered.sort((a, b) => {
    if (sortField === 'evidenceLevel') {
      // 证据水平排序（高>中>低）
      const order = { 'high': 3, 'medium': 2, 'low': 1 }
      return sortDirection * (order[a[sortField]] - order[b[sortField]])
    } else {
      // 字母排序
      return sortDirection * a[sortField].localeCompare(b[sortField])
    }
  })
  
  // 限制显示数量
  return filtered.slice(0, displayCount.value)
})

// 加载更多基因对
const loadMore = () => {
  loading.value = true
  
  // 模拟API请求延迟
  setTimeout(() => {
    displayCount.value += 6
    loading.value = false
  }, 800)
}

onMounted(() => {
  // 页面加载时可以执行一些初始化操作
})
</script>  