<template>
  <div class="space-y-8">
    <h1 class="text-3xl font-bold dark:text-white">{{ $t('about.title') }}</h1>
    
    <!-- 简介 -->
    <div class="bg-white dark:bg-neutral-700 rounded-xl shadow-md p-6 transition-colors duration-300">
      <h2 class="text-2xl font-semibold mb-4 dark:text-white">{{ $t('about.sections.whatIs.title') }}</h2>
      <p class="text-gray-700 dark:text-gray-300 mb-4">
        {{ $t('about.description') }}
      </p>
      <p class="text-gray-700 dark:text-gray-300">
        {{ $t('about.sections.whatIs.content') }}
      </p>
    </div>
    

    
    <!-- 团队 -->
    <div class="bg-white dark:bg-neutral-700 rounded-xl shadow-md p-6 transition-colors duration-300">
      <h2 class="text-2xl font-semibold mb-4 dark:text-white">{{ $t('about.sections.ourMission.title') }}</h2>
      <p class="text-gray-700 dark:text-gray-300 mb-4">
        {{ $t('about.sections.ourMission.content') }}
      </p>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
        <div class="flex flex-col items-center">
          
          <h3 class="font-semibold text-lg dark:text-white">{{$t('about.team.mem1.name')}}</h3>
          <p class="text-gray-500 dark:text-gray-400 text-sm mb-2">{{$t('about.team.mem1.role')}}</p>
          <p class="text-gray-600 dark:text-gray-300 text-center text-sm" v-html="$t('about.team.mem1.description')"></p>
        </div>
        
        <div class="flex flex-col items-center">
         
          <h3 class="font-semibold text-lg dark:text-white">{{$t('about.team.mem2.name')}}</h3>
          <p class="text-gray-500 dark:text-gray-400 text-sm mb-2">{{$t('about.team.mem2.role')}}</p>
          <p class="text-gray-600 dark:text-gray-300 text-center text-sm" v-html="$t('about.team.mem2.description')"></p>
        </div>
        
        
      </div>
    </div>
    

    <!-- 联系我们 -->
    <div class="bg-white dark:bg-neutral-700 rounded-xl shadow-md p-6 transition-colors duration-300">
      <h2 class="text-2xl font-semibold mb-4 dark:text-white">{{ $t('about.sections.contact.title') }}</h2>
      <p class="text-gray-700 dark:text-gray-300 mb-4">
        如有任何问题、建议或合作意向，请通过以下方式联系我们：
      </p>
      <div class="flex flex-col md:flex-row gap-6">
        <div>
          <h3 class="font-semibold mb-2 dark:text-white">{{ $t('about.sections.contact.email') }}</h3>
          <p class="text-gray-600 dark:text-gray-300 mb-4">lijunyi@hit.edu.cn</p>
          
          <h3 class="font-semibold mb-2 dark:text-white">{{ $t('about.sections.contact.phone') }}</h3>
          <p class="text-gray-600 dark:text-gray-300">
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