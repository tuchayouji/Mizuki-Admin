<template>
  <div class="page">
    <h1>项目管理</h1>
    <div class="card">
      <div class="header">
        <h3>项目列表</h3>
        <button @click="showForm = true; editMode = false; resetForm()">添加项目</button>
      </div>
      <div v-if="showForm" class="form">
        <input v-model="form.id" placeholder="ID (英文)" :disabled="editMode" />
        <input v-model="form.title" placeholder="项目名称" />
        <input v-model="form.description" placeholder="描述" />
        <select v-model="form.category">
          <option value="web">网页应用</option>
          <option value="mobile">移动应用</option>
          <option value="desktop">桌面应用</option>
          <option value="other">其他</option>
        </select>
        <select v-model="form.status">
          <option value="completed">已完成</option>
          <option value="in-progress">进行中</option>
          <option value="planned">计划中</option>
        </select>
        <input v-model="form.sourceCode" placeholder="源码链接" />
        <input v-model="form.liveDemo" placeholder="演示链接" />
        <div class="btns">
          <button @click="editMode ? update() : create()">{{ editMode ? '保存' : '添加' }}</button>
          <button class="cancel" @click="showForm = false">取消</button>
        </div>
      </div>
      <div v-for="item in projects" :key="item.id" class="item">
        <div class="info">
          <span class="name">{{ item.title }}</span>
          <span class="tag">{{ categoryText(item.category) }}</span>
          <span class="tag status" :class="item.status">{{ statusText(item.status) }}</span>
        </div>
        <div class="actions">
          <button class="edit" @click="edit(item)">编辑</button>
          <button class="delete" @click="remove(item.id)">删除</button>
        </div>
      </div>
      <p v-if="!projects.length" class="empty">暂无项目</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getProjects, createProject, updateProject, deleteProject } from '../api'

const projects = ref([])
const showForm = ref(false)
const editMode = ref(false)
const form = ref({ id: '', title: '', description: '', category: 'web', status: 'completed', sourceCode: '', liveDemo: '' })

const resetForm = () => { form.value = { id: '', title: '', description: '', category: 'web', status: 'completed', sourceCode: '', liveDemo: '' } }
const categoryText = (c) => ({ web: '网页', mobile: '移动', desktop: '桌面', other: '其他' }[c])
const statusText = (s) => ({ completed: '已完成', 'in-progress': '进行中', planned: '计划中' }[s])

const load = async () => { const { data } = await getProjects(); projects.value = data }
onMounted(load)
const edit = (item) => { form.value = { ...item }; editMode.value = true; showForm.value = true }
const create = async () => { await createProject(form.value); showForm.value = false; resetForm(); load() }
const update = async () => { await updateProject(form.value.id, form.value); showForm.value = false; resetForm(); load() }
const remove = async (id) => { if (confirm('确定删除？')) { await deleteProject(id); load() } }
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
.btns { grid-column: 1 / -1; display: flex; gap: 10px; }
.item { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
.item .info { display: flex; gap: 10px; align-items: center; }
.item .name { font-weight: bold; color: #333; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.tag { padding: 2px 8px; border-radius: 4px; font-size: 12px; background: #e9ecef; color: #495057; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.tag.status.completed { background: #28a745; color: #fff; }
.tag.status.in-progress { background: #ffc107; color: #333; }
.tag.status.planned { background: #6c757d; color: #fff; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
</style>
