import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    username: null,
    isAdmin: false,
    avatar: null,
    email: null
  }),

  actions: {
    setUser(username, isAdmin, avatar = null, email = null) {
      this.username = username
      this.isAdmin = isAdmin
      this.avatar = avatar
      this.email = email
    },

    setAvatar(avatarUrl) {
      this.avatar = avatarUrl
    },

    logout() {
      this.username = null
      this.isAdmin = false
      this.avatar = null
      this.email = null
      localStorage.removeItem('token')
    }
  }
})