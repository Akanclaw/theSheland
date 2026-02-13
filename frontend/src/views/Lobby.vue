<template>
  <div class="lobby">
    <el-header>
      <h1>游戏大厅</h1>
      <el-button type="primary" @click="showCreateDialog = true">创建房间</el-button>
    </el-header>
    
    <el-main>
      <el-table :data="rooms" style="width: 100%" v-loading="loading">
        <el-table-column prop="name" label="房间名称" />
        <el-table-column prop="player_count" label="当前人数">
          <template #default="{ row }">
            {{ row.player_count }} / {{ row.max_players }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="seed" label="种子" show-overflow-tooltip />
        <el-table-column label="操作">
          <template #default="{ row }">
            <el-button type="success" size="small" @click="joinRoom(row, 'politician')">加入（政客）</el-button>
            <el-button type="warning" size="small" @click="joinRoom(row, 'god')" :disabled="hasGod(row)">加入（上帝）</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-main>

    <el-dialog v-model="showCreateDialog" title="创建房间" width="500px">
      <el-form :model="createForm" label-width="120px">
        <el-form-item label="房间名称">
          <el-input v-model="createForm.name" placeholder="输入房间名称" />
        </el-form-item>
        <el-form-item label="游戏种子">
          <el-input v-model="createForm.seed" placeholder="输入种子（留空自动生成）" />
        </el-form-item>
        <el-form-item label="最大人数">
          <el-input-number v-model="createForm.max_players" :min="2" :max="10" />
        </el-form-item>
        <el-form-item label="回合数">
          <el-input-number v-model="createForm.total_rounds" :min="3" :max="30" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="createRoom">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useGameStore } from '../stores/game'
import type { Room } from '../types/game'

const router = useRouter()
const store = useGameStore()

const rooms = ref<Room[]>([])
const loading = ref(false)
const showCreateDialog = ref(false)
const createForm = ref({
  name: '',
  seed: '',
  max_players: 6,
  total_rounds: 10
})

const statusType = (status: string) => {
  const map: Record<string, string> = { waiting: 'success', playing: 'warning', finished: 'info' }
  return map[status] || 'info'
}

const statusText = (status: string) => {
  const map: Record<string, string> = { waiting: '等待中', playing: '游戏中', finished: '已结束' }
  return map[status] || status
}

const hasGod = (room: Room) => {
  return room.players?.some(p => p.role === 'god')
}

const fetchRooms = async () => {
  loading.value = true
  try {
    rooms.value = await store.fetchPublicRooms()
  } catch (e) {
    // Mock data for demo
    rooms.value = [
      { id: '1', name: '新手房', max_players: 4, player_count: 1, status: 'waiting', seed: 'ABC123', players: [] },
      { id: '2', name: '高手局', max_players: 6, player_count: 3, status: 'waiting', seed: 'XYZ789', players: [] }
    ]
  } finally {
    loading.value = false
  }
}

const createRoom = async () => {
  if (!createForm.value.name) {
    ElMessage.warning('请输入房间名称')
    return
  }
  try {
    const room = await store.createRoom(createForm.value)
    ElMessage.success('创建成功')
    router.push(`/room/${room.id}`)
  } catch (e) {
    ElMessage.error('创建失败')
  }
}

const joinRoom = async (room: Room, role: string) => {
  try {
    await store.joinRoom(room.id, role)
    ElMessage.success('加入成功')
    router.push(`/room/${room.id}`)
  } catch (e) {
    ElMessage.error('加入失败')
  }
}

onMounted(() => {
  fetchRooms()
})
</script>

<style scoped>
.lobby {
  padding: 20px;
}

.el-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
