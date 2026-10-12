import { defineConfig } from 'vite';
export default defineConfig({base:'./',server:{port:5178,strictPort:true},preview:{port:5179,strictPort:true},build:{chunkSizeWarningLimit:1600}});
