import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    username: null,
    isAdmin: false
  }),

  actions: {
    setUser(username, isAdmin) {
      this.username = username
      this.isAdmin = isAdmin
    },

    logout() {
      this.username = null
      this.isAdmin = false
      localStorage.removeItem('token')
    }
  }
})
