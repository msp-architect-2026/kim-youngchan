import { create } from 'zustand'

export const useAuthStore = create((set) => ({
  token: localStorage.getItem('dropx_token') || null,
  user: null,
  setToken: (token) => {
    localStorage.setItem('dropx_token', token)
    set({ token })
  },
  setUser: (user) => set({ user }),
  logout: () => {
    localStorage.removeItem('dropx_token')
    set({ token: null, user: null })
  }
}))
