<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useAppStore } from '@/stores/app'
import { ElMessage } from 'element-plus'
import AvatarIcon from '@/components/common/AvatarIcon.vue'
import { useCurrentUser } from '@/composables/useCurrentUser'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const appStore = useAppStore()
const { displayName, avatar: avatarUrl, token, refresh } = useCurrentUser()
const searchKeyword = ref('')
const searchFocused = ref(false)
const themeSpinning = ref(false)

function refreshProfile() {
  // 由 useCurrentUser 的 refresh() 触发重新读取 localStorage
  // displayName 和 avatarUrl 是 computed，会在 username 变化时自动更新。
  // 此处保留函数签名供 watch 回调使用，实际数据已由 composable 管理。
}

// 从 Java 后端拉取最新头像/昵称（跨设备同步）
async function pullProfileFromBackend() {
  if (!token.value) return
  try {
    const res = await fetch('/api/v1/user/info', { headers: { 'Authorization': `Bearer ${token.value}` } })
    if (!res.ok) return
    const data = (await res.json()).data
    const u = userStore.username || 'default'
    if (data?.nickname) {
      localStorage.setItem(`cs:nickname:${u}`, data.nickname)
    }
    if (data?.avatar) {
      localStorage.setItem(`cs:avatar:${u}`, data.avatar)
    }
    refresh() // 触发 composable 重新读取 localStorage
  } catch { /* ignore */ }
}
// 登录后自动从 Java 后端同步最新资料
if (userStore.isLoggedIn) pullProfileFromBackend()

// 从 Profile 页返回时自动刷新头像和昵称
watch(() => route.fullPath, () => refresh())
// 登录/登出时自动同步
watch(() => userStore.isLoggedIn, (loggedIn) => {
  if (loggedIn) { refresh(); pullProfileFromBackend() }
  // 登出时 displayName/avatarUrl 会自动因 username 变为空而更新，无需手动赋值
})

function handleSearch() {
  if (searchKeyword.value.trim()) {
    router.push({ path: '/wiki', query: { q: searchKeyword.value.trim() } })
    searchKeyword.value = ''
  }
}

function handleLogout() {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}
</script>

<template>
  <header class="app-header">
    <div class="header-inner">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <span class="logo-icon">◆</span>
        <span class="logo-text">动数派<sup>π</sup></span>
      </router-link>

      <!-- 导航 -->
      <nav class="nav-links">
        <router-link to="/" class="nav-link" active-class="nav-active">
          <el-icon><HomeFilled /></el-icon> 首页
        </router-link>
        <router-link to="/community" class="nav-link" active-class="nav-active">
          <el-icon><View /></el-icon> 发现
        </router-link>
        <router-link to="/sandbox" class="nav-link" active-class="nav-active">
          <el-icon><EditPen /></el-icon> 创作
        </router-link>
        <router-link to="/wiki" class="nav-link" active-class="nav-active">
          <el-icon><Collection /></el-icon> 百科
        </router-link>
        <router-link to="/templates" class="nav-link" active-class="nav-active">
          <el-icon><Tickets /></el-icon> 模板
        </router-link>
        <router-link to="/gallery" class="nav-link" active-class="nav-active">
          <el-icon><PictureFilled /></el-icon> 画廊
        </router-link>
        <router-link to="/study" class="nav-link" active-class="nav-active">
          <el-icon><Guide /></el-icon> 知识合集
        </router-link>
      </nav>

      <div class="header-actions">
        <!-- 搜索 -->
        <div class="search-box" :class="{ 'search-expanded': searchFocused }">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索数学动画、知识点..."
            size="default"
            prefix-icon="Search"
            @keyup.enter="handleSearch"
            @focus="searchFocused = true"
            @blur="searchFocused = false"
            class="search-input"
          />
        </div>

        <!-- 主题切换 -->
        <el-button
          :icon="appStore.theme === 'dark' ? 'Sunny' : 'Moon'"
          circle
          size="default"
          @click="appStore.toggleTheme"
          class="theme-btn"
          :class="{ 'theme-spin': themeSpinning }"
          @click.once="themeSpinning = true; setTimeout(() => themeSpinning = false, 600)"
        />

        <!-- 用户 -->
        <template v-if="userStore.isLoggedIn">
          <el-dropdown trigger="click">
            <div class="user-avatar">
              <AvatarIcon :name="displayName" :size="32" :avatar-url="avatarUrl" />
              <span class="username">{{ displayName }}</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="router.push('/profile')">
                  <el-icon><User /></el-icon> 个人中心
                </el-dropdown-item>
                <el-dropdown-item @click="router.push('/sandbox')">
                  <el-icon><EditPen /></el-icon> 创作工坊
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon> 退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button type="primary" size="default" @click="router.push('/login')" round>
            登录 / 注册
          </el-button>
        </template>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  position: fixed;
  top: 0; left: 0; right: 0; z-index: 100;
  height: var(--header-height);
  background: rgba(10, 10, 15, 0.82);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-bottom: 1px solid var(--border-color);
}
[data-theme="light"] .app-header {
  background: rgba(255, 255, 255, 0.82);
}

.header-inner {
  max-width: 1400px; margin: 0 auto; height: 100%;
  display: flex; align-items: center; gap: var(--space-xl);
  padding: 0 var(--space-2xl);
}

/* ====== Logo ====== */
.logo {
  display: flex; align-items: baseline; gap: 6px;
  text-decoration: none; flex-shrink: 0;
  transition: transform var(--transition-fast);
}
.logo:hover { transform: scale(1.04); }
.logo-icon {
  font-size: 1.75rem;
  background: var(--gradient-primary);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  filter: drop-shadow(0 0 8px rgba(124, 58, 237, 0.4));
}
.logo-text {
  font-size: 1.25rem; font-weight: 800; letter-spacing: -0.02em;
  background: linear-gradient(135deg, var(--accent-purple) 0%, var(--accent-cyan) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  white-space: nowrap;
}
.logo-text sup {
  font-size: 0.55em; font-weight: 600;
  background: none; -webkit-text-fill-color: var(--accent-cyan);
  margin-left: 1px;
}

/* ====== 导航 — 胶囊标签 ====== */
.nav-links {
  display: flex; gap: 2px;
  flex: 1; justify-content: center;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-full);
  padding: 3px;
  max-width: fit-content;
  margin: 0 auto;
}
.nav-link {
  display: flex; align-items: center; gap: 5px;
  padding: 7px 16px;
  border-radius: var(--radius-full);
  text-decoration: none;
  color: var(--text-tertiary);
  font-size: 0.85rem; font-weight: 550;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  white-space: nowrap; position: relative;
}
.nav-link:hover {
  color: var(--text-primary);
}
.nav-link.nav-active {
  color: #fff;
  background: var(--gradient-primary);
  box-shadow: 0 2px 12px rgba(124, 58, 237, 0.35), 0 0 0 1px rgba(255,255,255,0.1) inset;
}
[data-theme="light"] .nav-link.nav-active {
  color: #fff;
}
.nav-link.nav-active :deep(.el-icon) {
  filter: drop-shadow(0 0 4px rgba(255,255,255,0.4));
}

/* ====== 操作区 ====== */
.header-actions {
  display: flex; align-items: center; gap: var(--space-md);
  flex-shrink: 0;
}

.search-box {
  width: 200px; transition: width var(--transition-base);
}
.search-box.search-expanded { width: 250px; }
.search-input :deep(.el-input__wrapper) {
  background: var(--bg-card); border: 1px solid var(--border-color);
  border-radius: var(--radius-full); box-shadow: none;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
  height: 38px;
}
.search-input :deep(.el-input__wrapper:hover) {
  border-color: var(--border-color-light);
}
.search-input :deep(.el-input__wrapper.is-focus) {
  border-color: var(--accent-purple);
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.12);
}

.theme-btn {
  background: var(--bg-card) !important; border: 1px solid var(--border-color) !important;
  color: var(--text-secondary) !important; transition: all var(--transition-base) !important;
  width: 38px; height: 38px;
}
.theme-btn:hover {
  color: var(--text-primary) !important; border-color: var(--accent-purple) !important;
}
.theme-btn.theme-spin :deep(i) {
  animation: theme-spin 0.6s var(--ease-spring);
}
@keyframes theme-spin {
  0% { transform: rotate(0deg) scale(1); }
  50% { transform: rotate(180deg) scale(1.2); }
  100% { transform: rotate(360deg) scale(1); }
}

/* 用户 */
.user-avatar {
  display: flex; align-items: center; gap: var(--space-sm);
  cursor: pointer; color: var(--text-secondary);
  padding: 4px 12px 4px 4px; border-radius: var(--radius-full);
  background: var(--bg-card); border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
}
.user-avatar:hover { color: var(--text-primary); border-color: var(--border-color-light); }
.username { font-size: 0.85rem; font-weight: 550; }

@media (max-width: 1100px) {
  .search-box { display: none; }
  .nav-links { gap: 0; }
  .nav-link { padding: 7px 10px; font-size: 0.8rem; }
  .nav-link .el-icon { font-size: 15px; }
}
@media (max-width: 768px) {
  .header-inner { padding: 0 var(--space-md); gap: var(--space-sm); }
  .logo-text { font-size: 1.1rem; }
  .nav-link { padding: 6px 8px; }
  .nav-link span, .username { display: none; }
  .nav-link { font-size: 0; }
}
</style>
