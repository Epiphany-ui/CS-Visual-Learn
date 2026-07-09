<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useAppStore } from '@/stores/app'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const appStore = useAppStore()
const searchKeyword = ref('')

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
        <span class="logo-text">CS Visual Learn</span>
      </router-link>

      <!-- 导航 -->
      <nav class="nav-links">
        <router-link to="/wiki" class="nav-link">
          <el-icon><Collection /></el-icon> 百科
        </router-link>
        <router-link to="/sandbox" class="nav-link">
          <el-icon><EditPen /></el-icon> 沙箱
        </router-link>
        <router-link to="/templates" class="nav-link">
          <el-icon><Tickets /></el-icon> 模板库
        </router-link>
        <router-link to="/gallery" class="nav-link">
          <el-icon><PictureFilled /></el-icon> 画廊
        </router-link>
        <router-link to="/community" class="nav-link">
          <el-icon><User /></el-icon> 社区
        </router-link>
        <router-link to="/study" class="nav-link">
          <el-icon><School /></el-icon> 备考
        </router-link>
      </nav>

      <div class="header-actions">
        <!-- 搜索 -->
        <div class="search-box">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索知识点、动画、模板..."
            size="default"
            prefix-icon="Search"
            @keyup.enter="handleSearch"
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
        />

        <!-- 用户 -->
        <template v-if="userStore.isLoggedIn">
          <el-dropdown trigger="click">
            <div class="user-avatar">
              <el-avatar :size="32" :icon="'UserFilled'" />
              <span class="username">{{ userStore.username }}</span>
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
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: var(--header-height);
  background: rgba(10, 10, 15, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-color);
  transition: background var(--transition-base);
}

[data-theme="light"] .app-header {
  background: rgba(255, 255, 255, 0.85);
}

.header-inner {
  max-width: var(--max-content-width);
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  gap: var(--space-lg);
  padding: 0 var(--space-xl);
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  text-decoration: none;
  flex-shrink: 0;
}
.logo-icon {
  font-size: 1.5rem;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.logo-text {
  font-size: 1.05rem;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  white-space: nowrap;
}

/* 导航 */
.nav-links {
  display: flex;
  gap: var(--space-xs);
  flex: 1;
  justify-content: center;
}
.nav-link {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 14px;
  border-radius: var(--radius-md);
  text-decoration: none;
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 500;
  transition: all var(--transition-fast);
  white-space: nowrap;
}
.nav-link:hover {
  color: var(--text-primary);
  background: var(--bg-card-hover);
}
.nav-link.router-link-active {
  color: var(--accent-purple-light);
  background: rgba(124, 58, 237, 0.1);
}

/* 操作区 */
.header-actions {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  flex-shrink: 0;
}

.search-box {
  width: 200px;
}
.search-input :deep(.el-input__wrapper) {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-full);
  box-shadow: none;
}
.search-input :deep(.el-input__wrapper:hover) {
  border-color: var(--border-color-light);
}

.theme-btn {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-color) !important;
  color: var(--text-secondary) !important;
}
.theme-btn:hover {
  color: var(--text-primary) !important;
  border-color: var(--accent-purple) !important;
}

/* 用户 */
.user-avatar {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  cursor: pointer;
  color: var(--text-secondary);
}
.user-avatar:hover {
  color: var(--text-primary);
}
.username {
  font-size: 0.9rem;
  font-weight: 500;
}
</style>
