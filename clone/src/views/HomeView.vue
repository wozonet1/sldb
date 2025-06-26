<template>
  <div class="space-y-8">
    <!-- 英雄区域 -->
  <section class="bg-gradient-to-r from-blue-900 to-indigo-800 text-white py-20" style="background-image: url('./src/assets/bg-pattern.jpg'); background-size: cover; background-repeat: no-repeat; background-position: center;">
    <div class="max-w-7xl mx-auto px-4">
      <div class="text-center mb-8">
        <h1 class="text-5xl md:text-6xl font-bold mb-6">
          Welcome to Struct2SL
        </h1>
        <p class="text-xl md:text-2xl mb-10">
          Discover synthetic lethality pairs and gain deeper insights into genetic interactions.
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
      <StatCard value="12,543" label="基因对" />
      <StatCard value="5,678" label="实验" />
      <StatCard value="3,210" label="癌症类型" />
      <StatCard value="890" label="出版物" />
    </section>
    
    <!-- 最近更新 -->
    <section class="px-4">
      <h2 class="text-2xl font-bold mb-6">最近更新</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <UpdateCard>
          <template #icon>
            <i class="fa fa-flask"></i>
          </template>
          <template #title>新增乳腺癌相关基因对</template>
          <template #content>我们新增了342个与乳腺癌相关的合成致死基因对，为乳腺癌治疗提供了新的潜在靶点。</template>
          <template #date>更新于 2025-06-15</template>
        </UpdateCard>
        
        <!-- 可以轻松添加更多更新卡片 -->
        <UpdateCard>
          <template #icon>
            <i class="fa fa-code"></i>
          </template>
          <template #title>网站界面优化</template>
          <template #content>我们对网站进行了界面优化，提升了用户体验和搜索功能，使数据检索更加便捷。</template>
          <template #date>更新于 2025-06-01</template>
        </UpdateCard>
      </div>
    </section>
    
   <!-- About Struct2SL 部分 -->
    <section class="px-4 py-12 bg-gray-50">
      <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 md:items-start">
        <div>
          <h2 class="text-3xl font-bold mb-6">About Struct2SL</h2>
          <p class="text-gray-700 mb-5 text-xl leading-relaxed" style="max-width: 500px;">
            Struct2SL is a synthetic lethal gene pair prediction model,
            providing valuable references for cancer research and drug
            development. Our system leverages advanced algorithms and
            comprehensive data sources to identify potential gene
            interactions that could lead to new therapeutic strategies. For
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
        <h2 class="text-3xl font-bold mb-6">Statistics of Struct2SL</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 md:items-start">
          <div>
            <p class="text-gray-700 mb-4 text-xl leading-relaxed" style="max-width: 500px;">
              Struct2SL uses the latest research data from SynLethDB
              (human synthetic lethal gene pairs and non-synthetic lethal
              gene pairs) to predict potential gene pairs. The current version
              covers 15794 human genes, and the results presented are
              computational prediction results.
            </p>
          </div>
          <div class="rounded-lg overflow-hidden shadow-lg">
            <!-- 表格部分 -->
            <div class="bg-white p-4">
              <table class="w-full border-collapse">
                <thead>
                  <tr class="bg-gray-100">
                    <th class="border p-2 text-left">Types of data</th>
                    <th class="border p-2 text-left">Number of entities</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td class="border p-2">Synthetic lethal gene pairs</td>
                    <td class="border p-2">23749</td>
                  </tr>
                  <tr>
                    <td class="border p-2">Nonsynthetic lethal gene pairs</td>
                    <td class="border p-2">103613</td>
                  </tr>
                  <tr>
                    <td class="border p-2">Protein sequence</td>
                    <td class="border p-2">20504</td>
                  </tr>
                  <tr>
                    <td class="border p-2">Protein-Protein Interaction Networks (nodes)</td>
                    <td class="border p-2">17740</td>
                  </tr>
                  <tr>
                    <td class="border p-2">Protein-Protein Interaction Networks (edges)</td>
                    <td class="border p-2">1477610</td>
                  </tr>
                  <tr>
                    <td class="border p-2">Protein spatial structure</td>
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
import SearchBar from '../components/SearchBar.vue'
import UpdateCard from '../components/UpdateCard.vue'
import StatCard from '../components/StatCard.vue'

// 页面加载状态
const loading = ref(true)

onMounted(() => {
  // 模拟数据加载
  setTimeout(() => {
    loading.value = false
  }, 800)
})
</script>