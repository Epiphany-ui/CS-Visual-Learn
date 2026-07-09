<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { generationApi } from '@/api/generation'
import { useSSE } from '@/composables/useSSE'
import { useTaskStore } from '@/stores/task'
import type { SSETaskEvent, SSEDoneEvent } from '@/types/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const taskStore = useTaskStore()
const { connect, disconnect } = useSSE()

// 三栏状态
const requirement = ref('')
const code = ref('')
const videoPath = ref('')
const videoUrl = ref('')
const generating = ref(false)
const progress = ref(0)
const progressMsg = ref('')
const logOutput = ref('')
const activeTab = ref<'生成' | '渲染' | '修复'>('生成')

// Monaco Editor 占位
const codeEditorContent = ref('')

function handleGenerate() {
  if (!requirement.value.trim()) return
  activeTab.value = '生成'
  startAsyncTask(() => generationApi.asyncGenerate(requirement.value.trim()))
}

function handleRender() {
  if (!code.value.trim()) { ElMessage.warning('请先输入或生成 Manim 代码'); return }
  activeTab.value = '渲染'
  startAsyncTask(() => generationApi.asyncRender(code.value))
}

function handleGenerateCode() {
  if (!requirement.value.trim()) return
  activeTab.value = '生成'
  startAsyncTask(() => generationApi.asyncGenerate(requirement.value.trim()))
}

async function startAsyncTask(apiCall: () => Promise<any>) {
  generating.value = true
  progress.value = 0
  videoPath.value = ''
  logOutput.value = ''
  try {
    const res = await apiCall()
    const taskId = res.data.data?.task_id
    if (taskId) {
      taskStore.startTask(taskId)
      connect(taskId, (data) => {
        if ((data as SSEDoneEvent).type === 'done') {
          generating.value = false
          disconnect()
          return
        }
        const evt = data as SSETaskEvent
        progress.value = evt.progress
        progressMsg.value = evt.message
        if (evt.video_path) {
          videoPath.value = evt.video_path
          videoUrl.value = `http://localhost:8000${evt.video_path}`
        }
        if (evt.log) {
          logOutput.value += evt.log + '\n'
        }
        taskStore.updateProgress(evt)
        if (evt.state === 'SUCCESS' || evt.state === 'FAILURE') {
          generating.value = false
          disconnect()
        }
      }, () => {
        generating.value = false
        ElMessage.error('SSE 连接失败')
      })
    }
  } catch {
    generating.value = false
  }
}

// 从首页跳转带 prompt 参数
onMounted(() => {
  const prompt = route.query.prompt as string
  if (prompt) requirement.value = prompt
})
onUnmounted(() => disconnect())
</script>

<template>
  <div class="sandbox-page">
    <div class="sb-toolbar">
      <h1 class="sb-title">
        <el-icon :size="22"><EditPen /></el-icon> 动画沙箱
      </h1>
      <div class="sb-actions">
        <el-button :loading="generating" type="primary" round @click="handleGenerateCode">
          <el-icon><MagicStick /></el-icon> AI 生成
        </el-button>
        <el-button :loading="generating" round @click="handleRender" :disabled="!code">
          <el-icon><VideoPlay /></el-icon> 渲染
        </el-button>
      </div>
    </div>

    <!-- 进度条 -->
    <div v-if="generating" class="progress-bar-wrap">
      <el-progress :percentage="progress" :color="'#7c3aed'" :stroke-width="6" />
      <span class="progress-msg">{{ progressMsg }}</span>
    </div>

    <!-- 三栏布局 -->
    <div class="sb-panels">
      <!-- 左：AI 对话 -->
      <div class="sb-panel panel-chat">
        <div class="panel-header">
          <el-icon><ChatDotRound /></el-icon> AI 对话助手
        </div>
        <div class="panel-body">
          <el-input
            v-model="requirement"
            type="textarea"
            :rows="6"
            placeholder="描述你想要的动画效果...&#10;&#10;例如：&#10;• 冒泡排序算法可视化&#10;• 傅里叶级数分解方波动画&#10;• 二叉树前中后序遍历对比"
            class="req-input"
          />
          <div class="quick-prompts">
            <span class="qp-label">快速模板：</span>
            <el-tag v-for="t in ['快速排序','Dijkstra算法','傅里叶变换','正态分布','二叉树遍历']" :key="t"
              size="small" class="qp-tag" @click="requirement = t + '动画可视化'"
            >{{ t }}</el-tag>
          </div>
        </div>
      </div>

      <!-- 中：代码编辑器 -->
      <div class="sb-panel panel-code">
        <div class="panel-header">
          <el-icon><Document /></el-icon> Manim 代码
        </div>
        <div class="panel-body">
          <textarea
            v-model="code"
            class="code-editor"
            placeholder="# AI 生成的 Manim 代码将显示在这里..."
            spellcheck="false"
          ></textarea>
        </div>
      </div>

      <!-- 右：视频预览 -->
      <div class="sb-panel panel-preview">
        <div class="panel-header">
          <el-icon><VideoCamera /></el-icon> 预览
        </div>
        <div class="panel-body preview-body">
          <div v-if="videoUrl" class="video-player">
            <video :src="videoUrl" controls autoplay loop class="preview-video">
              你的浏览器不支持视频播放
            </video>
          </div>
          <div v-else class="preview-empty">
            <el-icon :size="48"><VideoCamera /></el-icon>
            <p>生成动画后将在此处预览</p>
          </div>
        </div>
        <!-- 日志 -->
        <div v-if="logOutput" class="panel-log">
          <pre>{{ logOutput }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sandbox-page { padding: var(--space-lg); max-width: 1500px; margin: 0 auto; }
.sb-toolbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--space-md); }
.sb-title { font-size: 1.3rem; font-weight: 800; display: flex; align-items: center; gap: var(--space-sm); background: var(--gradient-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.sb-actions { display: flex; gap: var(--space-sm); }

.progress-bar-wrap { margin-bottom: var(--space-md); display: flex; align-items: center; gap: var(--space-md); background: var(--bg-card); padding: var(--space-sm) var(--space-md); border-radius: var(--radius-md); border: 1px solid var(--border-color); }
.progress-bar-wrap :deep(.el-progress-bar__outer) { background: var(--bg-secondary); }
.progress-msg { color: var(--text-secondary); font-size: 0.85rem; white-space: nowrap; }

.sb-panels { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: var(--space-md); height: calc(100vh - 180px); }
.sb-panel { display: flex; flex-direction: column; border: 1px solid var(--border-color); border-radius: var(--radius-lg); background: var(--bg-card); overflow: hidden; }
.panel-header { padding: 10px var(--space-md); font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); display: flex; align-items: center; gap: 6px; border-bottom: 1px solid var(--border-color); background: var(--bg-secondary); }
.panel-body { flex: 1; overflow: auto; padding: var(--space-md); }

.req-input :deep(.el-textarea__inner) { background: transparent; color: var(--text-primary); border: 1px solid var(--border-color); font-size: 0.9rem; resize: none; }
.quick-prompts { margin-top: var(--space-md); }
.qp-label { font-size: 0.78rem; color: var(--text-tertiary); }
.qp-tag { cursor: pointer; margin: 3px; background: var(--bg-card-hover) !important; border-color: var(--border-color) !important; color: var(--text-secondary); transition: all var(--transition-fast); }
.qp-tag:hover { border-color: var(--accent-purple) !important; color: var(--accent-purple-light); }

.code-editor { width: 100%; height: 100%; background: var(--bg-secondary); color: var(--text-primary); border: none; padding: var(--space-md); font-family: var(--font-mono); font-size: 0.82rem; line-height: 1.5; resize: none; outline: none; tab-size: 4; }

.preview-body { display: flex; align-items: center; justify-content: center; flex-direction: column; }
.preview-video { max-width: 100%; max-height: 100%; border-radius: var(--radius-md); }
.preview-empty { text-align: center; color: var(--text-tertiary); }
.preview-empty .el-icon { margin-bottom: var(--space-md); opacity: 0.3; }
.preview-empty p { font-size: 0.9rem; }
.panel-log { max-height: 120px; overflow-y: auto; padding: var(--space-sm) var(--space-md); background: var(--bg-secondary); border-top: 1px solid var(--border-color); }
.panel-log pre { font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-tertiary); white-space: pre-wrap; margin: 0; }

@media (max-width: 1024px) { .sb-panels { grid-template-columns: 1fr; height: auto; } .sb-panel { min-height: 300px; } }
</style>
