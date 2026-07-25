<script setup lang="ts">
import { ref, watch, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { generationApi } from '@/api/generation'
import { videosApi } from '@/api/videos'
import { useSSE } from '@/composables/useSSE'
import { useCurrentUser } from '@/composables/useCurrentUser'
import { useTaskStore } from '@/stores/task'
import type { SSETaskEvent, SSEDoneEvent } from '@/types/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import CodeEditor from '@/components/common/CodeEditor.vue'
import CanvasTypewriter from '@/components/common/CanvasTypewriter.vue'
import ParamPanel from '@/components/sandbox/ParamPanel.vue'
import TaskQueue from '@/components/sandbox/TaskQueue.vue'
import { getKnowledgeNameBySlug, getStudyPathById, paths } from '@/config/studyPaths'

const route = useRoute()
const taskStore = useTaskStore()
const { connect, disconnect } = useSSE()
const { username, token } = useCurrentUser()

const requirement = ref('')
const code = ref('')
const typingActive = ref(false) // Canvas typewriter 动画进行中
const videoPath = ref('')
const videoUrl = ref('')
const generating = ref(false)
const fixing = ref(false)
const progress = ref(0)
const progressMsg = ref('')
const logOutput = ref('')
const savedToGallery = ref(false)
const currentFilename = ref('')
const publishDialogVisible = ref(false)
const publishDesc = ref('')
const publishToGallery = ref(false)
const studyWikiSlug = ref('')
const studyPathId = ref('')
// 发布时用户手动选择的标签
const publishPathId = ref('')
const publishKnowledgeSlug = ref('')
const publishKnowledgeItems = computed(() => {
  if (!publishPathId.value) return []
  const path = paths.find(p => p.id === publishPathId.value)
  if (!path) return []
  return path.chapters.flatMap(c => c.items)
})
const studySourceHint = computed(() => {
  const parts: string[] = []
  if (studyWikiSlug.value) {
    const name = getKnowledgeNameBySlug(studyWikiSlug.value) || studyWikiSlug.value
    parts.push(`${name} 知识点`)
  }
  if (studyPathId.value) {
    const name = getStudyPathById(studyPathId.value)?.name || studyPathId.value
    parts.push(`${name} 路径`)
  }
  return parts.length > 0 ? `将自动关联到【${parts.join(' / ')}】` : ''
})
const PY_BASE = import.meta.env.VITE_PYTHON_BASE ?? ''
const renderQuality = ref(localStorage.getItem('cs:render-quality') || '-qm')
// ========== 简易/高级模式 ==========
const sandboxMode = ref<'simple' | 'advanced'>((localStorage.getItem('cs:sandbox-mode') as 'simple' | 'advanced') || 'simple')
const animSpeed = ref<'slow' | 'medium' | 'fast'>('medium')
const colorTheme = ref<'dark' | 'light' | 'neon'>('dark')
const showFormulaLabel = ref(true)

function toggleSandboxMode() {
  sandboxMode.value = sandboxMode.value === 'simple' ? 'advanced' : 'simple'
  localStorage.setItem('cs:sandbox-mode', sandboxMode.value)
}

// 简易模式：生成时附带选项参数（纯前端拼字符串，不改后端）
function buildSimplePrompt(base: string): string {
  const parts = [base]
  // 速度
  if (animSpeed.value === 'slow') parts.push('动画播放速度较慢，细节清晰')
  else if (animSpeed.value === 'fast') parts.push('动画播放速度较快，流畅展示')
  // 主题
  if (colorTheme.value === 'light') parts.push('白色浅色背景')
  else if (colorTheme.value === 'neon') parts.push('霓虹赛博朋克配色，高对比度')
  // 公式标注
  if (showFormulaLabel.value) parts.push('在动画关键位置标注对应的 LaTeX 数学公式')
  return parts.join('。')
}

const inputPlaceholder = computed(() => {
  if (sandboxMode.value === 'simple') {
    return '你想生成什么数学动画？例如：傅里叶级数逼近方波、y=sin(1/x)函数图像、曼德博集合放大'
  }
  return '描述你想要的动画效果...\n\n例如：\n• 冒泡排序算法可视化\n• 傅里叶级数分解方波动画'
})

const mathQuickPrompts = [
  { label: '傅里叶变换', prompt: '傅里叶级数分解与合成的可视化动画，展示方波如何由正弦波叠加而成' },
  { label: '分形图案', prompt: '曼德博集合分形图案放大过程的可视化动画，展示自相似特性' },
  { label: '函数绘图', prompt: '绘制y=sin(1/x)在x趋近于0时的函数图像动画' },
  { label: '矩阵变换', prompt: '二维平面上的线性变换可视化动画，展示矩阵对向量的旋转和缩放效果' },
  { label: '正态分布', prompt: '正态分布概率密度函数的可视化动画，展示不同参数对分布形状的影响' },
  { label: '级数逼近', prompt: '泰勒级数多项式逼近函数的动画，展示随着阶数增加逼近效果的变化' },
]
let _activeTaskId = ''
let _aiChanging = false   // 标记正在由 AI 修改代码（触发 typewriter）
let _progressTimer: ReturnType<typeof setInterval> | null = null
let _progressTarget = 0
let _taskCompleted = false // 防止 onerror 覆盖已完成的结果
let _recoveryAttempts = 0  // 防止无限重连循环
let _nextTaskTimer: ReturnType<typeof setTimeout> | null = null // 自动启动下一个任务的定时器

// ========== 状态恢复标记（防止刷新丢失） ==========
const _isStateRestored = ref(false)

// ========== Canvas Typewriter 画笔写入效果 ==========
function onCanvasDone() {
  typingActive.value = false
}

// 监听 AI 带来的代码变更 → 触发 Canvas typewriter
watch(code, (newVal, oldVal) => {
  if (_aiChanging && newVal && newVal !== oldVal) {
    _aiChanging = false
    typingActive.value = true
  }
})

// ========== 状态持久化：离开再回来界面不变（按用户隔离） ==========
const STATE_KEY = computed(() => {
  const u = username.value || 'anon'
  return `cs:sandbox-state:${u}`
})

function saveState() {
  try {
    const state = {
      requirement: requirement.value,
      code: code.value,
      videoPath: videoPath.value,
      videoUrl: videoUrl.value,
      currentFilename: currentFilename.value,
      savedToGallery: savedToGallery.value,
      logOutput: logOutput.value,
      progress: progress.value,
      progressMsg: progressMsg.value,
      activeTaskId: _activeTaskId,
      sandboxMode: sandboxMode.value,
    }
    localStorage.setItem(STATE_KEY.value, JSON.stringify(state))
  } catch { /* ignore */ }
}

function restoreState() {
  try {
    const raw = localStorage.getItem(STATE_KEY.value)
    if (!raw) return
    const state = JSON.parse(raw)
    requirement.value = state.requirement || ''
    code.value = state.code || ''
    videoPath.value = state.videoPath || ''
    videoUrl.value = state.videoUrl || ''
    currentFilename.value = state.currentFilename || ''
    savedToGallery.value = state.savedToGallery || false
    logOutput.value = state.logOutput || ''
    _activeTaskId = state.activeTaskId || ''
    progress.value = state.progress || 0
    progressMsg.value = state.progressMsg || ''
    // 如果上次任务已完成，确保不在生成中状态
    if (progress.value >= 100) {
      generating.value = false
    }
    if (state.sandboxMode === 'simple' || state.sandboxMode === 'advanced') {
      sandboxMode.value = state.sandboxMode
    }
  } catch { /* ignore */ }
}

function startSmoothProgress(fromPct = 0) {
  stopSmoothProgress()
  progress.value = fromPct
  _progressTarget = Math.max(fromPct, 5)
  _taskCompleted = false
  _progressTimer = setInterval(() => {
    if (progress.value < _progressTarget) {
      progress.value = Math.round(progress.value + 1)
    }
    if (_progressTarget < 92) {
      _progressTarget += 0.3
    }
  }, 300)
}

function stopSmoothProgress() {
  if (_progressTimer) { clearInterval(_progressTimer); _progressTimer = null }
  _progressTarget = 0
}

function onTaskDone(success: boolean) {
  _taskCompleted = true
  stopSmoothProgress()
  progress.value = success ? 100 : progress.value
  generating.value = false
  disconnect()
  localStorage.removeItem('cs:active-task')
}

function onSSEEvent(evt: SSETaskEvent) {
  progressMsg.value = evt.message || progressMsg.value
  if ((evt as any).code) { _aiChanging = true; code.value = (evt as any).code }
  if (evt.video_path) {
    videoPath.value = evt.video_path
    videoUrl.value = evt.video_path  // 相对路径，走 Vite 代理 /videos → :8000
    currentFilename.value = evt.video_path.replace('/videos/', '')
    // 加入"我的作品"（localStorage + 服务端双写）
    try {
      const u = username.value || 'anon'
      const works = JSON.parse(localStorage.getItem(`cs:my-works:${u}`) || '[]')
      if (!works.includes(currentFilename.value)) {
        works.unshift(currentFilename.value)
        localStorage.setItem(`cs:my-works:${u}`, JSON.stringify(works.slice(0, 50)))
      }
      // 同步到服务端（跨设备持久化）
      if (username.value) {
        videosApi.syncMyWorks(username.value, [currentFilename.value]).catch(() => {})
      }
    } catch { /* ignore */ }
  }
  if (evt.log) logOutput.value += evt.log + '\n'
  if (evt.state === 'SUCCESS') {
    onTaskDone(true)
  } else if (evt.state === 'FAILURE') {
    onTaskDone(false)
  }
}

function onSSEError() {
  if (_taskCompleted) return // SSE 关闭触发的 onerror，忽略
  // SSE 连接彻底失败（重试次数耗尽），不要直接放弃——
  // _connectTaskSSE 里的错误回调会先尝试兜底轮询
  stopSmoothProgress()
  generating.value = false
}

// SSE 断连后兜底：轮询一次服务器确认任务真实状态
async function _pollAndRecoverTask(taskId: string) {
  if (_taskCompleted) return
  _recoveryAttempts++
  if (_recoveryAttempts > 5) {
    // 5 次恢复尝试均失败 → 放弃
    taskStore.updateTaskProgress(taskId, { state: 'FAILURE', message: '多次恢复失败，任务已中止' })
    onSSEError()
    _onQueueTaskDone(taskId, false)
    return
  }
  try {
    const res = await generationApi.getTaskStatus(taskId)
    const data = res.data.data
    if (!data) { onSSEError(); return }

    const state = data.state
    if (state === 'SUCCESS' || state === 'FAILURE') {
      // 任务其实已经完成了！只是 SSE 没收到事件
      taskStore.updateTaskProgress(taskId, {
        state: state as 'SUCCESS' | 'FAILURE',
        progress: state === 'SUCCESS' ? 100 : (data.progress || 0),
        message: state === 'SUCCESS' ? '已完成（后台恢复）' : '任务失败',
        video_path: data.video_path || '',
      })
      if (data.video_path) {
        videoPath.value = data.video_path
        videoUrl.value = data.video_path
        currentFilename.value = data.video_path.replace('/videos/', '')
      }
      if (data.log) logOutput.value += data.log + '\n'
      if ((data as any).code) { _aiChanging = true; code.value = (data as any).code }
      onTaskDone(state === 'SUCCESS')
      _onQueueTaskDone(taskId, state === 'SUCCESS')
    } else if (state === 'RUNNING' || state === 'PENDING' || state === 'STARTED' || state === 'PROGRESS') {
      // 任务还在运行 → 重新连接 SSE
      progressMsg.value = '连接恢复中...'
      _connectTaskSSE(taskId)
    } else {
      // UNKNOWN 或其他状态 → 标记失败让队列继续
      taskStore.updateTaskProgress(taskId, { state: 'FAILURE', message: '连接丢失且无法恢复' })
      onSSEError()
      _onQueueTaskDone(taskId, false)
    }
  } catch {
    // 网络也不通 → 放弃，标记失败
    taskStore.updateTaskProgress(taskId, { state: 'FAILURE', message: '连接丢失' })
    onSSEError()
    _onQueueTaskDone(taskId, false)
  }
}

// --- 恢复 ---
function restoreTaskFromSession() {
  const tid = localStorage.getItem('cs:active-task')
  if (!tid) return

  // 从队列中找这个任务
  const cached = taskStore.queue.find(t => t.taskId === tid)
  // 从 localStorage 恢复进度
  let savedProgress = 0
  try {
    const raw = localStorage.getItem(STATE_KEY.value)
    if (raw) {
      const state = JSON.parse(raw)
      savedProgress = state.progress || 0
      if (state.progressMsg) progressMsg.value = state.progressMsg
    }
  } catch { /* ignore */ }

  if (cached?.state === 'SUCCESS') {
    progress.value = 100
    generating.value = false
    if (cached.code) code.value = cached.code
    if (cached.videoPath) {
      videoPath.value = cached.videoPath
      videoUrl.value = cached.videoPath  // 相对路径，走 Vite 代理
      currentFilename.value = cached.videoPath.replace('/videos/', '')
    }
    return
  }
  if (cached?.state === 'FAILURE') {
    generating.value = false
    progressMsg.value = cached.message || '任务失败'
    return
  }
  // 任务可能仍在运行 → 重新建立 SSE 连接
  if (cached?.state === 'PENDING' || cached?.state === 'RUNNING') {
    _activeTaskId = tid
    generating.value = true
    const bestProgress = Math.max(savedProgress, cached?.progress || 0)
    // 估算离开期间的进度增量
    if (cached?.createdAt) {
      const elapsed = (Date.now() - cached.createdAt) / 1000
      const estimated = Math.min(92, Math.round(elapsed / 120 * 100))
      startSmoothProgress(Math.max(bestProgress, estimated))
    } else {
      startSmoothProgress(bestProgress)
    }
    progressMsg.value = cached.message || '恢复中...'
    if (cached.code) code.value = cached.code
    _connectTaskSSE(tid)
    return
  }
  // 其他状态：清理
  localStorage.removeItem('cs:active-task')
}

// --- 操作 ---
function handleGenerate() {
  if (!requirement.value.trim()) return
  const prompt = sandboxMode.value === 'simple'
    ? buildSimplePrompt(requirement.value.trim())
    : requirement.value.trim()
  startAsyncTask(
    () => generationApi.asyncGenerate(prompt, 3, renderQuality.value, username.value),
    { title: requirement.value.slice(0, 30), type: 'generate' }
  )
}

function handleRegenerateWithOptions() {
  if (!requirement.value.trim()) return
  const prompt = buildSimplePrompt(requirement.value.trim())
  startAsyncTask(
    () => generationApi.asyncGenerate(prompt, 3, renderQuality.value, username.value),
    { title: requirement.value.slice(0, 30), type: 'generate' }
  )
}

function handleRender() {
  if (!code.value.trim()) { ElMessage.warning('请先输入或生成 Manim 代码'); return }
  // 从代码中提取类名作为标题
  const classMatch = code.value.match(/class\s+(\w+)\s*\(\s*\w*Scene/)
  const title = classMatch?.[1] || '手动渲染'
  startAsyncTask(
    () => generationApi.asyncRender(code.value, renderQuality.value, username.value),
    { title, type: 'render' }
  )
}

async function handleCancelTask() {
  if (!_activeTaskId) return
  try {
    await ElMessageBox.confirm('确定要停止当前任务吗？', '取消生成', { confirmButtonText: '停止', cancelButtonText: '继续等待', type: 'warning' })
  } catch { return } // 用户取消
  try {
    disconnect()
    stopSmoothProgress()
    generating.value = false
    _recoveryAttempts = 0
    progressMsg.value = '任务已取消'
    // 尝试通知后端取消 Celery 任务
    await fetch(`${PY_BASE}/api/tasks/${_activeTaskId}`, { method: 'DELETE' }).catch(() => {})
    localStorage.removeItem('cs:active-task')
  } catch { /* ignore */ }
}

async function handleFixCode() {
  if (!code.value.trim()) return
  const err = getLastError()
  fixing.value = true
  try {
    // 把错误信息和原始需求都传给 AI（无错误时仅传需求，AI 也能优化代码）
    const res = await generationApi.fixCode(code.value, err || '请根据用户需求优化代码', requirement.value || undefined)
    const fixed = res.data.data?.code
    if (fixed && fixed !== code.value) {
      _aiChanging = true
      code.value = fixed
      ElMessage.success(err.trim() ? 'AI 已根据错误信息修复代码' : 'AI 已根据需求优化代码，请渲染验证')
    } else {
      ElMessage.info('AI 未找到需要修改的地方')
    }
  } catch { ElMessage.error('修复失败，请重试') }
  finally { fixing.value = false }
}

function openPublishDialog() {
  publishDesc.value = requirement.value.slice(0, 200)
  publishToGallery.value = false
  // 预填：优先用学习路径来源，否则清空让用户自选
  publishPathId.value = studyPathId.value || ''
  publishKnowledgeSlug.value = studyWikiSlug.value || ''
  publishDialogVisible.value = true
}

async function handlePublish() {
  // 从完整代码中提取场景类名作为智能标题（不截断，避免类名被切碎）
  const classMatch = code.value.match(/class\s+(\w+)\s*\(\s*\w*Scene/)
  const title = classMatch?.[1] || requirement.value.slice(0, 40) || '未命名作品'
  if (!token.value) { ElMessage.warning('请先登录再发布'); return }
  try {
    const body = new URLSearchParams()
    body.append('workTitle', title)
    body.append('workDesc', publishDesc.value)
    body.append('isPublic', 'true')
    body.append('code', code.value)
    body.append('previewUrl', videoUrl.value || '')
    // 如果是 Fork 的作品，传递来源 ID
    const forkSourceId = sessionStorage.getItem('cs:fork-source-id')
    if (forkSourceId) {
      body.append('sourceWorkId', forkSourceId)
      sessionStorage.removeItem('cs:fork-source-id')
    }
    // 标签：优先用用户手动选择的，其次用学习路径来源的
    const finalKnowledgeSlug = publishKnowledgeSlug.value || studyWikiSlug.value
    const finalPathId = publishPathId.value || studyPathId.value
    if (finalKnowledgeSlug) body.append('knowledgeSlug', finalKnowledgeSlug)
    if (finalPathId) body.append('pathId', finalPathId)
    const res = await fetch('/api/v1/work/publish', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token.value}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: body.toString(),
    })
    const data = await res.json()
    if (data.code === 200) {
      publishDialogVisible.value = false
      // 发布到社区 = 自动设为公开
      if (currentFilename.value) {
        videosApi.togglePublic(currentFilename.value).catch(() => {})
      }
      // 如果勾选了发布到画廊，同步收藏
      if (publishToGallery.value && currentFilename.value) {
        videosApi.saveVideo(currentFilename.value, username.value).then(() => {
          savedToGallery.value = true
        }).catch(() => {})
      }
      ElMessage.success('已发布到社区！')
    } else {
      ElMessage.error(data.msg || '发布失败')
    }
  } catch (e) { ElMessage.error('发布失败：' + (e as Error).message) }
}

async function handleSaveToGallery() {
  if (!currentFilename.value) return
  try {
    const res = await videosApi.saveVideo(currentFilename.value, username.value)
    savedToGallery.value = res.data.data?.saved ?? false
    ElMessage.success(savedToGallery.value ? '已收藏' : '已取消收藏')
  } catch { ElMessage.error('操作失败') }
}

function getLastError(): string {
  const lines = logOutput.value.split('\n')
  const errStart = lines.findIndex(l => l.includes('Traceback') || l.includes('Error') || l.includes('❌'))
  if (errStart >= 0) return lines.slice(errStart).join('\n')
  return logOutput.value.slice(-500)
}

// --- 异步任务核心 ---
async function startAsyncTask(apiCall: () => Promise<any>, options?: { title?: string; type?: 'generate' | 'render' | 'template' }) {
  try {
    const res = await apiCall()
    const taskId = res.data.data?.task_id
    if (!taskId) return

    // 加入任务队列
    const title = options?.title || requirement.value || '渲染任务'
    const type = options?.type || 'render'
    const task = taskStore.addTask({
      taskId,
      title,
      type,
      code: code.value,
      prompt: requirement.value,
    })

    // 如果这个任务被标记为运行中（队列第一个），建立 SSE 连接
    if (task.state === 'RUNNING') {
      _connectTaskSSE(taskId)
      generating.value = true
      startSmoothProgress(0)
    }
  } catch {
    ElMessage.error('任务提交失败')
  }
}

// 建立单个任务的 SSE 连接
function _connectTaskSSE(taskId: string) {
  _activeTaskId = taskId
  _recoveryAttempts = 0  // 新连接 → 重置恢复计数
  localStorage.setItem('cs:active-task', taskId)
  taskStore.markTaskRunning(taskId)

  connect(taskId, (data) => {
    if ((data as SSEDoneEvent).type === 'done') {
      taskStore.updateTaskProgress(taskId, { state: 'SUCCESS' })
      _onQueueTaskDone(taskId, true)
      return
    }
    // 更新 store 中的进度
    taskStore.updateTaskProgress(taskId, {
      state: (data as SSETaskEvent).state,
      progress: (data as SSETaskEvent).progress,
      message: (data as SSETaskEvent).message,
      video_path: (data as SSETaskEvent).video_path,
    })
    // 同步到沙箱当前显示（如果是当前活跃任务）
    if (taskId === _activeTaskId) {
      onSSEEvent(data as SSETaskEvent)
    }
  }, () => {
    // SSE 连接彻底失败（重试次数耗尽）→ 兜底轮询确认任务真实状态
    if (taskId === _activeTaskId) {
      _pollAndRecoverTask(taskId)
    }
  })
}

// 队列中的任务完成后，自动启动下一个（FIFO）
function _onQueueTaskDone(taskId: string, success: boolean) {
  if (taskId === _activeTaskId) {
    onTaskDone(success)
  }
  disconnect()

  // 清理之前的定时器
  if (_nextTaskTimer) {
    clearTimeout(_nextTaskTimer)
    _nextTaskTimer = null
  }

  // 找下一个排队任务，显式提升为 RUNNING 并连接 SSE
  // （不在 updateTaskProgress 里 auto-promote，否则任务变 RUNNING 却没有 SSE 连接）
  const next = taskStore.nextPendingTask
  if (next) {
    taskStore.markTaskRunning(next.taskId)
    _nextTaskTimer = setTimeout(() => {
      _connectTaskSSE(next.taskId)
      generating.value = true
      startSmoothProgress(next.progress || 0)
      _nextTaskTimer = null
    }, 500)
  }
}

// 从队列加载任务结果到沙箱
function loadTaskFromQueue(taskId: string) {
  const task = taskStore.loadTaskResult(taskId)
  if (!task) return

  // 重置状态
  generating.value = false
  savedToGallery.value = false
  logOutput.value = ''

  if (task.code) {
    _aiChanging = true
    code.value = task.code
  }
  if (task.prompt) {
    requirement.value = task.prompt
  }
  if (task.videoPath) {
    videoPath.value = task.videoPath
    videoUrl.value = task.videoPath  // 相对路径，走 Vite 代理
    currentFilename.value = task.videoPath.replace('/videos/', '')
  } else {
    videoPath.value = ''
    videoUrl.value = ''
    currentFilename.value = ''
  }
  progress.value = task.progress
  progressMsg.value = task.message
  ElMessage.success('已加载任务结果')
}

onMounted(() => {
  // 1. 先恢复任务队列
  taskStore.restore()
  // 2. 恢复本地存储的沙箱状态（代码、视频、设置、进度）
  restoreState()
  // 3. 恢复正在进行的任务（重连SSE）
  restoreTaskFromSession()
  // 4. 标记状态恢复完成！！！核心：没等恢复完就被后面的逻辑清了
  _isStateRestored.value = true

  // ========== 下面处理跳转参数，必须等状态恢复完再处理 ==========
  // 处理Fork参数：Fork优先级最高，只要session里有forkedCode就无条件覆盖
  const forkedCode = sessionStorage.getItem('cs:forked-code')
  if (forkedCode) {
    // 停止当前所有生成任务
    disconnect()
    stopSmoothProgress()
    generating.value = false
    // 清空旧状态
    videoUrl.value = ''
    videoPath.value = ''
    currentFilename.value = ''
    logOutput.value = ''
    typingActive.value = false
    progress.value = 0
    progressMsg.value = ''
    savedToGallery.value = false
    localStorage.removeItem('cs:active-task')
    // Fork 代码覆盖
    code.value = forkedCode
    sandboxMode.value = 'advanced'
    // 清空旧需求描述和来源标签
    requirement.value = ''
    studyWikiSlug.value = ''
    studyPathId.value = ''
    // 删掉 forkedCode 避免刷新重复覆盖，保留 cs:fork-source-id 给发布用
    sessionStorage.removeItem('cs:forked-code')
  } else {
    sessionStorage.removeItem('cs:fork-source-id')
    sessionStorage.removeItem('cs:forked-code')
  }

  // 读取来源标签
  studyWikiSlug.value = (route.query.wikiSlug as string) || ''
  studyPathId.value = (route.query.pathId as string) || ''

  // 处理模板跳转参数，有恢复内容就不覆盖
  if (route.query.template && forkedCode && !code.value && !videoUrl.value) {
    requirement.value = `模板创作: ${route.query.template}`
    videoUrl.value = ''
    videoPath.value = ''
    currentFilename.value = ''
    logOutput.value = ''
    typingActive.value = false
    localStorage.removeItem('cs:active-task')
  }

  // 处理路由带的prompt：只有满足以下条件才触发新生成：
  // 条件1：状态已经恢复完成
  // 条件2：url里的prompt和当前恢复出来的requirement不一样（真的是新跳转，不是刷新）
  // 条件3：当前没有正在生成的任务，也没有已经生成好的视频
  const prompt = route.query.prompt as string
  if (prompt && _isStateRestored.value && prompt !== requirement.value && !generating.value && !videoUrl.value) {
    disconnect()
    stopSmoothProgress()
    requirement.value = prompt
    code.value = ''
    videoUrl.value = ''
    videoPath.value = ''
    currentFilename.value = ''
    logOutput.value = ''
    typingActive.value = false
    sessionStorage.removeItem('cs:fork-source-id')
    localStorage.removeItem('cs:active-task')
    nextTick(() => handleGenerate())
  }
})

// 监听路由参数变化（同一组件内跳转时 onMounted 不触发）
watch(
  () => route.query.prompt,
  (newPrompt, oldPrompt) => {
    // 只有状态恢复完、新prompt和当前内容不一样、没有正在生成/已生成的视频，才触发新生成
    if (_isStateRestored.value && newPrompt && newPrompt !== oldPrompt && newPrompt !== requirement.value && !generating.value && !videoUrl.value) {
      disconnect()
      stopSmoothProgress()
      generating.value = false
      requirement.value = newPrompt as string
      code.value = ''
      videoUrl.value = ''
      videoPath.value = ''
      currentFilename.value = ''
      logOutput.value = ''
      typingActive.value = false
      studyWikiSlug.value = (route.query.wikiSlug as string) || ''
      studyPathId.value = (route.query.pathId as string) || ''
      sessionStorage.removeItem('cs:fork-source-id')
      localStorage.removeItem('cs:active-task')
      nextTick(() => handleGenerate())
    }
  }
)

// 自动保存：code、requirement、videoUrl 变化时即时持久化
let _autoSaveTimer: ReturnType<typeof setTimeout> | null = null
function autoSave() {
  if (_autoSaveTimer) clearTimeout(_autoSaveTimer)
  _autoSaveTimer = setTimeout(() => saveState(), 500)
}
watch([code, requirement, videoUrl], autoSave)

onUnmounted(() => {
  disconnect()
  stopSmoothProgress()
  if (_nextTaskTimer) {
    clearTimeout(_nextTaskTimer)
    _nextTaskTimer = null
  }
  if (_autoSaveTimer) clearTimeout(_autoSaveTimer)
  saveState()
})
</script>

<template>
  <div class="sandbox-page">
    <div class="sb-toolbar">
      <h1 class="sb-title"><el-icon :size="22"><EditPen /></el-icon> AI动画创作台</h1>
      <div class="sb-actions">
        <div class="mode-toggle">
          <el-button size="small" :type="sandboxMode === 'simple' ? 'primary' : 'default'" round @click="toggleSandboxMode">
            {{ sandboxMode === 'simple' ? '🎨 简易模式' : '🔧 高级模式' }}
          </el-button>
        </div>
        <el-select v-show="sandboxMode === 'advanced'" v-model="renderQuality" size="small" style="width:110px" @change="(v: string) => localStorage.setItem('cs:render-quality', v)">
          <el-option label="⚡ 480p" value="-ql" />
          <el-option label="🎯 720p" value="-qm" />
          <el-option label="✨ 1080p" value="-qh" />
        </el-select>
        <el-button :loading="generating" type="primary" round @click="handleGenerate">
          <el-icon><MagicStick /></el-icon> AI 生成
        </el-button>
        <el-button :loading="generating" round @click="handleRender" :disabled="!code">
          <el-icon><VideoPlay /></el-icon> 渲染
        </el-button>
      </div>
    </div>

    <div v-if="generating" class="progress-bar-wrap">
      <el-progress :percentage="progress" :color="'#7c3aed'" :stroke-width="6" />
      <span class="progress-msg">{{ progressMsg || '生成中...' }}</span>
      <el-button size="small" type="danger" plain round @click="handleCancelTask" style="flex-shrink:0">
        <el-icon><Close /></el-icon> 取消
      </el-button>
    </div>

    <div class="sb-panels" :class="{ 'sb-panels-simple': sandboxMode === 'simple' }">
      <div class="sb-panel panel-chat">
        <div class="panel-header">
          <el-icon><ChatDotRound /></el-icon>
          {{ sandboxMode === 'simple' ? '描述你想生成的数学动画' : 'AI 对话助手' }}
        </div>
        <div class="panel-body">
          <el-input v-model="requirement" type="textarea" :rows="sandboxMode === 'simple' ? 5 : 6"
            :placeholder="inputPlaceholder"
            class="req-input" />
          <!-- 简易模式：数学快捷提示 -->
          <div v-if="sandboxMode === 'simple'" class="quick-prompts">
            <span class="qp-label">🔥 热门示例：</span>
            <el-tag v-for="t in mathQuickPrompts" :key="t.label"
              size="small" class="qp-tag" @click="requirement = t.prompt">{{ t.label }}</el-tag>
          </div>
          <!-- 高级模式：原有CS快捷提示 -->
          <div v-else class="quick-prompts">
            <span class="qp-label">快速模板：</span>
            <el-tag v-for="t in ['快速排序','Dijkstra算法','傅里叶变换','正态分布','二叉树遍历','矩阵旋转','Floyd算法','二分查找','链表','傅里叶级数']" :key="t"
              size="small" class="qp-tag" @click="requirement = t + '动画可视化'">{{ t }}</el-tag>
          </div>
        </div>
      </div>

      <div v-show="sandboxMode === 'advanced'" class="sb-panel panel-code">
        <div class="panel-header">
          <el-icon><Document /></el-icon> Manim 代码
          <el-tooltip :content="requirement.trim() ? 'AI 将参考左侧需求描述修复代码' : '先在左侧输入动画需求，AI 修复效果更好'" placement="bottom" :show-after="300">
            <el-button link size="small" :loading="fixing" @click="handleFixCode" style="margin-left:auto">
              <el-icon><MagicStick /></el-icon> AI 修复
            </el-button>
          </el-tooltip>
        </div>
        <div class="panel-body code-panel-body" style="position:relative">
          <CodeEditor v-if="!typingActive" v-model="code" :readonly="false" />
          <!-- Canvas 画笔覆盖层 -->
          <CanvasTypewriter
            v-if="typingActive"
            :code="code"
            :active="typingActive"
            @done="onCanvasDone"
          />
        </div>
      </div>

      <div class="sb-panel panel-preview">
        <div class="preview-section">
          <div class="panel-header"><el-icon><VideoCamera /></el-icon> 预览</div>
          <div class="preview-body">
            <div v-if="videoUrl" class="video-player">
              <video :src="videoUrl" controls autoplay loop class="preview-video" />
              <div style="display:flex;gap:8px;margin-top:8px">
                <el-button :type="savedToGallery ? 'warning' : 'default'" size="small" round @click="handleSaveToGallery">
                  <el-icon><StarFilled v-if="savedToGallery" /><Star v-else /></el-icon>
                  {{ savedToGallery ? '已收藏' : '收藏' }}
                </el-button>
                <el-button size="small" type="success" round @click="openPublishDialog">
                  <el-icon><Upload /></el-icon> 发布到社区
                </el-button>
              </div>
              <!-- 简易模式：零代码调节选项 -->
              <div v-if="sandboxMode === 'simple'" class="simple-options">
                <div class="so-title">🎛️ 动画调节</div>
                <div class="so-row">
                  <span class="so-label">动画速度：</span>
                  <el-radio-group v-model="animSpeed" size="small">
                    <el-radio-button value="slow">慢</el-radio-button>
                    <el-radio-button value="medium">中</el-radio-button>
                    <el-radio-button value="fast">快</el-radio-button>
                  </el-radio-group>
                </div>
                <div class="so-row">
                  <span class="so-label">颜色主题：</span>
                  <el-radio-group v-model="colorTheme" size="small">
                    <el-radio-button value="dark">深色</el-radio-button>
                    <el-radio-button value="light">浅色</el-radio-button>
                    <el-radio-button value="neon">霓虹</el-radio-button>
                  </el-radio-group>
                </div>
                <div class="so-row">
                  <span class="so-label">显示公式标注：</span>
                  <el-switch v-model="showFormulaLabel" size="small" />
                </div>
                <el-button type="primary" round size="small" :loading="generating" @click="handleRegenerateWithOptions" class="so-regenerate-btn">
                  <el-icon><MagicStick /></el-icon> 重新生成
                </el-button>
              </div>
            </div>
            <div v-else class="preview-empty">
              <el-icon :size="48"><VideoCamera /></el-icon>
              <p>{{ sandboxMode === 'simple' ? '输入描述后点击生成，AI 将为你创建数学动画' : '生成动画后将在此处预览' }}</p>
            </div>
          </div>
        </div>
        <ParamPanel v-show="sandboxMode === 'advanced'" :code="code" @update:code="(v: string) => { code = v }" @render="handleRender" />
        <TaskQueue @load-task="loadTaskFromQueue" />
        <div v-if="logOutput" class="log-section">
          <div class="panel-header"><el-icon><Document /></el-icon> 渲染日志</div>
          <div class="log-body"><pre>{{ logOutput }}</pre></div>
        </div>
      </div>
    </div>

    <!-- 发布到社区弹窗 -->
    <el-dialog v-model="publishDialogVisible" title="发布到社区" width="500px">
      <div v-if="studySourceHint" class="publish-source-hint">🔗 {{ studySourceHint }}</div>
      <el-input v-model="publishDesc" type="textarea" :rows="3" placeholder="写一段描述介绍你的作品..." />
      <!-- 标签选择 -->
      <div class="publish-tags">
        <div class="publish-tags-label">🏷️ 作品标签（选填，帮助更多人发现你的作品）</div>
        <div class="publish-tags-row">
          <el-select v-model="publishPathId" placeholder="选择知识合辑" size="small" clearable
            @change="publishKnowledgeSlug = ''" style="width:100%">
            <el-option v-for="p in paths" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </div>
        <div class="publish-tags-row">
          <el-select v-model="publishKnowledgeSlug" placeholder="选择具体知识点（可选）" size="small" clearable
            :disabled="!publishPathId" style="width:100%">
            <el-option v-for="item in publishKnowledgeItems" :key="item.wikiSlug"
              :label="`${item.name} (${item.difficulty})`" :value="item.wikiSlug" />
          </el-select>
        </div>
      </div>
      <el-checkbox v-model="publishToGallery" style="margin-top:12px">同时发布到画廊</el-checkbox>
      <template #footer>
        <el-button @click="publishDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handlePublish">发布</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
/* ====== Canvas 画布风格沙箱 ====== */
.sandbox-page {
  padding: var(--space-lg); max-width: 1600px; margin: 0 auto;
  min-height: calc(100vh - var(--header-height));
  position: relative;
  /* 画布底色 */
  background:
    /* 噪点纹理 */
    repeating-conic-gradient(rgba(255,255,255,0.008) 0% 25%, transparent 0% 50%) 50% / 3px 3px,
    /* 暖灰画布 */
    var(--bg-primary);
}
[data-theme="light"] .sandbox-page {
  background:
    repeating-conic-gradient(rgba(0,0,0,0.02) 0% 25%, transparent 0% 50%) 50% / 3px 3px,
    #faf8f5;
}

/* 画布网格点阵 */
.sandbox-page::before {
  content: ''; position: absolute; inset: 0; pointer-events: none; z-index: 0;
  background-image: radial-gradient(circle, rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 24px 24px;
  mask-image: radial-gradient(ellipse at 50% 0%, black 40%, transparent 80%);
}
[data-theme="light"] .sandbox-page::before {
  background-image: radial-gradient(circle, rgba(0,0,0,0.08) 1px, transparent 1px);
}

/* ====== 工具栏 — 调色板风格 ====== */
.sb-toolbar {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: var(--space-md); position: relative; z-index: 1;
  padding: 10px 20px;
  background: linear-gradient(180deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);
  border: 1.5px solid var(--border-color); border-radius: var(--radius-xl);
  backdrop-filter: blur(16px);
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
}
[data-theme="light"] .sb-toolbar {
  background: linear-gradient(180deg, #fff 0%, #faf8f5 100%);
  border-color: #d4c8b8;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.sb-title {
  font-size: 1.1rem; font-weight: 800; display: flex; align-items: center; gap: var(--space-sm);
  background: var(--gradient-primary);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  letter-spacing: -0.01em;
}
.sb-actions { display: flex; gap: var(--space-sm); align-items: center; }

/* 进度条 — 颜料涂抹 */
.progress-bar-wrap {
  margin-bottom: var(--space-md); display: flex; align-items: center; gap: var(--space-md);
  padding: var(--space-sm) var(--space-lg);
  border-radius: var(--radius-xl); border: 1.5px solid var(--border-color);
  position: relative; z-index: 1;
  background: linear-gradient(135deg, rgba(124,58,237,0.06) 0%, rgba(6,182,212,0.04) 100%);
  animation: scale-in 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
  box-shadow: 0 2px 16px rgba(124,58,237,0.06);
}
.progress-bar-wrap :deep(.el-progress-bar__outer) { background: rgba(255,255,255,0.05); overflow: hidden; border-radius: var(--radius-full); }
.progress-bar-wrap :deep(.el-progress-bar__inner) {
  background: linear-gradient(90deg, var(--accent-purple), var(--accent-blue), var(--accent-cyan));
  background-size: 200% 100%; animation: gradient-shift 2s linear infinite;
}
.progress-msg { color: var(--text-secondary); font-size: 0.85rem; white-space: nowrap; flex: 1; }

@keyframes gradient-shift { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }

/* 三栏画架布局 */
.sb-panels {
  display: grid; grid-template-columns: 1fr 1fr 1.6fr;
  gap: var(--space-md); height: calc(100vh - 220px);
  position: relative; z-index: 1;
}

/* 面板 — 画框风格 */
.sb-panel {
  display: flex; flex-direction: column;
  background: linear-gradient(180deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
  border-radius: var(--radius-xl);
  border: 2px solid rgba(255,255,255,0.06);
  overflow: hidden; transition: all 0.3s ease;
  backdrop-filter: blur(8px);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.03),
    0 4px 24px rgba(0,0,0,0.1);
}
[data-theme="light"] .sb-panel {
  background: #fffefc;
  border: 2px solid #d4c8b8;
  box-shadow:
    inset 0 0 20px rgba(139,119,90,0.04),
    0 4px 20px rgba(0,0,0,0.04);
}
.sb-panel:hover {
  border-color: rgba(124,58,237,0.3);
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.05),
    0 8px 32px rgba(124,58,237,0.08);
}
[data-theme="light"] .sb-panel:hover { border-color: rgba(124,58,237,0.25); }

.panel-preview {
  display: flex;
  flex-direction: column;
}
.panel-preview :deep(.param-panel) {
  margin: var(--space-sm);
  flex-shrink: 0;
}
.panel-preview :deep(.task-queue) {
  margin: 0 var(--space-sm) var(--space-sm);
  flex-shrink: 0;
}

.panel-header {
  padding: 12px 16px; font-size: 0.8rem; font-weight: 650;
  color: var(--text-secondary); display: flex; align-items: center; gap: 8px;
  border-bottom: 1px solid var(--border-color);
  background: rgba(255,255,255,0.02);
  letter-spacing: 0.02em; text-transform: uppercase; font-size: 0.72rem;
}
[data-theme="light"] .panel-header { background: rgba(0,0,0,0.015); }
.panel-body { flex: 1; overflow: auto; padding: var(--space-md); }

/* AI 对话面板 — 素描纸感 */
.panel-chat .panel-body {
  background:
    linear-gradient(rgba(255,255,255,0.01) 1px, transparent 1px);
  background-size: 100% 28px;
}
.req-input :deep(.el-textarea__inner) {
  background: rgba(255,255,255,0.03); color: var(--text-primary);
  border: 1.5px dashed rgba(255,255,255,0.1); font-size: 0.9rem; resize: none;
  border-radius: var(--radius-lg); line-height: 1.6; padding: var(--space-md);
  transition: all 0.3s ease;
  font-style: italic;
}
[data-theme="light"] .req-input :deep(.el-textarea__inner) {
  background: rgba(0,0,0,0.01); border: 1.5px dashed #c8bda8;
}
.req-input :deep(.el-textarea__inner:focus) {
  border-color: var(--accent-purple); border-style: solid;
  box-shadow: 0 0 0 4px rgba(124,58,237,0.06);
  font-style: normal;
}
.quick-prompts { margin-top: var(--space-md); }
.qp-label { font-size: 0.75rem; color: var(--text-tertiary); font-weight: 500; letter-spacing: 0.04em; text-transform: uppercase; }
.qp-tag {
  cursor: pointer; margin: 3px; font-size: 0.78rem;
  background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important;
  color: var(--text-secondary); transition: all 0.25s ease;
  border-radius: var(--radius-full);
}
.qp-tag:hover { border-color: var(--accent-purple) !important; color: var(--accent-purple-light); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(124,58,237,0.15); }

/* 代码面板 — 暗色画布 */
.code-panel-body { padding: 0; background: #161b22; }
.code-panel-body :deep(.cm-editor) { background: #161b22; }

/* 预览面板 — 整体可滚动，各模块独立堆叠 */
.panel-preview { overflow-y: auto; }
.panel-preview .panel-header { flex-shrink: 0; }
.preview-section { flex-shrink: 0; }
.preview-body {
  min-height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: var(--space-md);
}
.preview-video {
  max-width: 100%; max-height: 100%; border-radius: var(--radius-lg);
  animation: scale-in 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  border: 2px solid rgba(255,255,255,0.06);
}
.preview-empty { text-align: center; color: var(--text-tertiary); animation: fade-in 0.5s ease both; }
.preview-empty .el-icon { margin-bottom: var(--space-md); opacity: 0.15; }
.preview-empty p { font-size: 0.9rem; font-style: italic; }

/* 日志区块 */
.log-section { flex-shrink: 0; border-top: 1px solid var(--border-color); }
.log-body {
  max-height: 160px;
  overflow-y: auto;
  padding: var(--space-sm) var(--space-md);
  background: rgba(0,0,0,0.2);
}
.log-body pre { font-family: var(--font-mono); font-size: 0.7rem; color: var(--text-tertiary); white-space: pre-wrap; margin: 0; line-height: 1.5; }

@keyframes scale-in { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
@keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }

.publish-source-hint {
  font-size: 0.8rem; color: var(--accent-purple); margin-bottom: 12px;
  padding: 8px 12px; background: rgba(124,58,237,0.06);
  border-left: 3px solid var(--accent-purple); border-radius: 6px;
}
.publish-tags {
  margin-top: 14px; padding: 12px;
  background: var(--bg-secondary); border-radius: var(--radius-md);
}
.publish-tags-label {
  font-size: 0.78rem; color: var(--text-tertiary); margin-bottom: 8px;
}
.publish-tags-row {
  margin-bottom: 6px;
}
.publish-tags-row:last-child { margin-bottom: 0; }

/* ====== 模式切换 ====== */
.mode-toggle {
  display: flex; align-items: center;
}
.mode-toggle .el-button {
  font-weight: 600; padding: 6px 18px;
}

/* 简易模式：两栏布局 */
.sb-panels-simple {
  grid-template-columns: 1fr 1fr !important;
}
.sb-panels-simple .panel-chat { grid-column: span 1; }

/* ====== 简易模式：零代码调节选项 ====== */
.simple-options {
  margin-top: 12px; padding: 14px 16px;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
}
[data-theme="light"] .simple-options {
  background: rgba(0,0,0,0.02);
}
.so-title {
  font-size: 0.82rem; font-weight: 650; color: var(--text-primary); margin-bottom: 10px;
}
.so-row {
  display: flex; align-items: center; justify-content: space-between; gap: 8px;
  margin-bottom: 8px;
}
.so-label {
  font-size: 0.78rem; color: var(--text-secondary); white-space: nowrap;
}
.so-regenerate-btn {
  margin-top: 8px; width: 100%;
}

@media (max-width: 1024px) {
  .sb-panels { grid-template-columns: 1fr; height: auto; }
  .sb-panels-simple { grid-template-columns: 1fr !important; }
  .sb-panel { min-height: 320px; }
}
</style>
