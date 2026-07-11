<script setup lang="ts">
import { ref, computed } from 'vue'
import { useIntersectionObserver } from '@vueuse/core'

const props = withDefaults(defineProps<{
  threshold?: number
  rootMargin?: string
  delay?: number
  once?: boolean
  /** 进入方向 */
  direction?: 'up' | 'down' | 'left' | 'right' | 'none'
  /** 弹入效果 */
  bounce?: boolean
  /** 模糊渐清 */
  blur?: boolean
}>(), {
  threshold: 0.12,
  rootMargin: '0px 0px -30px 0px',
  delay: 0,
  once: true,
  direction: 'up',
  bounce: false,
  blur: false,
})

const el = ref<HTMLElement | null>(null)
const visible = ref(false)

const dirClass = computed(() => `reveal-${props.direction}`)

const { stop } = useIntersectionObserver(
  el,
  ([{ isIntersecting }]) => {
    if (isIntersecting) {
      setTimeout(() => { visible.value = true }, props.delay)
      if (props.once) stop()
    } else if (!props.once) {
      visible.value = false
    }
  },
  { threshold: props.threshold, rootMargin: props.rootMargin },
)
</script>

<template>
  <div
    ref="el"
    :class="[
      'reveal-on-scroll',
      dirClass,
      { 'reveal-bounce': bounce },
      { 'reveal-blur': blur },
      { 'is-visible': visible },
    ]"
  >
    <slot />
  </div>
</template>

<style scoped>
.reveal-on-scroll {
  opacity: 0;
  transition: all 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}
.reveal-on-scroll.reveal-blur {
  filter: blur(8px);
}
.reveal-on-scroll.is-visible {
  opacity: 1;
}
.reveal-on-scroll.reveal-blur.is-visible {
  filter: blur(0);
}

/* 方向位移 */
.reveal-up { transform: translateY(40px); }
.reveal-up.is-visible { transform: translateY(0); }

.reveal-down { transform: translateY(-40px); }
.reveal-down.is-visible { transform: translateY(0); }

.reveal-left { transform: translateX(-60px); }
.reveal-left.is-visible { transform: translateX(0); }

.reveal-right { transform: translateX(60px); }
.reveal-right.is-visible { transform: translateX(0); }

.reveal-none { transform: none; }

/* 弹性弹入 */
.reveal-bounce {
  transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.reveal-bounce.is-visible {
  transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* 延迟 */
</style>
