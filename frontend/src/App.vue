<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
    <Layout>
      <RouterView />
    </Layout>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Layout from './components/Layout.vue'
</script>
