<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { videosApi } from '@/api/videos'
import { workApi } from '@/api/work'
import { tasksApi } from '@/api/tasks'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { VideoFile } from '@/types/task'
import PageHeader from '@/components/common/PageHeader.vue'

const router = useRouter()
const route = useRoute()
const allVideos = ref<VideoFile[]>([])
const starredVideos = ref<VideoFile[]>([])
const loading = ref(false)
const deleting = ref<string | null>(null)
const publishing = ref<string | null>(null)
const publishedWorks = ref<string[]>([])
const thumbFailed = ref<Set<string>>(new Set())

function onThumbError(event: Event, v: any) {
  thumbFailed.value = new Set([...thumbFailed.value, v.filename])
}

const activeTab = ref<'all' | 'my-works' | 'stars'>(
  (route.query.tab as 'all' | 'my-works' | 'stars') || 'all',
)

function getMyWorks(): string[] {
  try { return JSON.parse(localStorage.getItem('cs:my-works') || '[]') }
  catch { return [] }
}

function loadPublished() {
  try { publishedWorks.value = JSON.parse(localStorage.getItem('cs:published-works') || '[]') }
  catch { publishedWorks.value = [] }
}

function savePublished(list: string[]) {
  publishedWorks.value = list
  localStorage.setItem('cs:published-works', JSON.stringify(list))
}

function isAdmin(): boolean {
  return localStorage.getItem('username') === 'admin'
}

function canDeleteFile(filename: string): boolean {
  if (isAdmin()) return true
  if (getMyWorks().includes(filename)) return true
  // 服务端加载的作品也可以删除
  return serverMyWorks.value.some((v: any) => v.filename === filename)
}

const videos = computed(() => {
  if (activeTab.value === 'stars') return starredVideos.value
  if (activeTab.value === 'my-works') {
    if (serverMyWorks.value.length > 0) return serverMyWorks.value
    const works = getMyWorks()
    return allVideos.value.filter(v => works.includes(v.filename))
  }
  return allVideos.value
})

const myWorksCount = computed(() => {
  if (serverMyWorks.value.length > 0) return serverMyWorks.value.length
  const works = getMyWorks()
  return allVideos.value.filter(v => works.includes(v.filename)).length
})
const starsCount = computed(() => starredVideos.value.length)

function switchTab(tab: 'all' | 'my-works' | 'stars') {
  activeTab.value = tab
  router.replace({ query: { tab } })
}

// ==================== 发布对话框状态 ====================
const publishDialogVisible = ref(false)
const publishTarget = ref('')
const publishTitle = ref('')
const publishDesc = ref('')
const publishTags = ref('')
const publishIsPublic = ref(true)
const publishTitleError = ref('')
const publishValid = computed(() => publishTitle.value.trim().length > 0)

function openPublishDialog(v: VideoFile & { title?: string }, event: Event) {
  event.stopPropagation()
  publishTarget.value = v.filename
  publishTitle.value = (v as any).title || v.filename.replace('.mp4', '')
  publishDesc.value = ''
  publishTags.value = ''
  publishIsPublic.value = true
  publishTitleError.value = ''
  publishDialogVisible.value = true
}

async function handlePublish() {
  const filename = publishTarget.value
  if (!filename) return
  if (!publishTitle.value.trim()) { publishTitleError.value = '作品标题不能为空'; return }
  publishTitleError.value = ''
  publishing.value = filename
  try {
    let code = ''
    try {
      const codeRes = await videosApi.getCode(filename)
      code = codeRes.data.data?.code || ''
      if (!code) ElMessage.warning('未找到代码文件，将发布空白代码')
    } catch (codeErr: any) {
      ElMessage.error('获取代码失败：' + (codeErr.message || '请确认 Python 服务已重启'))
      return
    }
    const res = await workApi.publish({
      workTitle: publishTitle.value.trim() || filename,
      workDesc: publishDesc.value,
      tagList: publishTags.value,
      isPublic: publishIsPublic.value,
      code,
      previewUrl: `/videos/${filename}`,
    })
    if (res.data.code === 200 || res.data.code === 0) {
      ElMessage.success({ message: '已发布到社区', duration: 1200 })
      publishDialogVisible.value = false
      const list = [...publishedWorks.value]
      if (!list.includes(filename)) { list.push(filename); savePublished(list) }
    } else {
      ElMessage.error(res.data.message || '发布失败')
    }
  } catch (e: any) {
    const status = e.response?.status
    const detail = e.response?.data?.message || e.response?.data?.detail || ''
    ElMessage.error(`发布失败（HTTP ${status || '网络错误'}）：${detail || e.message || '未知错误'}`)
  } finally {
    publishing.value = null
  }
}

// ==================== 删除功能 ====================
async function handleDeleteFile(filename: string, event: Event) {
  event.stopPropagation()
  try {
    await ElMessageBox.confirm(
      `确定要删除「${filename}」吗？\n对应的代码文件也将被删除，此操作不可撤销。`,
      '删除确认',
      { confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning' }
    )
  } catch { return }
  deleting.value = filename
  try {
    await videosApi.deleteVideo(filename)
    try { await workApi.deleteByVideoPath(`/videos/${filename}`) } catch { /* 无发布记录时忽略 */ }
    ElMessage.success('已删除')
    // 从 localStorage 移除
    const works = getMyWorks()
    const idx = works.indexOf(filename)
    if (idx !== -1) { works.splice(idx, 1); localStorage.setItem('cs:my-works', JSON.stringify(works)) }
    // 从服务端列表即时移除
    serverMyWorks.value = serverMyWorks.value.filter((v: any) => v.filename !== filename)
    await loadAll()
  } catch { ElMessage.error('删除失败') }
  finally { deleting.value = null }
}

async function loadAll() {
  loading.value = true
  try {
    const res = await videosApi.getList(false)
    allVideos.value = res.data.data?.items || []
  } finally { loading.value = false }
}

async function loadStars() {
  try {
    const res = await videosApi.getList(true)
    starredVideos.value = res.data.data?.items || []
  } catch { /* ignore */ }
}

const serverMyWorks = ref<VideoFile[]>([])
async function loadMyWorksFromServer() {
  const name = localStorage.getItem('username') || ''
  if (!name) return
  try {
    const res = await videosApi.getMyWorks(name)
    serverMyWorks.value = res.data.data?.items || []
    const local = getMyWorks()
    if (local.length > 0) { await videosApi.syncMyWorks(name, local).catch(() => {}) }
  } catch { /* ignore */ }
}

const sortBy = ref<'time' | 'title' | 'size'>('time')

const sortedVideos = computed(() => {
  const arr = [...videos.value]
  if (sortBy.value === 'title') arr.sort((a, b) => getTitle(a).localeCompare(getTitle(b), 'zh'))
  else if (sortBy.value === 'size') arr.sort((a, b) => b.size_bytes - a.size_bytes)
  return arr
})

function getTitle(v: VideoFile & { title?: string }) {
  return (v as any).title || v.filename
}

async function syncPendingTasks() {
  try {
    const pending: string[] = JSON.parse(localStorage.getItem('cs:pending-tasks') || '[]')
    if (!pending.length) return
    const works: string[] = JSON.parse(localStorage.getItem('cs:my-works') || '[]')
    let changed = false
    for (const tid of pending.slice(0, 10)) {
      try {
        const res = await tasksApi.getTask(tid)
        const data = res.data
        const vp = data?.data?.video_path || ''
        const fn = vp.replace('/videos/', '')
        if (fn && data?.data?.state === 'SUCCESS' && !works.includes(fn)) {
          works.unshift(fn); changed = true
        }
      } catch { /* skip */ }
    }
    if (changed) {
      localStorage.setItem('cs:my-works', JSON.stringify(works.slice(0, 50)))
      await loadAll()
    }
    localStorage.setItem('cs:pending-tasks', JSON.stringify(pending.slice(0, 5)))
  } catch { /* ignore */ }
}

onMounted(() => { loadPublished(); loadAll().then(() => loadStars()).then(() => syncPendingTasks()).then(() => loadMyWorksFromServer()) })
watch(() => route.query.tab, (t) => {
  if (t === 'all' || t === 'my-works' || t === 'stars') activeTab.value = t
})
// 登录状态变化时重新加载数据（退出登录后数据已清理，重新登录后刷新）
watch(() => localStorage.getItem('token'), () => {
  if (localStorage.getItem('token')) {
    loadAll().then(() => loadStars()).then(() => loadMyWorksFromServer())
  }
})
</script>

<template>
  <div class="gallery-page">
    <PageHeader title="精选画廊" description="动画作品展示与收藏" icon="PictureFilled" />

    <div class="gallery-tabs">
      <el-button :type="activeTab === 'all' ? 'primary' : 'default'" round @click="switchTab('all')">
        全部作品 ({{ allVideos.length }})
      </el-button>
      <el-button :type="activeTab === 'my-works' ? 'primary' : 'default'" round @click="switchTab('my-works')">
        我的作品 ({{ myWorksCount }})
      </el-button>
      <el-button :type="activeTab === 'stars' ? 'primary' : 'default'" round @click="switchTab('stars')">
        我的收藏 ({{ starsCount }})
      </el-button>
      <el-select v-model="sortBy" size="small" style="width:140px" @change="() => {}">
        <el-option label="最新优先" value="time" />
        <el-option label="标题 A-Z" value="title" />
        <el-option label="文件大小" value="size" />
      </el-select>
    </div>

    <div class="gallery-grid" v-loading="loading">
      <div v-for="v in sortedVideos" :key="v.filename" class="g-card glass-card" @click="router.push(`/gallery/${v.filename}`)">
        <div class="g-thumb">
          <img :src="(v as any).poster || videosApi.getThumbnailUrl(v.filename)"
               loading="lazy" class="g-thumb-img"
               @error="onThumbError($event, v)"
               :alt="getTitle(v)" />
          <div class="g-play"><el-icon :size="32"><VideoPlay /></el-icon></div>
          <div v-if="thumbFailed.has(v.filename)" class="g-thumb-placeholder">
            <el-icon :size="40"><VideoCamera /></el-icon>
            <span>无封面</span>
          </div>
        </div>
        <div class="g-info">
          <h4 :title="getTitle(v)">{{ getTitle(v) }}</h4>
          <span class="g-size">{{ v.size_mb }} MB · {{ v.created_at?.slice(0, 10) }}</span>
        </div>
        <!-- 操作按钮（我的作品 tab 显示） -->
        <div v-if="activeTab === 'my-works'" class="g-card-actions">
          <el-button
            v-if="!publishedWorks.includes(v.filename)"
            size="small" type="primary" plain
            :loading="publishing === v.filename"
            @click="openPublishDialog(v, $event)">
            <el-icon><Upload /></el-icon> 发布
          </el-button>
          <el-button
            v-if="canDeleteFile(v.filename)"
            size="small" type="danger" plain
            :loading="deleting === v.filename"
            @click="handleDeleteFile(v.filename, $event)">
            <el-icon><Delete /></el-icon> 删除
          </el-button>
          <el-tag v-if="publishedWorks.includes(v.filename)" size="small" type="success" disable-transitions>已发布</el-tag>
        </div>
      </div>
    </div>

    <!-- 发布对话框 -->
    <el-dialog v-model="publishDialogVisible" title="发布到社区" width="480px">
      <el-form label-position="top">
        <el-form-item label="作品标题" :class="{ 'is-error': publishTitleError }" :error="publishTitleError">
          <el-input v-model="publishTitle" placeholder="输入作品标题（必填）" @input="publishTitleError = ''" />
        </el-form-item>
        <el-form-item label="作品描述">
          <el-input v-model="publishDesc" type="textarea" :rows="3" placeholder="写一段描述介绍你的作品..." />
        </el-form-item>
        <el-form-item label="标签（逗号分隔）">
          <el-input v-model="publishTags" placeholder="如：排序算法, 可视化, 教学" />
        </el-form-item>
        <el-form-item label="公开范围">
          <el-radio-group v-model="publishIsPublic">
            <el-radio :value="true">公开</el-radio>
            <el-radio :value="false">私密</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="publishDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="publishing !== null" :disabled="!publishValid" @click="handlePublish">发布</el-button>
      </template>
    </el-dialog>

    <div v-if="!loading && videos.length === 0" class="empty-state">
      <el-empty :description="activeTab === 'stars' ? '还没有收藏作品' : activeTab === 'my-works' ? '还没有生成作品' : '还没有作品'" />
      <el-button v-if="activeTab !== 'stars'" type="primary" round @click="router.push('/sandbox')">去沙箱创作</el-button>
    </div>
  </div>
</template>

<style scoped>
.gallery-page { padding-bottom: var(--space-3xl); }
.gallery-tabs { display: flex; gap: var(--space-sm); justify-content: center; flex-wrap: wrap; max-width: var(--max-content-width); margin: 0 auto var(--space-xl); padding: 0 var(--space-xl); }
.gallery-grid { max-width: var(--max-content-width); margin: 0 auto; padding: 0 var(--space-xl); display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: var(--space-lg); }
.g-card { cursor: pointer; overflow: hidden; padding: 0; }
.g-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-lg); }
.g-thumb { position: relative; aspect-ratio: 16/9; background: var(--bg-secondary); overflow: hidden; }
.g-thumb-img { width: 100%; height: 100%; object-fit: cover; }
.g-thumb-placeholder { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; color: var(--text-tertiary); font-size: 0.75rem; }
.g-play { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.3); opacity: 0; transition: opacity var(--transition-fast); color: white; }
.g-card:hover .g-play { opacity: 1; }
.g-info { padding: var(--space-md); }
.g-info h4 { font-size: 0.9rem; font-weight: 600; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.g-size { font-size: 0.75rem; color: var(--text-tertiary); }
.g-card-actions { display: flex; gap: 6px; padding: 8px var(--space-md) var(--space-md); opacity: 0; transition: opacity var(--transition-fast); }
.g-card:hover .g-card-actions { opacity: 1; }
.empty-state { text-align: center; padding: var(--space-3xl); }
</style>
