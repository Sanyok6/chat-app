import { sveltekit } from '@sveltejs/kit/vite';

/** @type {import('vite').UserConfig} */
const config = {
  plugins: [sveltekit()],
  server: {
    proxy: {
      '/api/': {
        // Backend API Proxy
        target: 'http://127.0.0.1:8000/'
      },
      '/api/ws': {
        // Backend API Proxy
        target: 'http://127.0.0.1:8000/',
        ws: true,
      },
      '/static/': {
        // Staticfiles Proxy
        target: 'http://127.0.0.1:8000/'
      }
    }
  }
};

export default config;
