<template>
  <footer class="bg-primary dark:bg-primary-dark shadow-md text-white py-12 transition-colors duration-300">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- 关于我们 -->
        <div>
          <h3 class="text-lg font-semibold mb-4">{{ t('footer.about.title') }}</h3>
          <p class="text-gray-400 dark:text-gray-300">{{ t('footer.about.description') }}</p>
        </div>
        
        <!-- 快速链接 -->
        <div>
          <h3 class="text-lg font-semibold mb-4">{{ t('footer.quickLinks.title') }}</h3>
          <ul class="space-y-2">
            <li><a href="/" class="text-gray-400 dark:text-gray-300 hover:text-white transition-colors">{{ t('header.home') }}</a></li>
            <li><a href="/search" class="text-gray-400 dark:text-gray-300 hover:text-white transition-colors">{{ t('header.search') }}</a></li>
            <li><a href="about" class="text-gray-400 dark:text-gray-300 hover:text-white transition-colors">{{ t('header.about') }}</a></li>
          </ul>
        </div>
        
        <!-- 资源 -->
        <div>
          <h3 class="text-lg font-semibold mb-4">{{ t('footer.resources.title') }}</h3>
          <ul class="space-y-2">
            <li><a href="#" class="text-gray-400 dark:text-gray-300 hover:text-white transition-colors">{{ t('footer.resources.apiDocs') }}</a></li>
            <li><a href="#" class="text-gray-400 dark:text-gray-300 hover:text-white transition-colors">{{ t('footer.resources.tutorials') }}</a></li>
            <li><a href="#" class="text-gray-400 dark:text-gray-300 hover:text-white transition-colors">{{ t('footer.resources.download') }}</a></li>
            <li><a href="#" class="text-gray-400 dark:text-gray-300 hover:text-white transition-colors">{{ t('footer.resources.faq') }}</a></li>
          </ul>
        </div>
        
        <!-- 联系我们 -->
        <div>
          <h3 class="text-lg font-semibold mb-4">{{ t('footer.contact.title') }}</h3>
          <ul class="space-y-2">
            <li class="flex items-center text-gray-400 dark:text-gray-300">
              <i class="fa fa-envelope-o mr-2"></i>
              <a href="mailto:lijunyi@hit.edu.cn" class="hover:text-white transition-colors">lijunyi@hit.edu.cn</a>
            </li>
            <li class="flex items-center text-gray-400 dark:text-gray-300">
              <i class="fa fa-phone mr-2"></i>
              <span>+1 (123) 456-7890</span>
            </li>
          </ul>
        </div>
      </div>

      <div class="border-t border-gray-700 dark:border-gray-600 mt-8 pt-8 text-center text-gray-500 dark:text-gray-400">
        <p>&copy; 2025 Struct2SL. {{ t('footer.copyright') }}</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

// 获取i18n实例
const { t } = useI18n()
</script>