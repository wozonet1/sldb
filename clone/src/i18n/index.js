import { createI18n } from 'vue-i18n'

// 导入语言文件
import zh from './locales/zh.js'
import en from './locales/en.js'

// 创建i18n实例
const i18n = createI18n({
  legacy: false, // 使用组合式API
  locale: localStorage.getItem('language') || 'zh', // 默认语言
  fallbackLocale: 'zh', // 回退语言
  messages: {
    zh,
    en
  }
})

export default i18n