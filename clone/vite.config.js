import path from 'path'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    tailwindcss(),
  ],
  css: ['~/assets/tailwind.css'],
  resolve: {
    extensions: ['.js', '.json', '.vue'], // 确保支持 .vue 文件扩展名
    alias: {
      '@': path.resolve(__dirname, './src'), // 设置 '@' 别名指向 src 目录
    },
  },
})
