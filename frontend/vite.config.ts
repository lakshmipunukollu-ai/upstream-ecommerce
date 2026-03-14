import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5009,
    proxy: {
      '/api': 'http://localhost:3009',
      '/health': 'http://localhost:3009',
    },
  },
})
