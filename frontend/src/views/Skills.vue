<template>
  <div class="page">
    <h1>技能管理</h1>
    <div class="card">
      <div class="header">
        <h3>技能列表</h3>
        <button @click="showForm = true; editMode = false; resetForm()">添加技能</button>
      </div>
      <div v-if="showForm" class="form">
        <input v-model="form.id" placeholder="ID (英文)" :disabled="editMode" />
        <input v-model="form.name" placeholder="技能名称" @input="autoFillIcon" />
        <select v-model="form.category">
          <option value="frontend">前端</option>
          <option value="backend">后端</option>
          <option value="database">数据库</option>
          <option value="tools">工具</option>
          <option value="other">其他</option>
        </select>
        <select v-model="form.level">
          <option value="beginner">初级</option>
          <option value="intermediate">中级</option>
          <option value="advanced">高级</option>
          <option value="expert">专家</option>
        </select>
        <input v-model="form.description" placeholder="描述" />
        <div class="icon-input">
          <input v-model="form.icon" placeholder="图标 (如 logos:javascript)" />
          <span class="icon-preview" v-if="form.icon">{{ form.icon.split(':')[1] }}</span>
        </div>
        <div class="btns">
          <button @click="editMode ? update() : create()">{{ editMode ? '保存' : '添加' }}</button>
          <button class="cancel" @click="showForm = false">取消</button>
        </div>
      </div>
      <div v-for="item in skills" :key="item.id" class="item">
        <div class="info">
          <span class="name">{{ item.name }}</span>
          <span class="tag">{{ categoryText(item.category) }}</span>
          <span class="tag level">{{ levelText(item.level) }}</span>
        </div>
        <div class="actions">
          <button class="edit" @click="edit(item)">编辑</button>
          <button class="delete" @click="remove(item.id)">删除</button>
        </div>
      </div>
      <p v-if="!skills.length" class="empty">暂无技能</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSkills, createSkill, updateSkill, deleteSkill } from '../api'

const skills = ref([])
const showForm = ref(false)
const editMode = ref(false)
const form = ref({ id: '', name: '', category: 'frontend', level: 'beginner', description: '', icon: '' })

const resetForm = () => { form.value = { id: '', name: '', category: 'frontend', level: 'beginner', description: '', icon: '' } }
const categoryText = (c) => ({ frontend: '前端', backend: '后端', database: '数据库', tools: '工具', other: '其他' }[c])
const levelText = (l) => ({ beginner: '初级', intermediate: '中级', advanced: '高级', expert: '专家' }[l])

// 技能名称到图标的映射
const iconMap = {
  'javascript': 'logos:javascript',
  'js': 'logos:javascript',
  'typescript': 'logos:typescript-icon',
  'ts': 'logos:typescript-icon',
  'vue': 'logos:vue',
  'vue.js': 'logos:vue',
  'react': 'logos:react',
  'angular': 'logos:angular-icon',
  'next.js': 'logos:nextjs-icon',
  'nextjs': 'logos:nextjs-icon',
  'nuxt': 'logos:nuxt-icon',
  'nuxt.js': 'logos:nuxt-icon',
  'astro': 'logos:astro-icon',
  'svelte': 'logos:svelte-icon',
  'tailwind': 'logos:tailwindcss-icon',
  'tailwind css': 'logos:tailwindcss-icon',
  'css': 'devicon:css3',
  'html': 'devicon:html5',
  'sass': 'logos:sass',
  'webpack': 'logos:webpack',
  'vite': 'logos:vitejs',
  'node.js': 'logos:nodejs-icon',
  'nodejs': 'logos:nodejs-icon',
  'python': 'logos:python',
  'java': 'logos:java',
  'c': 'logos:c',
  'c++': 'logos:c-plusplus',
  'cpp': 'logos:c-plusplus',
  'c#': 'devicon:csharp',
  'csharp': 'devicon:csharp',
  'go': 'logos:go',
  'golang': 'logos:go',
  'rust': 'logos:rust',
  'ruby': 'logos:ruby',
  'php': 'logos:php',
  'swift': 'logos:swift',
  'kotlin': 'logos:kotlin-icon',
  'sql': 'devicon:mysql',
  'mysql': 'logos:mysql-icon',
  'postgresql': 'logos:postgresql',
  'postgres': 'logos:postgresql',
  'mongodb': 'logos:mongodb-icon',
  'redis': 'logos:redis',
  'sqlite': 'simple-icons:sqlite',
  'firebase': 'simple-icons:firebase',
  'git': 'logos:git-icon',
  'github': 'fa7-brands:github',
  'docker': 'logos:docker-icon',
  'kubernetes': 'logos:kubernetes',
  'k8s': 'logos:kubernetes',
  'nginx': 'logos:nginx',
  'linux': 'logos:linux-tux',
  'ubuntu': 'logos:ubuntu',
  'windows': 'devicon:windows8',
  'vs code': 'logos:visual-studio-code',
  'vscode': 'logos:visual-studio-code',
  'visual studio': 'logos:visual-studio',
  'intellij': 'logos:intellij-idea',
  'idea': 'logos:intellij-idea',
  'pycharm': 'logos:pycharm',
  'webstorm': 'logos:webstorm',
  'android': 'logos:android-icon',
  'ios': 'logos:apple',
  'flutter': 'logos:flutter',
  'dart': 'logos:dart',
  'spring': 'logos:spring-icon',
  'spring boot': 'logos:spring-icon',
  'django': 'logos:django-icon',
  'flask': 'logos:flask',
  'express': 'simple-icons:express',
  'fastapi': 'devicon:fastapi',
  'aws': 'logos:aws',
  'azure': 'logos:microsoft-azure',
  'gcp': 'logos:google-cloud',
  'figma': 'logos:figma',
  'photoshop': 'logos:adobe-photoshop',
  'illustrator': 'logos:adobe-illustrator',
  'postman': 'logos:postman-icon',
  'graphql': 'logos:graphql',
  'rest': 'devicon:rest',
  'api': 'mdi:api',
  'sass': 'logos:sass',
  'less': 'devicon:less',
  'jquery': 'logos:jquery',
  'bootstrap': 'logos:bootstrap',
  'tailwindcss': 'logos:tailwindcss-icon',
  'npm': 'logos:npm',
  'yarn': 'logos:yarn',
  'pnpm': 'logos:pnpm',
  'pip': 'devicon:pypi',
  'maven': 'devicon:maven',
  'gradle': 'logos:gradle',
  'tomcat': 'logos:tomcat',
  'apache': 'logos:apache',
  'elasticsearch': 'logos:elasticsearch',
  'elastic': 'logos:elasticsearch',
  'kibana': 'logos:kibana',
  'grafana': 'logos:grafana',
  'prometheus': 'logos:prometheus',
  'jest': 'logos:jest',
  'mocha': 'logos:mocha',
  'cypress': 'logos:cypress-icon',
  'playwright': 'logos:playwright',
  'selenium': 'logos:selenium',
  'vuepress': 'logos:vuepress',
  'vitepress': 'logos:vitepress',
  'deno': 'logos:deno',
  'bun': 'logos:bun',
  'solid': 'logos:solidjs',
  'solidjs': 'logos:solidjs',
  'preact': 'logos:preact',
  'ember': 'logos:ember',
  'backbone': 'logos:backbone',
  'jquery': 'logos:jquery',
  'lodash': 'logos:lodash',
  'axios': 'logos:axios',
  'fetch': 'devicon:fetch',
  'socket': 'logos:socket',
  'websocket': 'mdi:websocket',
  'mqtt': 'mdi:mqtt',
  'grpc': 'logos:grpc',
  'protobuf': 'mdi:protobuf',
  'json': 'mdi:json',
  'xml': 'mdi:xml',
  'yaml': 'mdi:yaml',
  'markdown': 'logos:markdown',
  'md': 'logos:markdown',
  'vim': 'logos:vim',
  'neovim': 'logos:neovim',
  'emacs': 'devicon:emacs',
  'sublime': 'devicon:sublime',
  'atom': 'logos:atom',
  'notion': 'logos:notion',
  'obsidian': 'logos:obsidian',
  'jira': 'logos:jira',
  'trello': 'logos:trello',
  'slack': 'logos:slack',
  'discord': 'logos:discord',
  'telegram': 'logos:telegram',
  'twitter': 'logos:twitter',
  'linkedin': 'logos:linkedin',
  'youtube': 'logos:youtube',
  'twitch': 'logos:twitch',
  'steam': 'logos:steam',
  'unity': 'logos:unity',
  'unreal': 'logos:unreal',
  'godot': 'logos:godot',
  'blender': 'logos:blender',
  'maya': 'logos:maya',
  'after effects': 'logos:aftereffects',
  'premiere': 'logos:premiere',
  'ae': 'logos:aftereffects',
  'pr': 'logos:premiere',
  'ps': 'logos:adobe-photoshop',
  'ai': 'logos:adobe-illustrator',
  'xd': 'logos:adobe-xd',
  'sketch': 'logos:sketch',
  'zeplin': 'logos:zeplin',
  'invision': 'logos:invision',
  'vercel': 'logos:vercel',
  'netlify': 'logos:netlify',
  'cloudflare': 'logos:cloudflare',
  'heroku': 'logos:heroku',
  'digitalocean': 'logos:digitalocean',
  'linode': 'logos:linode',
  'vultr': 'logos:vultr',
}

const autoFillIcon = () => {
  const name = form.value.name.toLowerCase().trim()
  if (iconMap[name]) {
    form.value.icon = iconMap[name]
  } else {
    // 尝试模糊匹配
    for (const [key, value] of Object.entries(iconMap)) {
      if (name.includes(key) || key.includes(name)) {
        form.value.icon = value
        break
      }
    }
  }
}

const load = async () => { const { data } = await getSkills(); skills.value = data }
onMounted(load)
const edit = (item) => { form.value = { ...item }; editMode.value = true; showForm.value = true }
const create = async () => { await createSkill(form.value); showForm.value = false; resetForm(); load() }
const update = async () => { await updateSkill(form.value.id, form.value); showForm.value = false; resetForm(); load() }
const remove = async (id) => { if (confirm('确定删除？')) { await deleteSkill(id); load() } }
</script>

<style scoped>
.page { max-width: 800px; }
h1 { margin-bottom: 20px; color: #333; }
.card { background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
button { background: #ff6b35; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; }
button.edit { background: #28a745; }
button.delete { background: #dc3545; }
button.cancel { background: #6c757d; }
.form { margin-bottom: 20px; padding: 16px; background: #f8f9fa; border-radius: 8px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.form input, .form select { padding: 10px; border: 1px solid #ddd; border-radius: 6px; }
.icon-input { grid-column: 1 / -1; display: flex; gap: 10px; align-items: center; }
.icon-input input { flex: 1; }
.icon-preview { color: #666; font-size: 12px; background: #e9ecef; padding: 4px 8px; border-radius: 4px; }
.btns { grid-column: 1 / -1; display: flex; gap: 10px; }
.item { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
.item .info { display: flex; gap: 10px; align-items: center; }
.item .name { font-weight: bold; color: #333; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.tag { padding: 2px 8px; border-radius: 4px; font-size: 12px; background: #e9ecef; color: #495057; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.tag.level { background: #ff6b35; color: #fff; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
</style>
