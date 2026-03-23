<template>
  <div
    class="p-4 bg-white dark:bg-gray-800 rounded shadow transition transform hover:scale-[1.02] hover:shadow-lg flex flex-col"
  >
    <div class="flex items-center mb-3 space-x-3">
      <img
        v-if="item.image_url"
        :src="`http://127.0.0.1:8000${item.image_url}`"
        alt="菜品图片"
        class="w-16 h-16 rounded object-cover"
      />
      <div>
        <h3 class="text-lg font-bold">{{ item.name }}</h3>
        <p class="text-xs text-gray-500 dark:text-gray-400">{{ item.category }} · {{ item.type }}</p>
      </div>
    </div>

    <p class="text-sm text-gray-700 dark:text-gray-200 flex-1">
      {{ item.description || '这道菜还没有描述。' }}
    </p>

    <div class="mt-3 flex items-center justify-between">
      <span class="text-lg font-bold text-green-600 dark:text-green-400">¥ {{ item.price }}</span>
      <button @click="$emit('add', item)" class="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700">
        加入购物车
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true
  }
})
defineEmits(['add'])
</script>
