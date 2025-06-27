<template>
  <div class="space-y-8">
    <h1 class="text-3xl font-bold">{{ $t('about.title') }}</h1>
    
    <!-- 简介 -->
    <div class="bg-white rounded-xl shadow-md p-6">
      <h2 class="text-2xl font-semibold mb-4">{{ $t('about.sections.whatIs.title') }}</h2>
      <p class="text-gray-700 mb-4">
        {{ $t('about.description') }}
      </p>
      <p class="text-gray-700">
        {{ $t('about.sections.whatIs.content') }}
      </p>
    </div>
    

    
    <!-- 团队 -->
    <div class="bg-white rounded-xl shadow-md p-6">
      <h2 class="text-2xl font-semibold mb-4">{{ $t('about.sections.ourMission.title') }}</h2>
      <p class="text-gray-700 mb-4">
        {{ $t('about.sections.ourMission.content') }}
      </p>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="flex flex-col items-center">
          <div class="w-24 h-24 rounded-full bg-gray-200 mb-4 overflow-hidden">
            <img src="https://picsum.photos/seed/researcher1/200/200" alt="研究人员照片" class="w-full h-full object-cover">
          </div>
          <h3 class="font-semibold text-lg">张明博士</h3>
          <p class="text-gray-500 text-sm mb-2">项目负责人</p>
          <p class="text-gray-600 text-center text-sm">癌症基因组学专家，在合成致死领域有10年研究经验</p>
        </div>
        
        <div class="flex flex-col items-center">
          <div class="w-24 h-24 rounded-full bg-gray-200 mb-4 overflow-hidden">
            <img src="https://picsum.photos/seed/researcher2/200/200" alt="研究人员照片" class="w-full h-full object-cover">
          </div>
          <h3 class="font-semibold text-lg">李华博士</h3>
          <p class="text-gray-500 text-sm mb-2">生物信息学家</p>
          <p class="text-gray-600 text-center text-sm">专注于开发分析合成致死相互作用的算法和工具</p>
        </div>
        
        <div class="flex flex-col items-center">
          <div class="w-24 h-24 rounded-full bg-gray-200 mb-4 overflow-hidden">
            <img src="https://picsum.photos/seed/researcher3/200/200" alt="研究人员照片" class="w-full h-full object-cover">
          </div>
          <h3 class="font-semibold text-lg">王芳博士</h3>
          <p class="text-gray-500 text-sm mb-2">数据管理员</p>
          <p class="text-gray-600 text-center text-sm">负责数据库的维护和更新，确保数据质量和完整性</p>
        </div>
      </div>
    </div>
    

    <!-- 联系我们 -->
    <div class="bg-white rounded-xl shadow-md p-6">
      <h2 class="text-2xl font-semibold mb-4">{{ $t('about.sections.contact.title') }}</h2>
      <p class="text-gray-700 mb-4">
        如有任何问题、建议或合作意向，请通过以下方式联系我们：
      </p>
      <div class="flex flex-col md:flex-row gap-6">
        <div>
          <h3 class="font-semibold mb-2">{{ $t('about.sections.contact.email') }}</h3>
          <p class="text-gray-600 mb-4">lijunyi@hit.edu.cn</p>
          
          <h3 class="font-semibold mb-2">{{ $t('about.sections.contact.phone') }}</h3>
          <p class="text-gray-600">
            计算机科学技术学院<br>
            哈尔滨工业大学 (深圳)<br>
            深圳 广东 518055 
          </p>
        </div>
        
        
      </div>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

// 获取i18n实例
const { t } = useI18n()
</script>