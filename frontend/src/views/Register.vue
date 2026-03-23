<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="w-full max-w-md bg-white rounded shadow p-6">
      <h2 class="text-2xl font-bold mb-4 text-center">注册</h2>

      <form @submit.prevent="onSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">用户名</label>
          <input
            v-model="form.username"
            type="text"
            class="w-full border rounded px-3 py-2"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">密码</label>
          <input
            v-model="form.password"
            type="password"
            class="w-full border rounded px-3 py-2"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">确认密码</label>
          <input
            v-model="form.confirm_password"
            type="password"
            class="w-full border rounded px-3 py-2"
            required
          />
          <p v-if="passwordMismatch" class="text-red-500 text-xs mt-1">
            两次输入的密码不一致
          </p>
        </div>

        <div class="flex items-center justify-between">
          <button
            type="submit"
            class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            注册
          </button>
          <router-link to="/login" class="text-sm text-blue-600 hover:underline">
            已有账号？去登录
          </router-link>
        </div>

        <p v-if="error" class="text-red-500 text-sm mt-2">{{ error }}</p>
        <p v-if="success" class="text-green-600 text-sm mt-2">{{ success }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const form = ref({
  username: '',
  password: '',
  confirm_password: ''
})

const error = ref('')
const success = ref('')

const passwordMismatch = computed(
  () => form.value.password && form.value.confirm_password && form.value.password !== form.value.confirm_password
)

const onSubmit = async () => {
  error.value = ''
  success.value = ''

  if (passwordMismatch.value) {
    error.value = '两次输入的密码不一致'
    return
  }

  try {
    const res = await fetch('http://127.0.0.1:8000/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })

    if (!res.ok) {
      const data = await res.json()
      error.value = data.detail || '注册失败'
      return
    }

    success.value = '注册成功，请前往登录'
  } catch (e) {
    error.value = '网络错误'
  }
}
</script>
