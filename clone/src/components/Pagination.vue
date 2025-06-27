<!-- components/Pagination.vue -->
<template>
  <div class="p-6 border-t border-gray-200 dark:border-gray-600 flex items-center justify-between transition-colors duration-300">
    <!-- 移动端简易分页 -->
    <div class="flex-1 flex justify-between sm:hidden">
      <button 
        @click="goToPreviousPage" 
        :disabled="currentPage === 1"
        class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-200 bg-white dark:bg-neutral-700 hover:bg-gray-50 dark:hover:bg-neutral-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-300"
      >
        {{ $t('search.pagination.previous') }}
      </button>
      <button 
        @click="goToNextPage" 
        :disabled="currentPage === totalPages"
        class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-200 bg-white dark:bg-neutral-700 hover:bg-gray-50 dark:hover:bg-neutral-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-300"
      >
        {{ $t('search.pagination.next') }}
      </button>
    </div>

    <!-- 桌面端完整分页 -->
    <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
      <div>
        <p class="text-sm text-gray-700 dark:text-gray-300 transition-colors duration-300">
          {{ $t('search.pagination.showing') }} 
          <span class="font-medium">{{ (currentPage - 1) * pageSize + 1 }}</span> 
          {{ $t('search.pagination.to') }} 
          <span class="font-medium">{{ Math.min(currentPage * pageSize, totalItems) }}</span> 
          {{ $t('search.pagination.of') }} 
          <span class="font-medium">{{ totalItems }}</span> 
          {{ $t('search.pagination.results') }}
        </p>
      </div>
      <div>
        <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
          <!-- 上一页 -->
          <button 
            @click="goToPreviousPage" 
            :disabled="currentPage === 1"
            class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-neutral-700 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-neutral-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-300"
          >
            <span class="sr-only">{{ $t('search.pagination.previous') }}</span>
            <i class="fa fa-chevron-left"></i>
          </button>

          <!-- 第一页 -->
          <button 
            v-if="displayedPageNumbers[0] > 1" 
            @click="goToPage(1)" 
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-neutral-700 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-neutral-600 transition-colors duration-300"
          >
            1
          </button>

          <!-- 省略号（前） -->
          <span 
            v-if="displayedPageNumbers[0] > 2" 
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-neutral-700 text-sm font-medium text-gray-700 dark:text-gray-200 transition-colors duration-300"
          >
            ...
          </span>

          <!-- 中间页码 -->
          <button 
            v-for="page in displayedPageNumbers" 
            :key="page" 
            @click="goToPage(page)" 
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium transition-colors duration-300" 
            :class="{
              'bg-primary dark:bg-primary-dark text-white': page === currentPage,
              'bg-white dark:bg-neutral-700 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-neutral-600': page !== currentPage
            }"
          >
            {{ page }}
          </button>

          <!-- 省略号（后） -->
          <span 
            v-if="displayedPageNumbers.at(-1) < totalPages - 1" 
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-neutral-700 text-sm font-medium text-gray-700 dark:text-gray-200 transition-colors duration-300"
          >
            ...
          </span>

          <!-- 最后一页 -->
          <button 
            v-if="displayedPageNumbers.at(-1) < totalPages" 
            @click="goToPage(totalPages)" 
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-neutral-700 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-neutral-600 transition-colors duration-300"
          >
            {{ totalPages }}
          </button>

          <!-- 下一页 -->
          <button 
            @click="goToNextPage" 
            :disabled="currentPage === totalPages || totalPages === 0"
            class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-neutral-700 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-neutral-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-300"
          >
            <span class="sr-only">{{ $t('search.pagination.next') }}</span>
            <i class="fa fa-chevron-right"></i>
          </button>
        </nav>
      </div>
    </div>

    <!-- 页码跳转 -->
    <div class="mt-4 sm:mt-0 sm:ml-4 flex items-center">
      <label for="pageJump" class="mr-2 text-sm text-gray-700 dark:text-gray-300 transition-colors duration-300">{{ $t('search.pagination.goToPage') }}</label>
      <input 
        id="pageJump" 
        v-model="pageJump" 
        type="number" 
        min="1" 
        :max="totalPages" 
        class="w-16 px-2 py-1 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-neutral-700 text-gray-700 dark:text-gray-200 focus:outline-none focus:ring-primary dark:focus:ring-primary-dark focus:border-primary dark:focus:border-primary-dark transition-colors duration-300"
      >
      <label for="pageJump" class="mr-2 text-sm text-gray-700 dark:text-gray-300 transition-colors duration-300">{{ $t('search.pagination.Page') }}</label>
      <button 
        @click="goToPage(parseInt(pageJump))" 
        class="ml-2 px-3 py-1 bg-primary dark:bg-primary-dark text-white text-sm rounded-md hover:bg-primary-dark dark:hover:bg-primary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary dark:focus:ring-primary-dark transition-colors duration-300"
      >
        {{ $t('search.pagination.go') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// 接收父组件参数
const props = defineProps({
  totalItems: { type: Number, required: true }, // 总数据量
  pageSize: { type: Number, default: 10 },     // 每页条数
  currentPage: { type: Number, default: 1 },   // 当前页码
})

// 计算总页数
const totalPages = computed(() => Math.ceil(props.totalItems / props.pageSize) || 1)

// 计算显示的页码范围（最多显示 5 个）
const displayedPageNumbers = computed(() => {
  const maxVisible = 5
  const start = Math.max(1, props.currentPage - Math.floor(maxVisible / 2))
  const end = Math.min(totalPages.value, start + maxVisible - 1)
  
  return Array.from({ length: end - start + 1 }, (_, i) => start + i)
})

// 暴露事件给父组件
const emit = defineEmits(['goToPage', 'goToPrevious', 'goToNext'])

// 跳转到指定页
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    emit('goToPage', page)
  }
}

// 上一页
const goToPreviousPage = () => {
  if (props.currentPage > 1) {
    emit('goToPrevious', props.currentPage - 1)
  }
}

// 下一页
const goToNextPage = () => {
  if (props.currentPage < totalPages.value) {
    emit('goToNext', props.currentPage + 1)
  }
}
</script>