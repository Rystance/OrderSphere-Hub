<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">购物车</h2>

    <div v-if="cart.items.length === 0">
      购物车为空。
    </div>

    <div v-else>
      <div
        v-for="item in cart.items"
        :key="item.id"
        class="p-4 bg-white dark:bg-gray-800 rounded shadow mb-3"
      >
        <div class="flex justify-between">
          <span>{{ item.name }} x {{ item.quantity }}</span>
          <span>¥ {{ item.price * item.quantity }}</span>
        </div>
      </div>

      <p class="text-xl font-bold mt-4">总价：¥ {{ cart.totalPrice }}</p>

      <button class="btn-primary mt-4" @click="submitOrder">
        提交订单
      </button>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '../store/cart'
import { useUserStore } from '../store/user'
import api from '../api'

const cart = useCartStore()
const user = useUserStore()

const submitOrder = async () => {
  if (!user.username) {
    alert('请先登录再提交订单')
    return
  }

  const payload = {
    customer_name: user.username,
    items: cart.items.map(i => ({
      menu_item_id: i.id,
      quantity: i.quantity
    }))
  }

  try {
    const res = await api.post('/orders/submit', payload)
    alert(`订单提交成功，订单号：${res.data.order_id}`)
    cart.clear()
  } catch (e) {
    alert('订单提交失败')
  }
}
</script>

<style scoped>
.btn-primary {
  @apply bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700;
}
</style>
