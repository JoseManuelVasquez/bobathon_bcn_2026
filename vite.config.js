import { defineConfig } from 'vite';
export default defineConfig({
  base: './',
  build: { outDir: 'docs', emptyOutDir: true, chunkSizeWarningLimit: 1400 },
  server: { port: 4186, strictPort: true },
  preview: { port: 4186, strictPort: true },
});
