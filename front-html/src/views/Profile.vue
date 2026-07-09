<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import RevealOnScroll from '@/components/common/RevealOnScroll.vue'

const userStore = useUserStore()
const router = useRouter()

function handleLogout() {
  userStore.logout()
  ElMessage.success('已退出')
  router.push('/')
}
</script>

<template>
  <div class="profile-page">
    <RevealOnScroll>
      <div class="profile-header glass-card" style="animation: scale-in 0.6s var(--ease-bounce) both">
        <el-avatar :size="72" :icon="'UserFilled'" />
        <h2>{{ userStore.username }}</h2>
        <p>ID: {{ userStore.userId }}</p>
        <el-button type="primary" round @click="router.push('/sandbox')"><el-icon><EditPen /></el-icon> 开始创作</el-button>
      </div>
    </RevealOnScroll>

    <div class="profile-grid">
      <RevealOnScroll v-for="(_, i) in 4" :key="i" :delay="i * 100">
        <div class="pf-card glass-card" :class="{ 'cursor-pointer': i === 0 }" @click="i === 0 ? router.push('/gallery') : undefined">
          <el-icon :size="32" :color="['var(--accent-purple)','var(--accent-orange)','var(--accent-cyan)','var(--accent-green)'][i]">
            <component :is="['PictureFilled','Star','Connection','Clock'][i]" />
          </el-icon>
          <h4>{{ ['我的作品','我的收藏','我的 Fork','浏览历史'][i] }}</h4>
          <span class="count">0</span>
        </div>
      </RevealOnScroll>
    </div>

    <RevealOnScroll :delay="400">
      <div class="pf-settings glass-card">
        <h4>账号设置</h4>
        <el-button type="danger" plain round @click="handleLogout">退出登录</el-button>
      </div>
    </RevealOnScroll>
  </div>
</template>

<style scoped>
.profile-page { max-width: 680px; margin: 0 auto; padding: var(--space-xl); }
.profile-header { text-align: center; padding: var(--space-2xl); margin-bottom: var(--space-xl); }
.profile-header h2 { margin: var(--space-md) 0 var(--space-xs); font-size: 1.3rem; font-weight: 700; color: var(--text-primary); }
.profile-header p { color: var(--text-tertiary); font-size: 0.85rem; margin-bottom: var(--space-lg); }
.profile-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-md); margin-bottom: var(--space-xl); }
.pf-card { text-align: center; padding: var(--space-lg); cursor: pointer; }
.pf-card h4 { font-size: 0.85rem; color: var(--text-secondary); margin: var(--space-sm) 0; }
.count { font-size: 1.8rem; font-weight: 800; color: var(--text-primary); }
.pf-settings { padding: var(--space-xl); }
.pf-settings h4 { font-size: 1rem; font-weight: 700; color: var(--text-primary); margin-bottom: var(--space-lg); }

@media (max-width: 480px) { .profile-grid { grid-template-columns: repeat(2, 1fr); } }
</style>
