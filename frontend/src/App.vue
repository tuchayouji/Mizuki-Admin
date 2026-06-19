<template>
  <div class="app">
    <nav class="sidebar">
      <div class="logo">
        <div class="logo-icon">T</div>
        <span>Tucha Blog</span>
      </div>
      <div class="menu-group" v-for="group in menuGroups" :key="group.key">
        <div class="group-title" @click="toggle(group.key)">
          <span class="group-icon">{{ group.icon }}</span>
          <span class="group-label">{{ group.label }}</span>
          <span class="arrow" :class="{ open: openGroups[group.key] }">›</span>
        </div>
        <transition name="slide">
          <div class="sub-menu" v-show="openGroups[group.key]">
            <router-link v-for="item in group.items" :key="item.path" :to="item.path">
              <span class="item-icon">{{ item.icon }}</span>
              {{ item.label }}
            </router-link>
          </div>
        </transition>
      </div>
      <div class="sidebar-footer">
        <span class="version">v1.0.0</span>
      </div>
    </nav>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const menuGroups = [
  {
    key: 'settings',
    icon: '⚙️',
    label: '基础设置',
    items: [
      { path: '/config', icon: '🏠', label: '站点配置' },
      { path: '/theme', icon: '🎨', label: '主题配置' }
    ]
  },
  {
    key: 'content',
    icon: '📝',
    label: '内容管理',
    items: [
      { path: '/posts', icon: '✏️', label: '文章管理' },
      { path: '/diary', icon: '📖', label: '日记管理' },
      { path: '/anime', icon: '🎬', label: '番剧管理' },
      { path: '/friends', icon: '👥', label: '友链管理' },
      { path: '/albums', icon: '🖼️', label: '相册管理' }
    ]
  },
  {
    key: 'showcase',
    icon: '✨',
    label: '个人展示',
    items: [
      { path: '/skills', icon: '💻', label: '技能管理' },
      { path: '/timeline', icon: '📅', label: '时间线管理' },
      { path: '/projects', icon: '🚀', label: '项目管理' }
    ]
  }
]

const openGroups = reactive({ settings: true, content: true, showcase: true })

const toggle = (group) => {
  openGroups[group] = !openGroups[group]
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Nunito', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #faf5f0;
}

.app { display: flex; min-height: 100vh; }

.sidebar {
  width: 220px;
  background: linear-gradient(180deg, #2d2b55 0%, #1a1a3e 100%);
  display: flex;
  flex-direction: column;
  box-shadow: 4px 0 20px rgba(0,0,0,0.1);
  position: relative;
  overflow: hidden;
}

.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 200px;
  background: radial-gradient(circle at 20% 50%, rgba(255, 107, 53, 0.15) 0%, transparent 50%);
  pointer-events: none;
}

.logo {
  padding: 24px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  position: relative;
}

.logo-icon {
  width: 38px;
  height: 38px;
  background: linear-gradient(135deg, #ff6b35, #ff8c42);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 700;
  font-size: 18px;
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
}

.logo span {
  color: #fff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.menu-group {
  padding: 8px 12px;
}

.group-title {
  color: rgba(255,255,255,0.45);
  font-size: 11px;
  padding: 12px 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  border-radius: 10px;
  transition: all 0.2s;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}

.group-title:hover {
  background: rgba(255,255,255,0.03);
  color: rgba(255,255,255,0.6);
}

.group-icon { font-size: 13px; }
.group-label { flex: 1; }

.arrow {
  font-size: 14px;
  transition: transform 0.3s ease;
  font-weight: 300;
}

.arrow.open {
  transform: rotate(90deg);
}

.sub-menu { overflow: hidden; }

.slide-enter-active, .slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from, .slide-leave-to {
  opacity: 0;
  max-height: 0;
}

.slide-enter-to, .slide-leave-from {
  opacity: 1;
  max-height: 500px;
}

.sidebar a {
  color: rgba(255,255,255,0.55);
  text-decoration: none;
  padding: 10px 16px;
  margin: 2px 4px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  border-radius: 10px;
  transition: all 0.2s ease;
  font-weight: 500;
}

.sidebar a:hover {
  background: rgba(255,255,255,0.06);
  color: #fff;
  transform: translateX(4px);
}

.sidebar a.router-link-active {
  background: linear-gradient(135deg, rgba(255,107,53,0.25), rgba(255,140,66,0.15));
  color: #ff8c42;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(255, 107, 53, 0.15);
}

.item-icon { font-size: 15px; }

.sidebar-footer {
  margin-top: auto;
  padding: 16px 20px;
  border-top: 1px solid rgba(255,255,255,0.06);
}

.version {
  color: rgba(255,255,255,0.2);
  font-size: 11px;
}

.content {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
  background: #faf5f0;
}

/* 全局表单样式美化 */
h1 {
  color: #2d2b55 !important;
  font-weight: 700 !important;
  font-size: 24px !important;
  margin-bottom: 24px !important;
}

.card {
  background: #fff !important;
  border-radius: 16px !important;
  box-shadow: 0 2px 12px rgba(45, 43, 85, 0.06) !important;
  border: 1px solid rgba(45, 43, 85, 0.06) !important;
}

button {
  border-radius: 10px !important;
  font-weight: 600 !important;
  transition: all 0.2s ease !important;
}

button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
}

input, select, textarea {
  border-radius: 10px !important;
  border: 1.5px solid #e8e4df !important;
  font-family: 'Nunito', sans-serif !important;
}

input:focus, select:focus, textarea:focus {
  border-color: #ff6b35 !important;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1) !important;
  outline: none !important;
}
</style>
