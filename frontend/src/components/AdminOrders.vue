<template>
  <div>
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-lg font-bold">订单管理</h2>
    </div>

    <table class="w-full text-sm border">
      <thead class="bg-gray-100">
        <tr>
          <th class="border px-2 py-1">ID</th>
          <th class="border px-2 py-1">客户名</th>
          <th class="border px-2 py-1">明细</th>
          <th class="border px-2 py-1">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.id">
          <td class="border px-2 py-1">{{ order.id }}</td>
          <td class="border px-2 py-1">{{ order.customer_name }}</td>
          <td class="border px-2 py-1">
            <ul>
              <li v-for="item in order.items" :key="item.id">
                菜品ID: {{ item.menu_item_id }} × {{ item.quantity }}
              </li>
            </ul>
          </td>
          <td class="border px-2 py-1">
            <button
              class="px-2 py-1 text-xs bg-red-500 text-white rounded"
              @click="remove(order.id)"
            >
              删除
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="error" class="text-red-500 text-xs mt-2">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  token: { type: String, required: true }
})

const orders = ref([])
const error = ref('')

const fetchOrders = async () => {
  error.value = ''
  const res = await fetch('http://127.0.0.1:8000/admin/orders/', {
    headers: {
      Authorization: `Bearer ${props.token}`
    }
  })
  if (res.ok) {
    orders.value = await res.json()
  } else {
    error.value = '获取订单失败'
  }
}

const remove = async (id) => {
  if (!confirm('确认删除该订单？')) return
  const res = await fetch(`http://127.0.0.1:8000/admin/orders/${id}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${props.token}`
    }
  })
  if (res.ok) {
    fetchOrders()
  } else {
    error.value = '删除失败'
  }
}

onMounted(fetchOrders)
watch(() => props.token, () => {
  if (props.token) fetchOrders()
})
</script>
