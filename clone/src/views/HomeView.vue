<template>
  <div class="space-y-8">
    <!-- 英雄区域 -->
  <section class="bg-gradient-to-r from-blue-900 to-indigo-800 text-white py-20" style="background-image: url('./src/assets/bg-pattern.jpg'); background-size: cover; background-repeat: no-repeat; background-position: center;">
    <div class="max-w-7xl mx-auto px-4">
      <div class="text-center mb-8">
        <h1 class="text-5xl md:text-6xl font-bold mb-6">
          {{ $t('home.welcome') }}
        </h1>
        <p class="text-xl md:text-2xl mb-10">
          {{ $t('home.subtitle') }}
        </p>
        
        <!-- 搜索栏 -->
        <div class="mt-8 w-full">
          <SearchBar />
        </div>
      </div>
    </div>
  </section>

    
    <!-- 统计数据 -->
    <section class="grid grid-cols-2 md:grid-cols-4 gap-6 px-4">
      <StatCard value="12,543" :label="$t('home.stats.genePairs')" />
      <StatCard value="5,678" :label="$t('home.stats.experiments')" />
      <StatCard value="3,210" :label="$t('home.stats.cancerTypes')" />
      <StatCard value="890" :label="$t('home.stats.publications')" />
    </section>
    
    <!-- 最近更新 -->
    <section class="px-4">
      <h2 class="text-2xl font-bold mb-6">{{ $t('home.updates.title') }}</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <UpdateCard>
          <template #icon>
            <i class="fa fa-flask"></i>
          </template>
          <template #title>{{ $t('home.updates.newBreastCancer.title') }}</template>
          <template #content>{{ $t('home.updates.newBreastCancer.content') }}</template>
          <template #date>{{ $t('home.updates.newBreastCancer.date') }}</template>
        </UpdateCard>
        
        <!-- 可以轻松添加更多更新卡片 -->
        <UpdateCard>
          <template #icon>
            <i class="fa fa-code"></i>
          </template>
          <template #title>{{ $t('home.updates.websiteOptimization.title') }}</template>
          <template #content>{{ $t('home.updates.websiteOptimization.content') }}</template>
          <template #date>{{ $t('home.updates.websiteOptimization.date') }}</template>
        </UpdateCard>
      </div>
    </section>
    
   <!-- About Struct2SL 部分 -->
    <section class="px-4 py-12 bg-gray-50">
      <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 md:items-start">
        <div>
          <h2 class="text-3xl font-bold mb-6">{{ $t('about.title') }}</h2>
          <p class="text-gray-700 mb-5 text-xl leading-relaxed" style="max-width: 500px;">
            {{ $t('about.description') }} For
            more detailed instructions, please refer to <a href="https://github.com/hyr-hit/Struct2SL/blob/main/User%20Guide%20for%20webserver.md" class="text-primary hover:underline">here</a>.
          </p>
        </div>
        <div class="rounded-lg overflow-hidden shadow-lg">
          <!-- 图片占位符，稍后替换 -->
          <img src="../../src/assets/frame.jpg" alt="Struct2SL Model Framework" class="w-full h-auto">
        </div>
      </div>
    </section>
    
    <!-- Statistics of Struct2SL 部分 -->
    <section class="px-4 py-12 bg-gray-50">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold mb-6">{{ $t('home.statistics.title') }}</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 md:items-start">
          <div>
            <p class="text-gray-700 mb-4 text-xl leading-relaxed" style="max-width: 500px;">
              {{ $t('home.statistics.description') }}
            </p>
          </div>
          <div class="rounded-lg overflow-hidden shadow-lg">
            <!-- 表格部分 -->
            <div class="bg-white p-4">
              <table class="w-full border-collapse">
                <thead>
                  <tr class="bg-gray-100">
                    <th class="border p-2 text-left">{{ $t('home.statistics.table.header.dataType') }}</th>
                    <th class="border p-2 text-left">{{ $t('home.statistics.table.header.entityCount') }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td class="border p-2">{{ $t('home.statistics.table.rows.syntheticLethalPairs') }}</td>
                    <td class="border p-2">23749</td>
                  </tr>
                  <tr>
                    <td class="border p-2">{{ $t('home.statistics.table.rows.nonsyntheticLethalPairs') }}</td>
                    <td class="border p-2">103613</td>
                  </tr>
                  <tr>
                    <td class="border p-2">{{ $t('home.statistics.table.rows.proteinSequence') }}</td>
                    <td class="border p-2">20504</td>
                  </tr>
                  <tr>
                    <td class="border p-2">{{ $t('home.statistics.table.rows.ppiNodesCount') }}</td>
                    <td class="border p-2">17740</td>
                  </tr>
                  <tr>
                    <td class="border p-2">{{ $t('home.statistics.table.rows.ppiEdgesCount') }}</td>
                    <td class="border p-2">1477610</td>
                  </tr>
                  <tr>
                    <td class="border p-2">{{ $t('home.statistics.table.rows.proteinStructure') }}</td>
                    <td class="border p-2">23391</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import SearchBar from '../components/SearchBar.vue'
import UpdateCard from '../components/UpdateCard.vue'
import StatCard from '../components/StatCard.vue'

// 获取i18n实例
const { t } = useI18n()

// 页面加载状态
const loading = ref(true)

onMounted(() => {
  // 模拟数据加载
  setTimeout(() => {
    loading.value = false
  }, 800)
})
</script>