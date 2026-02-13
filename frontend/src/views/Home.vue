<template>
  <div class="home">
    <div class="hero">
      <h1>🇨🇳 请遵守中华人民共和国法律和国家领土主权完整</h1>
      <h2>The Sheland</h2>
      <p class="subtitle">一个多人在线伪桌游</p>
      <p class="description">扮演政客竞选选票，或化身上帝掌控全局</p>
      <el-button type="primary" size="large" @click="goToLobby">开始游戏</el-button>
    </div>
    <div class="features">
      <div class="feature">
        <h3>🎭 成为政客</h3>
        <p>在地图上竞选，争取选票，制定政策</p>
      </div>
      <div class="feature">
        <h3>👑 成为上帝</h3>
        <p>干预选举，修改地图，影响文化</p>
      </div>
      <div class="feature">
        <h3>🗺️ 随机世界</h3>
        <p>相同种子生成相同的地图和参数</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToLobby = () => {
  router.push('/lobby')
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.hero {
  text-align: center;
  margin-bottom: 60px;
}

.hero h1 {
  font-size: 14px;
  color: #ffd700;
  margin-bottom: 20px;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.hero h2 {
  font-size: 64px;
  margin-bottom: 20px;
  text-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.subtitle {
  font-size: 24px;
  margin-bottom: 10px;
  opacity: 0.9;
}

.description {
  font-size: 18px;
  margin-bottom: 30px;
  opacity: 0.8;
}

.features {
  display: flex;
  gap: 40px;
  flex-wrap: wrap;
  justify-content: center;
  max-width: 1200px;
}

.feature {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 30px;
  width: 280px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.feature h3 {
  font-size: 24px;
  margin-bottom: 15px;
}

.feature p {
  font-size: 16px;
  opacity: 0.9;
}
</style>
