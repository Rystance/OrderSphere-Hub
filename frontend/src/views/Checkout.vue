<template>
  <div class="p-6 max-w-2xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">购物车</h1>

    <div v-if="cart.items.length === 0" class="text-gray-600">
      购物车为空。
    </div>

    <div v-else class="space-y-4">

      <!-- 每个料理卡片 -->
      <div
        v-for="item in cart.items"
        :key="item.id"
        class="flex items-center bg-white rounded shadow p-3 space-x-4"
      >

        <!-- ⭐ 左侧小图标 -->
        <img
          :src="`http://127.0.0.1:8000${item.image_url}`"
          alt=""
          class="w-16 h-16 object-cover rounded"
        />

        <!-- 右侧信息 -->
        <div class="flex-1 flex justify-between items-center">

          <!-- 名称 + 价格 -->
          <div>
            <p class="font-semibold">{{ item.name }}</p>
            <p class="text-gray-600">￥{{ item.price }}</p>
          </div>

          <!-- 数量编辑 + 删除 -->
          <div class="flex items-center space-x-3">

            <button
              @click="cart.decrease(item)"
              class="px-2 py-1 bg-gray-300 rounded"
            >
              -
            </button>

            <span class="font-semibold">{{ item.quantity }}</span>

            <button
              @click="cart.increase(item)"
              class="px-2 py-1 bg-gray-300 rounded"
            >
              +
            </button>

            <button
              @click="cart.remove(item)"
              class="text-red-500 ml-4"
            >
              删除
            </button>

          </div>
        </div>
      </div>

      <!-- 总价 -->
      <div class="text-right text-xl font-bold mt-4">
        总价：￥{{ cart.totalPrice }}
      </div>

      <!-- 提交订单 -->
      <button
        @click="submitOrder"
        class="w-full mt-4 py-2 bg-green-600 text-white rounded"
      >
        提交订单
      </button>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '../store/cart'
import {useUserStore} from '../store/user'

const cart = useCartStore()
const user = useUserStore()

const submitOrder = async () => {
  if (cart.items.length === 0) {
    alert('购物车为空')
    return
  }

  const username = user.username
  const token = localStorage.getItem('token')

  // ⭐ 未登录：只提示，不跳转
  if (!username || !token) {
    alert('请先登录后再提交订单')
    return
  }

  // ⭐ 已登录 → 正常提交
  const payload = {
    customer_name: username,
    items: cart.items.map(i => ({
      menu_item_id: i.id,
      quantity: i.quantity
    }))
  }

  const res = await fetch('http://127.0.0.1:8000/orders/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })

  if (!res.ok) {
    alert('提交订单失败')
    return
  }

  alert('订单提交成功')
  cart.clear()
}
</script>
