import { defineStore } from 'pinia'
import api from '../api/axios'
import type { Room, Player } from '../types/game'

export const useGameStore = defineStore('game', {
  state: () => ({
    currentRoom: null as Room | null,
    currentPlayer: null as Player | null,
    rooms: [] as Room[],
    isLoading: false
  }),

  actions: {
    async fetchPublicRooms() {
      this.isLoading = true
      try {
        const response = await api.get('/rooms/public/')
        return response.data
      } catch (error) {
        console.error('获取房间列表失败:', error)
        return []
      } finally {
        this.isLoading = false
      }
    },

    async createRoom(data: any) {
      try {
        const response = await api.post('/rooms/', data)
        return response.data
      } catch (error) {
        console.error('创建房间失败:', error)
        throw error
      }
    },

    async joinRoom(roomId: string, role: string) {
      try {
        const response = await api.post(`/rooms/${roomId}/join/`, { role })
        this.currentPlayer = response.data
        return response.data
      } catch (error) {
        console.error('加入房间失败:', error)
        throw error
      }
    },

    async fetchRoom(roomId: string) {
      try {
        const response = await api.get(`/rooms/${roomId}/`)
        this.currentRoom = response.data
        return response.data
      } catch (error) {
        console.error('获取房间信息失败:', error)
        throw error
      }
    },

    async leaveRoom(roomId: string) {
      try {
        await api.post(`/rooms/${roomId}/leave/`)
        this.currentRoom = null
        this.currentPlayer = null
      } catch (error) {
        console.error('离开房间失败:', error)
        throw error
      }
    },

    async ready(roomId: string) {
      try {
        const response = await api.post(`/rooms/${roomId}/ready/`)
        return response.data
      } catch (error) {
        console.error('准备失败:', error)
        throw error
      }
    },

    async startGame(roomId: string) {
      try {
        const response = await api.post(`/rooms/${roomId}/start/`)
        return response.data
      } catch (error) {
        console.error('开始游戏失败:', error)
        throw error
      }
    }
  }
})