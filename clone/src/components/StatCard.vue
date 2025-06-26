<template>
  <div class="bg-white rounded-xl shadow-md p-6 text-center transform hover:-translate-y-1 transition-transform">
    <div class="text-4xl font-bold text-primary mb-2">{{ value }}</div>
    <div class="text-gray-600">{{ label }}</div>
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