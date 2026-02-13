import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Lobby from '../views/Lobby.vue'
import GameRoom from '../views/GameRoom.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/lobby',
    name: 'Lobby',
    component: Lobby
  },
  {
    path: '/room/:id',
    name: 'GameRoom',
    component: GameRoom
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
