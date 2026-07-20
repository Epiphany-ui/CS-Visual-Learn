<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { wikiApi } from '@/api/wiki'
import type { WikiDetail } from '@/types/wiki'
import { marked } from 'marked'
import katex from 'katex'
import 'katex/dist/katex.min.css'

marked.setOptions({ breaks: true, gfm: true })

const props = defineProps<{
  wikiSlug: string
  visible: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'generate', prompt: string): void
  (e: 'mark-learned'): void
  (e: 'reading-seconds', seconds: number): void
}>()

const detail = ref<WikiDetail | null>(null)
const loading = ref(false)
const contentHtml = ref('')
const startTime = ref(0)

function renderMath(html: string): string {
  try {
    html = html.replace(/\$\$([\s\S]*?)\$\$/g, (_, f: string) => {
      try { return katex.renderToString(f.trim(), { displayMode: true, throwOnError: false }) }
      catch { return `<pre class="math-error">${f}</pre>` }
    })
    html = html.replace(/\\\[([\s\S]*?)\\\]/g, (_, f: string) => {
      try { return katex.renderToString(f.trim(), { displayMode: true, throwOnError: false }) }
      catch { return `<pre class="math-error">${f}</pre>` }
    })
    html = html.replace(/\$([^$]+?)\$/g, (_, f: string) => {
      try { return katex.renderToString(f.trim(), { displayMode: false, throwOnError: false }) }
      catch { return `<code class="math-error">${f}</code>` }
    })
    html = html.replace(/\\\(([\s\S]*?)\\\)/g, (_, f: string) => {
      try { return katex.renderToString(f.trim(), { displayMode: false, throwOnError: false }) }
      catch { return `<code class="math-error">${f}</code>` }
    })
  } catch { /* ignore */ }
  return html
}

function fixLinks(html: string): string {
  return html.replace(/href="\/api\/wiki\/([^"]+)"/g, 'href="#/wiki/$1"')
}

async function loadContent() {
  if (!props.wikiSlug) return
  loading.value = true
  startTime.value = Date.now()
  try {
    const res = await wikiApi.getDetail(props.wikiSlug)
    if (res.data.data) {
      detail.value = res.data.data
      let html = res.data.data.content
      html = renderMath(html)
      html = await marked.parse(html)
      html = fixLinks(html)
      contentHtml.value = html
      await nextTick()
    }
  } catch {
    detail.value = null
    contentHtml.value = '<p class="wiki-error">百科内容加载失败</p>'
  } finally {
    loading.value = false
  }
}

function handleClose() {
  if (startTime.value) {
    const seconds = Math.round((Date.now() - startTime.value) / 1000)
    emit('reading-seconds', seconds)
  }
  startTime.value = 0
  emit('close')
}

function handleGenerate() {
  // 同时上报阅读时长
  if (startTime.value) {
    const seconds = Math.round((Date.now() - startTime.value) / 1000)
    emit('reading-seconds', seconds)
  }
  startTime.value = 0
  emit('generate', detail.value?.meta?.title || '')
}

function handleMarkLearned() {
  if (startTime.value) {
    const seconds = Math.round((Date.now() - startTime.value) / 1000)
    emit('reading-seconds', seconds)
  }
  startTime.value = 0
  emit('mark-learned')
}

// 组件挂载时如果 visible 就加载；visible 或 wikiSlug 变化时重新加载
watch([() => props.visible, () => props.wikiSlug], ([v, slug]) => {
  if (v && slug) {
    detail.value = null
    contentHtml.value = ''
    loadContent()
  }
}, { immediate: true })

function getDifficultyClass(d: string): string {
  if (['入门', '初级'].includes(d)) return 'diff-easy'
  if (d === '中等') return 'diff-medium'
  return 'diff-hard'
}
</script>

<template>
  <Transition name="wiki-slide">
    <div v-if="visible" class="wiki-preview glass-card">
      <div class="wiki-preview-header">
        <div class="wiki-header-left">
          <el-icon :size="20"><Reading /></el-icon>
          <span v-if="detail">{{ detail.meta.title }}</span>
          <span v-else>百科词条</span>
          <el-tag v-if="detail" :class="getDifficultyClass(detail.meta.difficulty)" size="small">
            {{ detail.meta.difficulty }}
          </el-tag>
        </div>
        <el-button link @click="handleClose">
          <el-icon :size="18"><Close /></el-icon>
        </el-button>
      </div>

      <div class="wiki-preview-body" v-loading="loading">
        <div v-if="contentHtml" class="wiki-content prose" v-html="contentHtml" />
        <div v-else-if="!loading" class="wiki-empty">
          <el-icon :size="32"><Document /></el-icon>
          <p>暂无百科内容</p>
        </div>
      </div>

      <div v-if="detail && !loading" class="wiki-preview-actions">
        <el-button size="default" @click="handleMarkLearned">
          <el-icon><CircleCheck /></el-icon>
          标记已学
        </el-button>
        <el-button type="primary" size="default" @click="handleGenerate">
          <el-icon><MagicStick /></el-icon>
          理解了，生成动画
        </el-button>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.wiki-preview {
  margin-top: var(--space-sm);
  overflow: hidden;
  max-height: 600px;
  display: flex;
  flex-direction: column;
}

.wiki-preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid var(--border-color);
  background: rgba(124, 58, 237, 0.04);
}
.wiki-header-left {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}

.diff-easy { background: rgba(16, 185, 129, 0.12); color: var(--accent-green); border: none; }
.diff-medium { background: rgba(245, 158, 11, 0.12); color: var(--accent-orange); border: none; }
.diff-hard { background: rgba(239, 68, 68, 0.12); color: var(--accent-red); border: none; }

.wiki-preview-body {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-md) var(--space-lg);
  font-size: 0.88rem;
  line-height: 1.8;
}
.wiki-content :deep(h1) { font-size: 1.3rem; font-weight: 700; margin: 0 0 var(--space-md); }
.wiki-content :deep(h2) { font-size: 1.1rem; font-weight: 700; margin: var(--space-lg) 0 var(--space-sm); border-bottom: 1px solid var(--border-color); padding-bottom: 4px; }
.wiki-content :deep(h3) { font-size: 1rem; font-weight: 600; margin: var(--space-md) 0 var(--space-xs); }
.wiki-content :deep(p) { margin: var(--space-sm) 0; color: var(--text-secondary); }
.wiki-content :deep(code) { background: var(--bg-card); padding: 2px 6px; border-radius: 4px; font-size: 0.82rem; font-family: var(--font-mono); }
.wiki-content :deep(pre) { background: var(--bg-card); padding: var(--space-md); border-radius: var(--radius-md); overflow-x: auto; font-size: 0.8rem; }
.wiki-content :deep(pre code) { background: none; padding: 0; }
.wiki-content :deep(ul), .wiki-content :deep(ol) { padding-left: var(--space-lg); color: var(--text-secondary); }
.wiki-content :deep(li) { margin: 4px 0; }
.wiki-content :deep(blockquote) { border-left: 3px solid var(--accent-purple); padding-left: var(--space-md); color: var(--text-tertiary); font-style: italic; margin: var(--space-md) 0; }
.wiki-content :deep(.katex) { font-size: 1.05em; }
.wiki-content :deep(.katex-display) { margin: var(--space-md) 0; overflow-x: auto; }
.wiki-content :deep(table) { width: 100%; border-collapse: collapse; margin: var(--space-md) 0; font-size: 0.82rem; }
.wiki-content :deep(th) { background: var(--bg-card); padding: 6px 12px; text-align: left; font-weight: 600; border-bottom: 2px solid var(--border-color); }
.wiki-content :deep(td) { padding: 6px 12px; border-bottom: 1px solid var(--border-color); }
.wiki-content :deep(a) { color: var(--accent-purple); text-decoration: none; }
.wiki-content :deep(a:hover) { text-decoration: underline; }

.wiki-empty {
  text-align: center;
  color: var(--text-tertiary);
  padding: var(--space-2xl);
}

.wiki-preview-actions {
  display: flex;
  gap: var(--space-sm);
  justify-content: flex-end;
  padding: var(--space-sm) var(--space-md);
  border-top: 1px solid var(--border-color);
  background: var(--bg-primary);
}

/* slide animation */
.wiki-slide-enter-active { transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1); }
.wiki-slide-leave-active { transition: all 0.2s ease-in; }
.wiki-slide-enter-from { opacity: 0; max-height: 0; transform: translateY(-8px); }
.wiki-slide-enter-to { opacity: 1; max-height: 600px; transform: translateY(0); }
.wiki-slide-leave-from { opacity: 1; max-height: 600px; }
.wiki-slide-leave-to { opacity: 0; max-height: 0; transform: translateY(-4px); }
</style>
