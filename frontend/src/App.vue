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
    icon: '📄',
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
* { margin: 0; padding: 0; box-sizing: border-box; }
@font-face {
  font-family: 'Loli';
  src: url('/fonts/loli.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}
body { 
  font-family: 'Loli', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
  background: #f5f5f5; 
}
.app { display: flex; min-height: 100vh; }
.sidebar {
  width: 240px;
  background: #1e1e2d;
  display: flex;
  flex-direction: column;
  box-shadow: 4px 0 20px rgba(0,0,0,0.15);
}
.logo {
  padding: 24px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #ff6b35, #ff8c42);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 700;
  font-size: 18px;
}
.logo span {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
}
.menu-group {
  padding: 8px 12px;
}
.group-title {
  color: rgba(255,255,255,0.5);
  font-size: 12px;
  padding: 12px 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.group-title:hover {
  background: rgba(255,255,255,0.03);
  color: rgba(255,255,255,0.7);
}
.group-icon { font-size: 14px; }
.group-label { flex: 1; }
.arrow {
  font-size: 16px;
  transition: transform 0.3s ease;
  font-weight: 300;
}
.arrow.open {
  transform: rotate(90deg);
}
.sub-menu {
  overflow: hidden;
}
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
  color: rgba(255,255,255,0.6);
  text-decoration: none;
  padding: 10px 16px;
  margin: 2px 0;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  border-radius: 8px;
  transition: all 0.2s ease;
}
.sidebar a:hover {
  background: rgba(255,255,255,0.05);
  color: #fff;
}
.sidebar a.router-link-active {
  background: linear-gradient(135deg, rgba(255,107,53,0.2), rgba(255,140,66,0.1));
  color: #ff6b35;
  font-weight: 500;
}
.item-icon { font-size: 15px; }
.content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
  background: #f5f5f5;
}
</style>
