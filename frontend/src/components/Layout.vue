<template>
  <div>
    <Navbar />
    <main class="p-4 sm:p-6">
      <slot />
    </main>
  </div>
</template>

<script setup>
import Navbar from './Navbar.vue'
</script>
