import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'localhost:8000',
        changeOrigin: true,
      },
    },
    watch: {
      usePolling: true,
    },
  },
})
