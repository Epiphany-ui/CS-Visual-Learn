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

async function checkSaved() {
  // 通过 gallery list 检查是否已收藏（轻量级方式）
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

onMounted(checkSaved)
</script>

<template>
  <div class="gallery-detail">
    <el-button link @click="router.back()" style="margin-bottom:16px"><el-icon><ArrowLeft /></el-icon> 返回画廊</el-button>
    <div class="gd-player glass-card">
      <video :src="videoUrl" controls autoplay loop class="gd-video" />
    </div>
    <div class="gd-actions">
      <el-button round><el-icon><Download /></el-icon> <a :href="downloadUrl" download style="text-decoration:none;color:inherit">下载 MP4</a></el-button>
      <el-button round :loading="converting" @click="handleConvertGif"><el-icon><PictureFilled /></el-icon> 转为 GIF</el-button>
      <el-button round><el-icon><Share /></el-icon> 分享</el-button>
      <el-button round :type="saved ? 'warning' : 'default'" @click="handleSave">
        <el-icon><StarFilled v-if="saved" /><Star v-else /></el-icon> {{ saved ? '已收藏' : '收藏' }}
      </el-button>
    </div>
    <div v-if="gifUrl" class="gd-gif glass-card" style="margin-top:16px;padding:16px;">
      <h4>GIF 预览</h4>
      <img :src="gifUrl" style="max-width:100%;border-radius:8px;" />
    </div>
  </div>
</template>

<style scoped>
.gallery-detail { max-width: 1000px; margin: 0 auto; padding: var(--space-xl); }
.gd-player { overflow: hidden; border-radius: var(--radius-lg); }
.gd-video { width: 100%; display: block; }
.gd-actions { display: flex; gap: var(--space-md); margin-top: var(--space-lg); flex-wrap: wrap; }
</style>
