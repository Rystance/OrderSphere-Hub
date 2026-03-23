import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: []
  }),

  getters: {
    totalPrice: (state) =>
      state.items.reduce((sum, i) => sum + i.price * i.quantity, 0)
  },

  actions: {
    add(item) {
      const exist = this.items.find(i => i.id === item.id)
      if (exist) exist.quantity++
      else this.items.push({ ...item, quantity: 1 })
    },

    clear() {
      this.items = []
    }
  }
})
