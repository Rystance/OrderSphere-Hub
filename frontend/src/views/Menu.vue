<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">菜单</h2>

    <div v-if="loading" class="text-center py-10">
      正在加载菜单...
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <MenuItemCard
        v-for="item in menu"
        :key="item.id"
        :item="item"
        @add="addToCart"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import MenuItemCard from '../components/MenuItemCard.vue'
import { useCartStore } from '../store/cart'

const menu = ref([])
const loading = ref(true)
const cart = useCartStore()

onMounted(async () => {
  try {
    const res = await api.get('/menu/')
    menu.value = res.data
  } finally {
    loading.value = false
  }
})

const addToCart = (item) => {
  cart.add(item)
}
</script>
