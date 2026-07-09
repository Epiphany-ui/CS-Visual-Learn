<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { videosApi, debugApi } from '@/api/videos'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const filename = route.params.filename as string
const videoUrl = videosApi.getPlayUrl(filename)
const downloadUrl = videosApi.getDownloadUrl(filename)
const converting = ref(false)
const gifUrl = ref('')
const saved = ref(false)

// Debug/元数据
const videoInfo = ref<any>(null)
const thumbUrl = ref('')
const showDebug = ref(false)

async function checkSaved() {
  try {
    const res = await videosApi.getList(true)
    const items: { filename: string }[] = res.data.data?.items || []
    saved.value = items.some((v) => v.filename === filename)
  } catch { /* ignore */ }
}

async function handleSave() {
  try {
    const res = await videosApi.saveVideo(filename)
    saved.value = res.data.data?.saved ?? false
    ElMessage.success(saved.value ? '已收藏到画廊' : '已取消收藏')
  } catch {
    ElMessage.error('操作失败，请重试')
  }
}

async function handleConvertGif() {
  converting.value = true
  try {
    const res = await videosApi.convertGif(filename)
    const data = res.data.data
    if (data) {
      gifUrl.value = `http://localhost:8000${data.url}`
      ElMessage.success(`GIF 转换完成（${data.size_kb}KB）`)
    }
  } catch { /* handled */ }
  finally { converting.value = false }
}

async function loadDebugInfo() {
  try {
    const res = await debugApi.getVideoInfo(filename)
    videoInfo.value = res.data.data
    // 获取中间帧作为海报图
    const thumb = await debugApi.getThumbnailSheet(filename, 3, 2)
    thumbUrl.value = thumb.data.data?.url || ''
  } catch { /* debug info optional */ }
}

function formatDuration(seconds: number): string {
  const m = Math.floor(seconds / 60)
  const s = Math.round(seconds % 60)
  return `${m}:${s.toString().padStart(2, '0')}`
}

onMounted(() => { checkSaved(); loadDebugInfo() })
</script>

<template>
  <div class="gallery-detail">
    <el-button link @click="router.back()" style="margin-bottom:16px"><el-icon><ArrowLeft /></el-icon> 返回画廊</el-button>

    <div class="gd-layout">
      <!-- 左侧：视频播放器 -->
      <div class="gd-main">
        <div class="gd-player glass-card">
          <video
            :src="videoUrl"
            controls autoplay loop
            class="gd-video"
            :poster="`http://localhost:8000/api/debug/video/${filename}/frame-at-time?time=1.5`"
          />
        </div>
        <div class="gd-actions">
          <el-button round><el-icon><Download /></el-icon> <a :href="downloadUrl" download style="text-decoration:none;color:inherit">下载 MP4</a></el-button>
          <el-button round :loading="converting" @click="handleConvertGif"><el-icon><PictureFilled /></el-icon> 转为 GIF</el-button>
          <el-button round :type="saved ? 'warning' : 'default'" @click="handleSave">
            <el-icon><StarFilled v-if="saved" /><Star v-else /></el-icon> {{ saved ? '已收藏' : '收藏' }}
          </el-button>
          <el-button round @click="showDebug = !showDebug">
            <el-icon><VideoCamera /></el-icon> {{ showDebug ? '收起' : '调试' }}
          </el-button>
        </div>
        <div v-if="gifUrl" class="gd-gif glass-card" style="margin-top:16px;padding:16px;">
          <h4>GIF 预览</h4>
          <img :src="gifUrl" style="max-width:100%;border-radius:8px;" alt="GIF preview" />
        </div>
      </div>

      <!-- 右侧：元信息 -->
      <div class="gd-sidebar">
        <div class="gd-meta glass-card">
          <h3>视频信息</h3>
          <dl v-if="videoInfo">
            <div><dt>文件名</dt><dd>{{ filename }}</dd></div>
            <div v-if="videoInfo.duration"><dt>时长</dt><dd>{{ formatDuration(videoInfo.duration) }}</dd></div>
            <div v-if="videoInfo.fps"><dt>帧率</dt><dd>{{ videoInfo.fps }} fps</dd></div>
            <div v-if="videoInfo.total_frames"><dt>总帧数</dt><dd>{{ videoInfo.total_frames }}</dd></div>
            <div v-if="videoInfo.width"><dt>分辨率</dt><dd>{{ videoInfo.width }}×{{ videoInfo.height }}</dd></div>
          </dl>
          <p v-else class="no-meta">暂无可用的元数据</p>
        </div>
      </div>
    </div>

    <!-- 调试面板 -->
    <div v-if="showDebug" class="gd-debug glass-card" style="margin-top:24px;padding:20px;">
      <h3>逐帧调试</h3>
      <p style="color:var(--text-secondary);font-size:0.85rem;margin-bottom:16px">
        总帧数 {{ videoInfo?.total_frames || '?' }} ·
        <el-button link size="small" @click="loadDebugInfo">刷新</el-button>
      </p>
      <div v-if="thumbUrl" class="thumb-preview">
        <h4 style="margin-bottom:8px;color:var(--text-secondary);font-size:0.85rem">缩略图网格</h4>
        <img :src="`http://localhost:8000${thumbUrl}`" style="max-width:100%;border-radius:8px;" alt="缩略图" />
      </div>
      <el-empty v-else description="暂无可用的缩略图" :image-size="80" />
    </div>
  </div>
</template>

<style scoped>
.gallery-detail { max-width: 1200px; margin: 0 auto; padding: var(--space-xl); }
.gd-layout { display: grid; grid-template-columns: 1fr 300px; gap: var(--space-lg); }
.gd-player { overflow: hidden; border-radius: var(--radius-lg); }
.gd-video { width: 100%; display: block; }
.gd-actions { display: flex; gap: var(--space-md); margin-top: var(--space-lg); flex-wrap: wrap; }

.gd-sidebar { display: flex; flex-direction: column; gap: var(--space-md); }
.gd-meta { padding: var(--space-lg); }
.gd-meta h3 { font-size: 1rem; font-weight: 700; color: var(--text-primary); margin-bottom: var(--space-md); }
.gd-meta dl div { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid var(--border-color); }
.gd-meta dt { color: var(--text-tertiary); font-size: 0.85rem; }
.gd-meta dd { color: var(--text-primary); font-size: 0.85rem; font-weight: 500; }
.no-meta { color: var(--text-tertiary); font-size: 0.85rem; }

.gd-debug h3 { font-size: 1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 8px; }
.thumb-preview img { border: 1px solid var(--border-color); }

@media (max-width: 900px) {
  .gd-layout { grid-template-columns: 1fr; }
}
</style>
