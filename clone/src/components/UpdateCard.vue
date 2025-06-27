<template>
  <div class="bg-white dark:bg-neutral-800 rounded-xl shadow-md overflow-hidden transition-colors duration-300">
    <div class="p-6">
      <div class="flex items-center mb-4">
        <div class="bg-primary/10 dark:bg-primary-dark/20 text-primary dark:text-primary-dark p-2 rounded-full mr-3 transition-colors duration-300">
          <slot name="icon">
            <i class="fa fa-flask"></i>
          </slot>
        </div>
        <h3 class="font-semibold text-lg dark:text-white transition-colors duration-300">
          <slot name="title">更新标题</slot>
        </h3>
      </div>
      <p class="text-gray-600 dark:text-gray-300 mb-4 transition-colors duration-300">
        <slot name="content">更新内容描述</slot>
      </p>
      <div class="text-sm text-gray-500 dark:text-gray-400 transition-colors duration-300">
        <slot name="date">更新于 2023-01-01</slot>
      </div>
    </div>
  </div>
</template>

<script setup>
// 组件不需要任何特殊的逻辑，只使用插槽来接收内容
</script>