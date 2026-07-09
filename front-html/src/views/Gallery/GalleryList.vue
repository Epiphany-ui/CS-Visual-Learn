<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { videosApi } from '@/api/videos'
import type { VideoFile } from '@/types/task'
import PageHeader from '@/components/common/PageHeader.vue'

const router = useRouter()
const videos = ref<VideoFile[]>([])
const loading = ref(false)

async function load() {
  loading.value = true
  try {
    const res = await videosApi.getList()
    videos.value = res.data.data?.items || []
  } finally { loading.value = false }
}

onMounted(load)
</script>

<template>
  <div class="gallery-page">
    <PageHeader title="精选画廊" description="高质量可视化作品展示，点赞、收藏、Fork" icon="PictureFilled" />

    <div class="gallery-grid" v-loading="loading">
      <div v-for="v in videos" :key="v.filename" class="g-card glass-card" @click="router.push(`/gallery/${v.filename}`)">
        <div class="g-thumb">
          <video :src="videosApi.getPlayUrl(v.filename)" preload="metadata" class="g-video" />
          <div class="g-play"><el-icon :size="32"><VideoPlay /></el-icon></div>
        </div>
        <div class="g-info">
          <h4>{{ v.filename }}</h4>
          <span class="g-size">{{ v.size_mb }} MB · {{ v.created_at?.slice(0, 10) }}</span>
        </div>
      </div>
    </div>

    <div v-if="!loading && videos.length === 0" class="empty-state">
      <el-empty description="还没有作品，快去沙箱创作吧！" />
      <el-button type="primary" round @click="router.push('/sandbox')">去沙箱创作</el-button>
    </div>
  </div>
</template>

<style scoped>
.gallery-page { padding-bottom: var(--space-3xl); }
.gallery-grid {
  max-width: var(--max-content-width); margin: 0 auto; padding: 0 var(--space-xl);
  display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: var(--space-lg);
}
.g-card { cursor: pointer; overflow: hidden; padding: 0; }
.g-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-lg); }
.g-thumb { position: relative; aspect-ratio: 16/9; background: var(--bg-secondary); overflow: hidden; }
.g-video { width: 100%; height: 100%; object-fit: cover; }
.g-play { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.3); opacity: 0; transition: opacity var(--transition-fast); color: white; }
.g-card:hover .g-play { opacity: 1; }
.g-info { padding: var(--space-md); }
.g-info h4 { font-size: 0.9rem; font-weight: 600; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.g-size { font-size: 0.75rem; color: var(--text-tertiary); }
.empty-state { text-align: center; padding: var(--space-3xl); }
</style>
