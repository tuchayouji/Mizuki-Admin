<template>
  <div class="page">
    <h1>技能管理</h1>
    <div class="config-grid">
      <div class="card main-card">
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
          </div>
          <div class="btns">
            <button @click="editMode ? update() : create()">{{ editMode ? '保存' : '添加' }}</button>
            <button class="cancel" @click="showForm = false">取消</button>
          </div>
        </div>
        <div v-for="item in skills" :key="item.id" class="item">
          <div class="info">
            <span class="name" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.name }}</span>
            <span class="tag" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ categoryText(item.category) }}</span>
            <span class="tag level" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ levelText(item.level) }}</span>
          </div>
          <div class="actions">
            <button class="edit" @click="edit(item)">编辑</button>
            <button class="delete" @click="remove(item.id)">删除</button>
          </div>
        </div>
        <p v-if="!skills.length" class="empty">暂无技能</p>
      </div>
      <div class="card side-card">
        <h3>使用说明</h3>
        <div class="tips">
          <div class="tip-item">
            <span class="tip-icon">💻</span>
            <div>
              <strong>添加技能</strong>
              <p>展示你的技术栈，输入名称自动匹配图标</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">📊</span>
            <div>
              <strong>技能分类</strong>
              <p>前端、后端、数据库、工具等分类管理</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">⭐</span>
            <div>
              <strong>熟练程度</strong>
              <p>初级、中级、高级、专家四个等级</p>
            </div>
          </div>
        </div>
      </div>
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

const iconMap = {
  'javascript': 'logos:javascript', 'js': 'logos:javascript', 'typescript': 'logos:typescript-icon', 'ts': 'logos:typescript-icon',
  'vue': 'logos:vue', 'vue.js': 'logos:vue', 'react': 'logos:react', 'angular': 'logos:angular-icon',
  'next.js': 'logos:nextjs-icon', 'nextjs': 'logos:nextjs-icon', 'astro': 'logos:astro-icon', 'svelte': 'logos:svelte-icon',
  'tailwind': 'logos:tailwindcss-icon', 'tailwind css': 'logos:tailwindcss-icon', 'css': 'devicon:css3', 'html': 'devicon:html5',
  'python': 'logos:python', 'java': 'logos:java', 'c': 'logos:c', 'c++': 'logos:c-plusplus', 'cpp': 'logos:c-plusplus',
  'c#': 'devicon:csharp', 'csharp': 'devicon:csharp', 'go': 'logos:go', 'rust': 'logos:rust', 'ruby': 'logos:ruby', 'php': 'logos:php',
  'node.js': 'logos:nodejs-icon', 'nodejs': 'logos:nodejs-icon', 'mysql': 'logos:mysql-icon', 'postgresql': 'logos:postgresql',
  'mongodb': 'logos:mongodb-icon', 'redis': 'logos:redis', 'git': 'logos:git-icon', 'github': 'fa7-brands:github',
  'docker': 'logos:docker-icon', 'linux': 'logos:linux-tux', 'vscode': 'logos:visual-studio-code', 'vs code': 'logos:visual-studio-code',
  'intellij': 'logos:intellij-idea', 'pycharm': 'logos:pycharm', 'spring': 'logos:spring-icon', 'django': 'logos:django-icon',
  'flutter': 'logos:flutter', 'dart': 'logos:dart', 'kotlin': 'logos:kotlin-icon', 'swift': 'logos:swift', 'figma': 'logos:figma',
}

const autoFillIcon = () => {
  const name = form.value.name.toLowerCase().trim()
  if (iconMap[name]) { form.value.icon = iconMap[name]; return }
  for (const [key, value] of Object.entries(iconMap)) {
    if (name.includes(key) || key.includes(name)) { form.value.icon = value; break }
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
.page { max-width: 900px; }
h1 { margin-bottom: 24px; color: #2d2b55; font-weight: 700; font-size: 24px; }
.config-grid { display: grid; grid-template-columns: 1.5fr 1fr; gap: 20px; }
.card { background: #fff; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(45,43,85,0.06); border: 1px solid rgba(45,43,85,0.06); }
.card h3 { color: #2d2b55; font-size: 16px; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 2px solid #ff6b35; display: inline-block; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.form { margin-bottom: 20px; padding: 16px; background: #faf5f0; border-radius: 12px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.form input, .form select { padding: 12px 16px; border: 1.5px solid #e8e4df; border-radius: 10px; font-size: 14px; }
.icon-input { grid-column: 1 / -1; }
.btns { grid-column: 1 / -1; display: flex; gap: 10px; }
button {
  background: linear-gradient(135deg, #ff6b35, #ff8c42);
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.2s;
}
button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3); }
button.edit { background: linear-gradient(135deg, #28a745, #34d058); }
button.delete { background: linear-gradient(135deg, #dc3545, #e85d6a); }
button.cancel { background: linear-gradient(135deg, #6c757d, #868e96); }
.item { display: flex; justify-content: space-between; align-items: center; padding: 14px 0; border-bottom: 1px solid rgba(45,43,85,0.06); }
.item .info { display: flex; gap: 10px; align-items: center; }
.item .name { font-weight: 600; color: #2d2b55; }
.tag { padding: 3px 10px; border-radius: 6px; font-size: 12px; background: #e9ecef; color: #495057; font-weight: 600; }
.tag.level { background: linear-gradient(135deg, #ff6b35, #ff8c42); color: #fff; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
.tips { display: flex; flex-direction: column; gap: 16px; }
.tip-item { display: flex; gap: 12px; align-items: flex-start; }
.tip-icon { font-size: 20px; }
.tip-item strong { color: #2d2b55; font-size: 14px; display: block; margin-bottom: 2px; }
.tip-item p { color: #888; font-size: 12px; line-height: 1.4; }
</style>
