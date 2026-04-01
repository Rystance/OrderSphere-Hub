<template>
  <Teleport to="body">
    <Transition name="dialog-show">
      <div
        v-if="visible"
        class="dialog-overlay"
        :class="[ overlay ? 'dialog-overlay-dark' : 'no-overlay', `position-${position}` ]"
        @click.self="handleOverlayClick"
      >
        <div
            class="dialog-container"
            :style="containerStyle"
            role="dialog"
            aria-modal="true"
            :aria-label="title || 'dialog'"
            tabindex="0"
            ref="containerRef"
        >
          <div class="dialog-content">
            <slot name="header">
              <h3
                  v-if="title"
                  class="dialog-title"
                  :style="{ textAlign: titleAlign, font: titleFont, color: titleColor }"
              >
                {{ title }}
              </h3>
            </slot>
            <div
                class="dialog-message"
                :style="{ textAlign: messageAlign, font: messageFont, color: messageColor }"
            >
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
import {ref, computed, nextTick, watch, onBeforeUnmount} from 'vue'

const visible = ref(false)
const message = ref('')
const title = ref('')
const dialogWidth = ref('')
const dialogHeight = ref('')
const showButtons = ref(false)
const position = ref('center')
const overlay = ref(true)

const titleAlign = ref('left')
const messageAlign = ref('left')
const titleFont = ref('')
const titleColor = ref('')
const messageFont = ref('')
const messageColor = ref('')
const closeOnClickOverlay = ref(true)

let onConfirmCallback = null
let onCancelCallback = null

let durationTimer = null
let maxDurationTimer = null
let resolvePromise = null

const containerRef = ref(null)
let prevActiveElement = null

const containerStyle = computed(() => {
  const style = {}
  if (dialogWidth.value) style.width = dialogWidth.value
  if (dialogHeight.value) style.height = dialogHeight.value
  return style
})

const clearTimers = () => {
  if (durationTimer) {
    clearTimeout(durationTimer);
    durationTimer = null
  }
  if (maxDurationTimer) {
    clearTimeout(maxDurationTimer);
    maxDurationTimer = null
  }
}

const close = (action = 'close') => {
  if (!visible.value) return
  clearTimers()
  visible.value = false

  // restore focus
  if (prevActiveElement && prevActiveElement.focus) {
    prevActiveElement.focus()
  }
  prevActiveElement = null

  // resolve promise with consistent shape
  if (resolvePromise) {
    resolvePromise({
      action,
      title: title.value,
      message: message.value,
      showButtons: showButtons.value
    })
    resolvePromise = null
  }

  // clear callbacks
  onConfirmCallback = null
  onCancelCallback = null
}

const handleConfirm = () => {
  if (typeof onConfirmCallback === 'function') {
    try {
      onConfirmCallback({message: message.value, title: title.value})
    } catch (e) { /* ignore */
    }
  }
  close('confirm')
}

const handleCancel = () => {
  if (typeof onCancelCallback === 'function') {
    try {
      onCancelCallback({message: message.value, title: title.value})
    } catch (e) { /* ignore */
    }
  }
  close('cancel')
}

const handleOverlayClick = () => {
  if (!closeOnClickOverlay.value) return
  if (showButtons.value) close('cancel')
  else close('close')
}

const onKeydown = (e) => {
  if (!visible.value) return
  if (e.key === 'Escape' || e.key === 'Esc') {
    e.preventDefault()
    if (showButtons.value) close('cancel')
    else close('close')
  }
}

watch(visible, async (val) => {
  if (val) {
    prevActiveElement = document.activeElement
    await nextTick()
    // focus the container for accessibility
    try {
      containerRef.value && containerRef.value.focus()
    } catch (e) {
    }
    window.addEventListener('keydown', onKeydown)
  } else {
    window.removeEventListener('keydown', onKeydown)
  }
})

onBeforeUnmount(() => {
  clearTimers()
  window.removeEventListener('keydown', onKeydown)
})

const open = (options = {}) => {
  // default options
  const {
    message: msg = '',
    title: ttl = '',
    width = '',
    height = '',
    showButtons: btns = false,
    duration = 2000,
    maxDuration = 0,
    position: pos = 'center',
    overlay: ov = true,
    titleAlign: tAlign = 'left',
    messageAlign: mAlign = 'left',
    titleFont: tFont = '',
    titleColor: tColor = '',
    messageFont: mFont = '',
    messageColor: mColor = '',
    closeOnClickOverlay: cOverlay = undefined,
    onConfirm = null,
    onCancel = null
  } = options

  message.value = msg
  title.value = ttl
  dialogWidth.value = width
  dialogHeight.value = height
  showButtons.value = !!btns
  position.value = pos
  overlay.value = !!ov
  titleAlign.value = tAlign
  messageAlign.value = mAlign
  titleFont.value = tFont
  titleColor.value = tColor
  messageFont.value = mFont
  messageColor.value = mColor

  closeOnClickOverlay.value = (cOverlay !== undefined) ? !!cOverlay : !!ov

  onConfirmCallback = onConfirm
  onCancelCallback = onCancel

  clearTimers()
  resolvePromise = null

  visible.value = true

  // return a promise that always resolves with an object describing the action
  const promise = new Promise((resolve) => {
    resolvePromise = resolve
  })

  if (!showButtons.value && duration > 0) {
    durationTimer = setTimeout(() => close('close'), duration)
  }

  if (showButtons.value && maxDuration > 0) {
    maxDurationTimer = setTimeout(() => close('timeout'), maxDuration)
  }

  return promise
}

defineExpose({open})
</script>

<style scoped>
/* 保留原样式，略微修正注释 */
/* 过渡动画（淡入淡出 + 缩放） */
.dialog-show-enter-active,
.dialog-show-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.dialog-show-enter-from,
.dialog-show-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.dialog-show-enter-to,
.dialog-show-leave-from {
  opacity: 1;
  transform: scale(1);
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  z-index: 1000;
}

.dialog-overlay-dark {
  background-color: rgba(0, 0, 0, 0.5);
}

.no-overlay {
  background-color: transparent;
  pointer-events: none;
}

/* 位置预设 */
.position-center {
  align-items: center;
  justify-content: center;
}

.position-top {
  align-items: flex-start;
  justify-content: center;
  padding-top: 20px;
}

.position-bottom {
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 20px;
}

.position-left {
  align-items: center;
  justify-content: flex-start;
  padding-left: 20px;
}

.position-right {
  align-items: center;
  justify-content: flex-end;
  padding-right: 20px;
}

.position-top-left {
  align-items: flex-start;
  justify-content: flex-start;
  padding: 20px;
}

.position-top-right {
  align-items: flex-start;
  justify-content: flex-end;
  padding: 20px;
}

.position-bottom-left {
  align-items: flex-end;
  justify-content: flex-start;
  padding: 20px;
}

.position-bottom-right {
  align-items: flex-end;
  justify-content: flex-end;
  padding: 20px;
}

.dialog-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  width: auto;
  min-width: 200px;
  max-width: 60vw;
  height: auto;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  pointer-events: auto;
}

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
  color: #1f2937;
}

.dialog-message {
  margin-bottom: 20px;
  line-height: 1.5;
  color: #374151;
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

/* 夜间模式 */
.dark .dialog-container {
  background: #1f2937;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.5);
}

.dark .dialog-title {
  color: #f3f4f6;
}

.dark .dialog-message {
  color: #d1d5db;
}

.dark .dialog-btn-cancel {
  background-color: #374151;
  color: #e5e7eb;
}

.dark .dialog-btn-cancel:hover {
  background-color: #4b5563;
}

.dark .dialog-btn-confirm {
  background-color: #3b82f6;
}

.dark .dialog-btn-confirm:hover {
  background-color: #60a5fa;
}
</style>