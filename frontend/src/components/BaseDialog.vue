<template>
  <!-- 使用 Teleport 将弹窗挂载到 body，避免样式污染 -->
  <Teleport to="body">
    <Transition name="dialog-fade">
      <div v-if="visible" class="dialog-overlay" @click.self="handleOverlayClick">
        <div
          class="dialog-container"
          :style="{
            width: dialogWidth,
            height: dialogHeight,
          }"
        >
          <!-- 内容区域 -->
          <div class="dialog-content">
            <slot name="header">
              <h3 v-if="title" class="dialog-title">{{ title }}</h3>
            </slot>
            <div class="dialog-message">
              {{ message }}
            </div>
            <slot name="footer">
              <div v-if="showButtons" class="dialog-buttons">
                <button class="dialog-btn dialog-btn-cancel" @click="handleCancel">取消</button>
                <button class="dialog-btn dialog-btn-confirm" @click="handleConfirm">确定</button>
              </div>
            </slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'

// --- 响应式数据 ---
const visible = ref(false)
const message = ref('')
const title = ref('')
const dialogWidth = ref('300px')
const dialogHeight = ref('auto')
const showButtons = ref(false)
let durationTimer = null         // 自动关闭定时器
let maxDurationTimer = null      // 最大存活定时器
let pendingResolve = null        // 当前 Promise 的 resolve
let pendingReject = null         // 当前 Promise 的 reject
let isResolved = false           // 防止重复 resolve/reject

// --- 关闭弹窗并清理资源 ---
const close = (result) => {
  if (!visible.value) return

  // 清除所有定时器
  if (durationTimer) clearTimeout(durationTimer)
  if (maxDurationTimer) clearTimeout(maxDurationTimer)
  durationTimer = null
  maxDurationTimer = null

  // 调用 Promise 回调（如果尚未处理）
  if (!isResolved) {
    isResolved = true
    if (result !== undefined && pendingResolve) {
      pendingResolve(result)
    } else if (pendingReject && result === undefined) {
      // 若 result 为 undefined 且我们期望 reject（比如超时未交互），可触发 reject
      // 但为了统一，默认无按钮时 resolve undefined，有按钮且超时未操作则 reject
      if (showButtons.value && !result) {
        pendingReject(new Error('Dialog timeout'))
      } else if (pendingResolve) {
        pendingResolve(result)
      }
    }
  }

  pendingResolve = null
  pendingReject = null
  visible.value = false
}

// --- 用户点击确认 ---
const handleConfirm = () => {
  close('confirm')
}

// --- 用户点击取消 ---
const handleCancel = () => {
  close('cancel')
}

// --- 点击遮罩层关闭（可选，此处默认关闭）---
const handleOverlayClick = () => {
  if (showButtons.value) {
    close('cancel')
  } else {
    close()
  }
}

// --- 对外暴露的 open 方法 ---
const open = (options) => {
  // 防止重复打开
  if (visible.value) {
    // 如果已有弹窗，可选择关闭旧的再打开（简单处理：先关闭）
    close()
  }

  // 合并默认配置
  const {
    message: msg,
    title: ttl = '',
    width = '300px',
    height = 'auto',
    showButtons: btns = false,
    duration = 2000,          // 默认 2 秒自动关闭（无按钮时）
    maxDuration = 0,          // 0 表示不限制
    hasReturnValue = false,   // 是否有返回值（决定 Promise 行为）
  } = options

  // 赋值
  message.value = msg
  title.value = ttl
  dialogWidth.value = width
  dialogHeight.value = height
  showButtons.value = btns
  isResolved = false

  // 清除之前的 Promise 回调
  pendingResolve = null
  pendingReject = null

  // 显示弹窗
  visible.value = true

  // 返回 Promise
  const promise = new Promise((resolve, reject) => {
    pendingResolve = resolve
    pendingReject = reject
  })

  // --- 设置自动关闭定时器（无按钮时）---
  if (!btns && duration > 0) {
    durationTimer = setTimeout(() => {
      close()   // 无返回值时 resolve(undefined)
    }, duration)
  }

  // --- 设置最大存活定时器（有按钮且 maxDuration > 0）---
  if (btns && maxDuration > 0) {
    maxDurationTimer = setTimeout(() => {
      // 超时自动关闭，视为用户取消（或根据需求自定义）
      close('timeout')
    }, maxDuration)
  }

  // 如果 hasReturnValue 为 false，则 Promise 不携带结果（但依然可以等待关闭）
  if (!hasReturnValue) {
    // 对于无返回值场景，我们仍可返回 Promise，但调用者可能不关心结果
    // 这里简单处理：resolve 时传 undefined，但如果有按钮且用户点击，仍会触发 resolve
    // 实际上无返回值意味着调用者不需要等待，所以我们也可以不返回 Promise，
    // 但为了统一接口，我们仍然返回 Promise，并忽略其值。
  }

  return promise
}

// 暴露 open 方法给父组件
defineExpose({ open })
</script>

<style scoped>
/* 遮罩层 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

/* 弹窗容器 */
.dialog-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

/* 内容区域 */
.dialog-content {
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

.dialog-title {
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 1.2rem;
  font-weight: 600;
}

.dialog-message {
  margin-bottom: 20px;
  line-height: 1.5;
}

.dialog-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}

.dialog-btn {
  padding: 6px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.dialog-btn-cancel {
  background-color: #f0f0f0;
  color: #333;
}

.dialog-btn-cancel:hover {
  background-color: #e0e0e0;
}

.dialog-btn-confirm {
  background-color: #1890ff;
  color: white;
}

.dialog-btn-confirm:hover {
  background-color: #40a9ff;
}

/* 过渡动画 */
.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: opacity 0.3s ease;
}

.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;
}

.dialog-fade-enter-to,
.dialog-fade-leave-from {
  opacity: 1;
}
</style>