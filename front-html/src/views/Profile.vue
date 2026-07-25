<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import RevealOnScroll from '@/components/common/RevealOnScroll.vue'
import { videosApi } from '@/api/videos'
import AvatarIcon from '@/components/common/AvatarIcon.vue'
import CountNumber from '@/components/common/CountNumber.vue'
import { useCurrentUser } from '@/composables/useCurrentUser'

const PY_BASE = import.meta.env.VITE_PYTHON_BASE ?? ''

const userStore = useUserStore()
const router = useRouter()
const { username, avatar: avatarUrl, displayName, token, userKey, refresh } = useCurrentUser()

const myWorksCount = ref(0)
const myStarsCount = ref(0)
// 合集贡献：统计学习路径中已完成的知识点数量
const collectionContribCount = computed(() => {
  try {
    const u = username.value || 'anon'
    const learned = JSON.parse(localStorage.getItem(`cs:learn:${u}`) || '{}')
    return Object.values(learned).filter(Boolean).length
  } catch { return 0 }
})

const statCards = computed(() => [
  { icon: 'PictureFilled', color: '#7c3aed', label: '我的作品', count: javaWorkCount.value || serverWorksCount.value || myWorksCount.value || 0, click: () => router.push('/gallery?tab=my-works') },
  { icon: 'Star', color: '#f59e0b', label: '我的收藏', count: myStarsCount.value, click: () => router.push('/gallery?tab=stars') },
  { icon: 'Collection', color: '#06b6d4', label: '词条贡献', count: 0, click: () => router.push('/wiki') },
  { icon: 'Guide', color: '#10b981', label: '合集贡献', count: collectionContribCount.value, click: () => router.push('/study') },
  { icon: 'Clock', color: '#ec4899', label: '模板贡献', count: 0, click: () => router.push('/templates') },
])

const editingNickname = ref(false)
const editingBio = ref(false)
const nickname = ref(displayName.value)
const bio = ref(localStorage.getItem(userStore.username ? userKey('bio') : '') || '')

async function saveBio() {
  const text = bio.value.trim()
  localStorage.setItem(userKey('bio'), text)
  editingBio.value = false
  ElMessage.success('简介已更新')
  const ok = await syncProfileToBackend({ intro: text })
  if (!ok) ElMessage.warning('简介已本地保存，但同步到服务器失败')
}

async function syncProfileToBackend(fields: Record<string, string>, retries = 2): Promise<boolean> {
  if (!token.value) return false
  const params = new URLSearchParams(fields).toString()
  for (let i = 0; i <= retries; i++) {
    try {
      const res = await fetch(`/api/v1/user/profile/update?${params}`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${token.value}` },
      })
      if (res.ok) return true
    } catch { /* retry */ }
    if (i < retries) await new Promise(r => setTimeout(r, 500))
  }
  return false
}

async function saveNickname() {
  const name = nickname.value.trim()
  if (!name) return
  localStorage.setItem(userKey('nickname'), name)
  // 同步更新 login 时的 username（AppHeader 等组件 fallback 时会用到）
  localStorage.setItem('username', name)
  refresh() // 通知 composable 重新读取 localStorage
  editingNickname.value = false
  ElMessage.success('昵称已更新')
  // 异步同步到 Java 后端
  const ok = await syncProfileToBackend({ nickname: name })
  if (!ok) {
    ElMessage.warning('昵称已本地保存，但同步到服务器失败，重启后社区可能显示旧名字')
  }
}

function getMyWorksCount(): number {
  try {
    const u = username.value || 'anon'
    const works = JSON.parse(localStorage.getItem(`cs:my-works:${u}`) || '[]')
    return works.length
  } catch { return 0 }
}

// 从服务端加载我的作品数量（跨设备同步）
const serverWorksCount = ref(0)
async function loadServerWorksCount() {
  const name = username.value
  if (!name) return
  try {
    const r = await fetch(`/api/videos/list?my_works=true&username=${encodeURIComponent(name)}`)
    const d = await r.json()
    serverWorksCount.value = d.data?.total || 0
  } catch { /* ignore */ }
}

// 从 Java 后端加载作品总数（包含所有状态：草稿/发布/公开/私有）
const javaWorkCount = ref(0)
async function loadJavaWorkCount() {
  if (!token.value) return
  try {
    const res = await fetch('/api/v1/user/home/data', {
      headers: { 'Authorization': `Bearer ${token.value}` },
    })
    const data = await res.json()
    if (data.code === 200 && data.data?.workCount != null) {
      javaWorkCount.value = data.data.workCount
    }
  } catch { /* ignore */ }
}

// 同步 localStorage 的作品到服务端
async function syncWorksToServer() {
  const name = username.value
  if (!name) return
  try {
    const works = JSON.parse(localStorage.getItem(`cs:my-works:${name}`) || '[]')
    if (works.length > 0) {
      await videosApi.syncMyWorks(name, works)
      await loadServerWorksCount()
    }
  } catch { /* ignore */ }
}

// 自动将 localStorage 中已有的头像和昵称同步到 Java 后端
async function syncExistingProfileToBackend() {
  const fields: Record<string, string> = {}
  if (avatarUrl.value) fields.avatar = avatarUrl.value
  if (displayName.value) fields.nickname = displayName.value
  if (Object.keys(fields).length > 0) {
    await syncProfileToBackend(fields)
  }
}

async function loadStarsCount() {
  try {
    const res = await videosApi.getList(true, userStore.username)
    myStarsCount.value = res.data.data?.total || 0
  } catch { /* ignore */ }
}

async function handleAvatarUpload(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  if (file.size > 2 * 1024 * 1024) { ElMessage.warning('头像不能超过 2MB'); return }
  const form = new FormData()
  form.append('file', file)
  try {
    const res = await fetch(`${PY_BASE}/api/user/avatar`, { method: 'POST', body: form })
    const data = await res.json()
    if (data.code === 0 && data.data?.url) {
      const fullUrl = `${PY_BASE}${data.data.url}`
      localStorage.setItem(userKey('avatar'), fullUrl)
      refresh() // 通知 composable 重新读取 localStorage
      ElMessage.success('头像已更新')
      // 同步头像 URL 到 Java 后端数据库
      const ok = await syncProfileToBackend({ avatar: fullUrl })
      if (!ok) {
        ElMessage.warning('头像已本地保存，但同步到服务器失败，其他用户可能看不到新头像')
      }
    } else {
      ElMessage.error(data.message || '上传失败')
    }
  } catch { ElMessage.error('上传失败，请检查网络') }
}

function handleLogout() {
  userStore.logout()
  ElMessage.success('已退出')
  router.push('/')
}

// 从 Java 后端拉取最新头像/昵称，更新 localStorage（跨设备同步）
async function pullProfileFromBackend() {
  if (!token.value) return
  try {
    const res = await fetch('/api/v1/user/info', { headers: { 'Authorization': `Bearer ${token.value}` } })
    if (!res.ok) return
    const data = (await res.json()).data
    if (data) {
      if (data.nickname) {
        localStorage.setItem(userKey('nickname'), data.nickname)
        nickname.value = data.nickname
      }
      if (data.avatar) {
        localStorage.setItem(userKey('avatar'), data.avatar)
      }
      refresh() // 通知 composable 重新读取 localStorage
    }
  } catch { /* ignore */ }
}

onMounted(() => {
  myWorksCount.value = getMyWorksCount()
  loadStarsCount()
  loadServerWorksCount().then(() => syncWorksToServer())
  loadJavaWorkCount()
  // 从 Java 后端拉取最新数据（覆盖本地），然后同步本地未同步的数据
  pullProfileFromBackend().then(() => syncExistingProfileToBackend())
})
// username 异步初始化时自动重试
watch(username, (name) => {
  if (name) loadServerWorksCount()
})
</script>

<template>
  <div class="profile-page">
    <!-- 头部卡片 — 左右布局 -->
    <RevealOnScroll>
      <div class="pf-banner glass-card">
        <div class="pf-banner-left">
          <div class="pf-avatar-ring" @click="($refs.avatarInput as any).click()">
            <AvatarIcon :name="userStore.username" :size="80" :avatar-url="avatarUrl" />
            <span class="pf-avatar-badge"><el-icon :size="12"><Camera /></el-icon></span>
          </div>
          <input ref="avatarInput" type="file" accept="image/*" style="display:none" @change="handleAvatarUpload" />
        </div>

        <div class="pf-banner-center">
          <!-- 昵称 -->
          <div v-if="editingNickname" class="pf-edit-row">
            <el-input v-model="nickname" size="small" style="width:160px" @keyup.enter="saveNickname" />
            <el-button size="small" type="primary" @click="saveNickname">确认</el-button>
            <el-button size="small" @click="editingNickname = false; nickname = displayName">取消</el-button>
          </div>
          <div v-else class="pf-nickname" @click="editingNickname = true">
            {{ nickname }} <el-icon :size="14" class="pf-edit-icon"><EditPen /></el-icon>
          </div>
          <!-- ID -->
          <div class="pf-uid">@{{ userStore.userId }}</div>
          <!-- 简介 -->
          <div v-if="editingBio" class="pf-edit-row">
            <el-input v-model="bio" size="small" style="width:280px" maxlength="200" show-word-limit placeholder="介绍一下自己..." @keyup.enter="saveBio" />
            <el-button size="small" type="primary" @click="saveBio">确认</el-button>
            <el-button size="small" @click="editingBio = false">取消</el-button>
          </div>
          <div v-else class="pf-bio" @click="editingBio = true">
            {{ bio || '点击添加个人简介，让大家认识你...' }} <el-icon :size="12" class="pf-edit-icon"><EditPen /></el-icon>
          </div>
        </div>

        <div class="pf-banner-right">
          <el-button type="primary" size="large" round @click="router.push('/sandbox')" class="pf-cta-btn">
            <el-icon><MagicStick /></el-icon> 开始创作
          </el-button>
        </div>
      </div>
    </RevealOnScroll>

    <!-- 统计卡片 — 5列均匀 -->
    <div class="pf-stats">
      <RevealOnScroll v-for="(card, i) in statCards" :key="card.label" :delay="i * 80">
        <div class="pf-stat-card glass-card" @click="card.click()">
          <div class="pf-stat-icon" :style="{ '--pf-stat-color': card.color }">
            <el-icon :size="22"><component :is="card.icon" /></el-icon>
          </div>
          <div class="pf-stat-num">
            <CountNumber :value="card.count" :duration="1200" />
          </div>
          <div class="pf-stat-label">{{ card.label }}</div>
        </div>
      </RevealOnScroll>
    </div>

    <!-- 账号设置 -->
    <RevealOnScroll :delay="500">
      <div class="pf-settings glass-card">
        <div class="pf-settings-row">
          <div class="pf-settings-info">
            <h4>账号与安全</h4>
            <p>管理你的登录状态</p>
          </div>
          <el-button type="danger" plain round @click="handleLogout">退出登录</el-button>
        </div>
      </div>
    </RevealOnScroll>
  </div>
</template>

<style scoped>
.profile-page { max-width: 720px; margin: 0 auto; padding: var(--space-xl); display: flex; flex-direction: column; gap: var(--space-lg); }

/* ====== 头部横幅 ====== */
.pf-banner {
  display: flex; align-items: center; gap: var(--space-xl);
  padding: var(--space-2xl); border-radius: var(--radius-xl);
}
.pf-banner-left { flex-shrink: 0; }
.pf-avatar-ring {
  position: relative; cursor: pointer;
  width: 88px; height: 88px; border-radius: 50%;
  padding: 3px;
  background: var(--gradient-primary);
  transition: transform var(--transition-fast);
}
.pf-avatar-ring:hover { transform: scale(1.05); }
.pf-avatar-ring :deep(.avatar-icon) {
  border-radius: 50%; border: 3px solid var(--bg-card);
}
.pf-avatar-badge {
  position: absolute; bottom: 2px; right: 2px;
  width: 24px; height: 24px; border-radius: 50%;
  background: var(--bg-card); border: 2px solid var(--border-color-light);
  display: flex; align-items: center; justify-content: center;
  color: var(--text-secondary); transition: color var(--transition-fast);
}
.pf-avatar-ring:hover .pf-avatar-badge { color: var(--accent-purple-light); }

.pf-banner-center { flex: 1; min-width: 0; }
.pf-nickname {
  font-size: 1.35rem; font-weight: 750; color: var(--text-primary);
  cursor: pointer; display: inline-flex; align-items: center; gap: 6px;
  line-height: 1.3;
}
.pf-nickname:hover { color: var(--accent-purple-light); }
.pf-edit-icon { opacity: 0; transition: opacity var(--transition-fast); color: var(--text-tertiary); }
.pf-nickname:hover .pf-edit-icon,
.pf-bio:hover .pf-edit-icon { opacity: 1; }
.pf-uid {
  font-size: 0.82rem; color: var(--text-tertiary);
  font-family: var(--font-mono); margin-top: 2px;
}
.pf-bio {
  font-size: 0.88rem; color: var(--text-secondary);
  cursor: pointer; margin-top: 6px; line-height: 1.5;
  display: inline-flex; align-items: center; gap: 4px;
}
.pf-bio:hover { color: var(--text-primary); }
.pf-edit-row {
  display: flex; gap: 8px; align-items: center;
}

.pf-banner-right { flex-shrink: 0; }
.pf-cta-btn {
  padding: 14px 28px !important; font-weight: 650 !important;
  font-size: 0.95rem !important; letter-spacing: 0.02em;
  background: var(--gradient-primary) !important; border: none !important;
}

/* ====== 统计卡片行 ====== */
.pf-stats {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: var(--space-md);
}
.pf-stat-card {
  text-align: center; padding: var(--space-lg) var(--space-sm);
  cursor: pointer; border-radius: var(--radius-lg);
  transition: all 0.25s ease;
}
.pf-stat-card:hover {
  transform: translateY(-4px);
  border-color: var(--accent-purple);
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.12);
}
.pf-stat-icon {
  width: 44px; height: 44px; border-radius: var(--radius-md);
  background: color-mix(in srgb, var(--pf-stat-color, #7c3aed) 12%, transparent);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto var(--space-sm); transition: transform 0.25s ease;
  color: var(--pf-stat-color, #7c3aed);
}
.pf-stat-card:hover .pf-stat-icon { transform: scale(1.1); }
.pf-stat-num {
  font-size: 1.6rem; font-weight: 800; color: var(--text-primary);
  font-variant-numeric: tabular-nums; line-height: 1.2;
}
.pf-stat-label {
  font-size: 0.78rem; color: var(--text-tertiary);
  margin-top: 2px; font-weight: 500;
}

/* ====== 设置卡片 ====== */
.pf-settings {
  padding: var(--space-xl); border-radius: var(--radius-lg);
}
.pf-settings-row {
  display: flex; justify-content: space-between; align-items: center;
}
.pf-settings-info h4 {
  margin: 0; font-size: 0.95rem; font-weight: 700; color: var(--text-primary);
}
.pf-settings-info p {
  margin: 2px 0 0; font-size: 0.8rem; color: var(--text-tertiary);
}

/* ====== 响应式 ====== */
@media (max-width: 768px) {
  .pf-banner {
    flex-direction: column; text-align: center;
    gap: var(--space-md);
  }
  .pf-banner-right { width: 100%; }
  .pf-cta-btn { width: 100%; }
  .pf-stats { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 480px) {
  .profile-page { padding: var(--space-md); }
  .pf-banner { padding: var(--space-lg); }
  .pf-stats { grid-template-columns: repeat(2, 1fr); }
  .pf-settings-row { flex-direction: column; gap: var(--space-md); text-align: center; }
}
</style>
