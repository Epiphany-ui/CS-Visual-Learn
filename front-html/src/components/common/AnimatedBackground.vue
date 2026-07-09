<script setup lang="ts">
defineProps<{
  particleCount?: number
}>()
</script>

<template>
  <div class="animated-bg">
    <!-- Grid layer -->
    <div class="bg-grid" />
    <!-- Floating blobs -->
    <div class="bg-blob bg-blob--1" />
    <div class="bg-blob bg-blob--2" />
    <div class="bg-blob bg-blob--3" />
    <!-- Particles -->
    <div v-if="(particleCount ?? 15) > 0" class="particle-canvas" aria-hidden="true">
      <div
        v-for="i in (particleCount ?? 15)" :key="i"
        class="particle"
        :style="{
          left: `${Math.random() * 100}%`,
          animationDuration: `${8 + Math.random() * 12}s`,
          animationDelay: `${Math.random() * 10}s`,
          width: `${1 + Math.random() * 2}px`,
          height: `${1 + Math.random() * 2}px`,
        }"
      />
    </div>
  </div>
</template>

<style scoped>
.animated-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.bg-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.12;
  animation: float-rotate 12s ease-in-out infinite;
}
.bg-blob--1 {
  width: 500px; height: 500px;
  background: var(--accent-purple);
  top: -10%; left: -5%;
  animation-delay: 0s;
}
.bg-blob--2 {
  width: 400px; height: 400px;
  background: var(--accent-blue);
  top: 40%; right: -8%;
  animation-delay: -4s;
  animation-duration: 15s;
}
.bg-blob--3 {
  width: 350px; height: 350px;
  background: var(--accent-cyan);
  bottom: -10%; left: 30%;
  animation-delay: -8s;
  animation-duration: 18s;
}
</style>
