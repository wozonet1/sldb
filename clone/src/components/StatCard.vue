<template>
  <div class="bg-white dark:bg-neutral-800 rounded-xl shadow-md p-6 text-center transform hover:-translate-y-1 transition-all duration-300">
    <div class="text-4xl font-bold text-primary dark:text-primary-dark mb-2 transition-colors duration-300">{{ value }}</div>
    <div class="text-gray-600 dark:text-gray-300 transition-colors duration-300">{{ label }}</div>
  </div>
</template>

<script setup>
defineProps({
  value: {
    type: [String, Number],
    required: true
  },
  label: {
    type: String,
    required: true
  }
})
</script>