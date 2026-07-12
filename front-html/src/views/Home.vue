<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import StatCard from '@/components/common/StatCard.vue'
import RevealOnScroll from '@/components/common/RevealOnScroll.vue'
import AnimatedCounter from '@/components/common/AnimatedCounter.vue'

const router = useRouter()
const inputRequirement = ref('')
const heroReady = ref(false)
const categoriesRef = ref<HTMLElement | null>(null)

onMounted(() => {
  requestAnimationFrame(() => { heroReady.value = true })
})

const categories = [
  { name: '算法', icon: 'Operation', color: '#7c3aed', desc: '排序、搜索、贪心...', path: '/wiki?category=algorithm' },
  { name: '数据结构', icon: 'DataAnalysis', color: '#3b82f6', desc: '树、图、堆、哈希...', path: '/wiki?category=data-structures' },
  { name: '高等数学', icon: 'TrendCharts', color: '#06b6d4', desc: '微积分、级数、傅里叶...', path: '/wiki?category=math' },
  { name: '线性代数', icon: 'Grid', color: '#10b981', desc: '矩阵、特征值、SVD...', path: '/wiki?category=linear-algebra' },
  { name: '概率论', icon: 'PieChart', color: '#f59e0b', desc: '正态分布、贝叶斯...', path: '/wiki?category=probability' },
  { name: '图论', icon: 'Share', color: '#ec4899', desc: '最短路径、生成树...', path: '/wiki?category=graph-theory' },
]

function handleGenerate() {
  if (inputRequirement.value.trim()) {
    router.push({ path: '/sandbox', query: { prompt: inputRequirement.value.trim() } })
  }
}

function scrollToExplore() {
  const el = document.querySelector('.section-categories')
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
</script>

<template>
  <div class="home-page">
    <!-- Hero -->
    <section class="hero">
      <div class="hero-bg">
        <div class="hero-glow glow-1" />
        <div class="hero-glow glow-2" />
        <div class="hero-glow glow-3" />
        <div class="hero-grid" />
      </div>

      <div class="hero-content" :class="{ ready: heroReady }">
        <!-- 标题：每个字独立动画 -->
        <h1 class="hero-title">
          <span class="char-wrapper char-from-left" v-for="(ch, i) in '让抽象概念'" :key="'a'+i" :style="{ animationDelay: (0.1 + i * 0.06) + 's' }">{{ ch }}</span>
          <span class="char-wrapper char-bounce-in" style="animation-delay:0.7s">动</span>
          <span class="char-wrapper char-from-bottom" v-for="(ch, i) in '起来'" :key="'b'+i" :style="{ animationDelay: (0.75 + i * 0.08) + 's' }">{{ ch }}</span>
        </h1>

        <!-- 副标题：从下方飞入 -->
        <p class="hero-subtitle">
          <span class="sub-line sub-line-1">基于 AI 的可视化学习平台</span>
          <span class="sub-line sub-line-2">输入知识点，即刻生成交互式数学动画</span>
        </p>

        <!-- 搜索框：缩放入 -->
        <div class="hero-input">
          <el-input
            v-model="inputRequirement"
            size="large"
            placeholder="例如：冒泡排序动画、傅里叶级数可视化..."
            @keyup.enter="handleGenerate"
            class="hero-search"
          >
            <template #prefix><el-icon><Search /></el-icon></template>
            <template #suffix>
              <el-button type="primary" size="large" @click="handleGenerate" round class="hero-btn" v-ripple>
                <el-icon><MagicStick /></el-icon> 生成
              </el-button>
            </template>
          </el-input>
        </div>

        <!-- 标签：依次弹出 -->
        <div class="hero-tags">
          <span class="tags-label">🔥 热门：</span>
          <span
            v-for="(t, i) in ['快速排序','二叉树遍历','傅里叶变换','Dijkstra算法']"
            :key="t"
            class="hero-tag-item"
            :style="{ animationDelay: (1.5 + i * 0.12) + 's' }"
            @click="router.push({path:'/sandbox', query:{prompt:t}})"
          >{{ t }}</span>
        </div>
      </div>

      <!-- 探索更多 -->
      <div class="hero-scroll" @click="scrollToExplore">
        <span>探索更多</span>
        <el-icon :size="20"><ArrowDownBold /></el-icon>
      </div>
    </section>

    <!-- 分类导航 -->
    <section ref="categoriesRef" class="section section-categories">
      <RevealOnScroll>
        <h2 class="section-title text-gradient">探索知识领域</h2>
        <p class="section-desc">从你最感兴趣的领域开始学习之旅</p>
      </RevealOnScroll>
      <div class="category-grid">
        <RevealOnScroll v-for="(cat, i) in categories" :key="cat.name" :delay="i * 80">
          <div class="category-card glass-card" v-tilt @click="router.push(cat.path)">
            <div class="cat-icon" :style="{ color: cat.color, background: cat.color + '15', boxShadow: '0 4px 20px ' + cat.color + '25' }">
              <el-icon :size="28"><component :is="cat.icon" /></el-icon>
            </div>
            <h3 class="cat-name">{{ cat.name }}</h3>
            <p class="cat-desc">{{ cat.desc }}</p>
          </div>
        </RevealOnScroll>
      </div>
    </section>

    <!-- 统计数据 -->
    <section class="section stats-section">
      <RevealOnScroll>
        <h2 class="section-title text-gradient">平台数据</h2>
      </RevealOnScroll>
      <div class="stats-row">
        <StatCard label="知识词条" value="111" suffix="+" color="#7c3aed">
          <template #value><AnimatedCounter :target="111" :duration="1500" />+</template>
        </StatCard>
        <StatCard label="动画模板" value="10" suffix="+" color="#3b82f6">
          <template #value><AnimatedCounter :target="10" :duration="1000" />+</template>
        </StatCard>
        <StatCard label="已生成动画" value="∞" color="#06b6d4" />
        <StatCard label="知识分类" value="7" suffix="个" color="#10b981">
          <template #value><AnimatedCounter :target="7" :duration="800" />个</template>
        </StatCard>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* ====== Hero Background ====== */
.hero {
  position: relative; min-height: 92vh; display: flex;
  align-items: center; justify-content: center; overflow: hidden;
  padding: var(--space-3xl) var(--space-xl);
}
.hero-bg { position: absolute; inset: 0; pointer-events: none; }
.hero-glow {
  position: absolute; border-radius: 50%; filter: blur(140px); opacity: 0.45;
  animation: glow-drift 10s ease-in-out infinite alternate;
}
.glow-1 { width: 700px; height: 700px; background: var(--accent-purple); top: -250px; left: -150px; }
.glow-2 { width: 500px; height: 500px; background: var(--accent-blue); bottom: -200px; right: -150px; animation-delay: 3s; animation-duration: 12s; }
.glow-3 { width: 350px; height: 350px; background: var(--accent-cyan); top: 50%; left: 50%; transform: translate(-50%, -50%); animation-delay: 6s; animation-duration: 14s; opacity: 0.25; }
.hero-grid {
  position: absolute; inset: 0;
  background-image: linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
  background-size: 72px 72px;
  mask-image: radial-gradient(ellipse at 50% 40%, black 30%, transparent 70%);
}

@keyframes glow-drift {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(60px, 40px) scale(1.2); }
}

/* ====== Hero Content ====== */
.hero-content { position: relative; z-index: 2; text-align: center; max-width: 860px; }

/* 标题 — 字符拆分 */
.hero-title {
  font-size: 4.5rem; font-weight: 950; line-height: 1.2; color: var(--text-primary);
  margin-bottom: var(--space-md); letter-spacing: -0.03em;
  display: flex; flex-wrap: wrap; justify-content: center; gap: 0;
}
.char-wrapper {
  display: inline-block; opacity: 0;
}

/* 从左边飞入 */
.char-from-left {
  animation: fly-from-left 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes fly-from-left {
  0% { opacity: 0; transform: translateX(-120px) rotate(-15deg) scale(0.3); filter: blur(8px); }
  60% { opacity: 1; filter: blur(0); }
  100% { opacity: 1; transform: translateX(0) rotate(0deg) scale(1); filter: blur(0); }
}

/* 从底部飞入 */
.char-from-bottom {
  animation: fly-from-bottom 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes fly-from-bottom {
  0% { opacity: 0; transform: translateY(100px) scale(0.3); filter: blur(6px); }
  70% { opacity: 1; filter: blur(0); }
  100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
}

/* "动"字 — 弹入 + 跳两下 + 流光 */
.char-bounce-in {
  display: inline-block;
  background: linear-gradient(90deg, var(--accent-purple) 0%, var(--accent-cyan) 50%, var(--accent-purple) 100%);
  background-size: 200% auto;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  animation: bounce-in 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) 0.7s forwards,
             bounce-pop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) 1.5s forwards,
             shimmer-text 3s linear 1.5s infinite;
}
@keyframes bounce-in {
  0% { opacity: 0; transform: scale(0) rotate(-30deg); }
  60% { opacity: 1; transform: scale(1.25) rotate(5deg); }
  100% { opacity: 1; transform: scale(1) rotate(0deg); }
}
@keyframes bounce-pop {
  0% { transform: scale(1); }
  50% { transform: scale(1.12); }
  100% { transform: scale(1); }
}
@keyframes shimmer-text {
  to { background-position: 200% center; }
}

/* 副标题 — 从底部淡入 */
.hero-subtitle { margin-top: var(--space-xl); font-size: 1.2rem; color: var(--text-secondary); line-height: 1.9; letter-spacing: 0.02em; }
.sub-line { display: block; opacity: 0; }
.sub-line-1 { animation: subtitle-up 0.7s cubic-bezier(0.16, 1, 0.3, 1) 0.9s forwards; }
.sub-line-2 { animation: subtitle-up 0.7s cubic-bezier(0.16, 1, 0.3, 1) 1.05s forwards; }
@keyframes subtitle-up {
  0% { opacity: 0; transform: translateY(40px); filter: blur(4px); }
  100% { opacity: 1; transform: translateY(0); filter: blur(0); }
}

/* 搜索框 — 弹入 */
.hero-input { margin-top: var(--space-2xl); max-width: 620px; margin-inline: auto; opacity: 0; animation: input-pop 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) 1.2s forwards; }
@keyframes input-pop {
  0% { opacity: 0; transform: scale(0.8) translateY(20px); }
  100% { opacity: 1; transform: scale(1) translateY(0); }
}
.hero-search :deep(.el-input__wrapper) {
  background: var(--bg-card); backdrop-filter: blur(20px); border: 1.5px solid var(--border-color-light);
  border-radius: var(--radius-full); padding: 5px 5px 5px 20px; box-shadow: 0 12px 40px rgba(0,0,0,0.2);
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.hero-search :deep(.el-input__wrapper:hover) { border-color: var(--accent-purple); transform: translateY(-1px); box-shadow: 0 16px 48px rgba(0,0,0,0.25); }
.hero-search :deep(.el-input__wrapper.is-focus) {
  border-color: var(--accent-purple); box-shadow: 0 0 0 4px rgba(124,58,237,0.15), 0 16px 48px rgba(0,0,0,0.25);
  transform: scale(1.015);
}
.hero-btn { padding: 13px 30px !important; font-weight: 650 !important; letter-spacing: 0.02em; font-size: 0.95rem !important; }

/* 标签 — 从右侧弹入 */
.hero-tags { margin-top: var(--space-xl); display: flex; align-items: center; justify-content: center; gap: var(--space-sm); flex-wrap: wrap; }
.tags-label { color: var(--text-tertiary); font-size: 0.9rem; opacity: 0; animation: tag-pop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) 1.5s forwards; }
.hero-tag-item {
  display: inline-block; padding: 6px 16px; border-radius: var(--radius-full);
  background: var(--bg-card); border: 1px solid var(--border-color);
  color: var(--text-secondary); font-size: 0.85rem; cursor: pointer;
  opacity: 0; transition: all 0.25s ease;
  animation: tag-pop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}
.hero-tag-item:hover { border-color: var(--accent-purple); color: var(--accent-purple-light); transform: translateY(-2px); box-shadow: 0 4px 16px rgba(124,58,237,0.2); }
@keyframes tag-pop {
  0% { opacity: 0; transform: translateX(30px) scale(0.7); }
  100% { opacity: 1; transform: translateX(0) scale(1); }
}

/* ====== 探索更多 ====== */
.hero-scroll {
  position: absolute; bottom: var(--space-2xl); left: 50%; transform: translateX(-50%); z-index: 2;
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  color: var(--text-tertiary); font-size: 0.82rem; letter-spacing: 0.06em;
  animation: float-scroll 2.8s ease-in-out infinite; cursor: pointer;
  transition: color 0.25s; user-select: none;
}
.hero-scroll:hover { color: var(--accent-purple-light); }
@keyframes float-scroll {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(10px); }
}

/* ====== Sections ====== */
.section { max-width: var(--max-content-width); margin: 0 auto; padding: var(--space-3xl) var(--space-xl); }
.section-title { text-align: center; font-size: 2rem; font-weight: 850; letter-spacing: -0.01em; }
.section-desc { text-align: center; margin-top: var(--space-sm); color: var(--text-tertiary); font-size: 1rem; }

.category-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-lg); margin-top: var(--space-2xl); }
.category-card { text-align: center; padding: var(--space-2xl) var(--space-xl); cursor: pointer; transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1); border-radius: var(--radius-xl); }
.category-card:hover { transform: translateY(-8px) scale(1.02); box-shadow: 0 16px 48px rgba(0,0,0,0.18); }
.cat-icon { width: 60px; height: 60px; border-radius: var(--radius-xl); display: flex; align-items: center; justify-content: center; margin: 0 auto var(--space-md); transition: all 0.35s ease; }
.category-card:hover .cat-icon { transform: scale(1.2) rotate(-8deg); }
.cat-name { font-size: 1.1rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.01em; }
.cat-desc { margin-top: var(--space-xs); color: var(--text-tertiary); font-size: 0.85rem; }

.stats-section { padding-bottom: var(--space-4xl); }
.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-lg); }

@media (max-width: 768px) {
  .hero-title { font-size: 2.2rem; }
  .category-grid { grid-template-columns: repeat(2, 1fr); }
  .stats-row { grid-template-columns: repeat(2, 1fr); }
}
</style>
