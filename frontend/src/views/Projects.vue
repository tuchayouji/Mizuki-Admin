<template>
  <div class="page">
    <h1>项目管理</h1>
    <div class="config-grid">
      <div class="card main-card">
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
            <span class="name" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.title }}</span>
            <span class="tag" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ categoryText(item.category) }}</span>
            <span class="tag status" :class="item.status" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ statusText(item.status) }}</span>
          </div>
          <div class="actions">
            <button class="edit" @click="edit(item)">编辑</button>
            <button class="delete" @click="remove(item.id)">删除</button>
          </div>
        </div>
        <p v-if="!projects.length" class="empty">暂无项目</p>
      </div>
      <div class="card side-card">
        <h3>使用说明</h3>
        <div class="tips">
          <div class="tip-item">
            <span class="tip-icon">🚀</span>
            <div>
              <strong>展示项目</strong>
              <p>展示你的开发项目和作品集</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">📂</span>
            <div>
              <strong>项目分类</strong>
              <p>网页、移动、桌面等不同类型</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">🔗</span>
            <div>
              <strong>链接管理</strong>
              <p>填写源码和演示链接方便访问</p>
            </div>
          </div>
        </div>
      </div>
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
.page { max-width: 900px; }
h1 { margin-bottom: 24px; color: #2d2b55; font-weight: 700; font-size: 24px; }
.config-grid { display: grid; grid-template-columns: 1.5fr 1fr; gap: 20px; }
.card { background: #fff; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(45,43,85,0.06); border: 1px solid rgba(45,43,85,0.06); }
.card h3 { color: #2d2b55; font-size: 16px; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 2px solid #ff6b35; display: inline-block; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.form { margin-bottom: 20px; padding: 16px; background: #faf5f0; border-radius: 12px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.form input, .form select { padding: 12px 16px; border: 1.5px solid #e8e4df; border-radius: 10px; font-size: 14px; }
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
.tag.status.completed { background: linear-gradient(135deg, #28a745, #34d058); color: #fff; }
.tag.status.in-progress { background: linear-gradient(135deg, #ffc107, #ffda44); color: #333; }
.tag.status.planned { background: linear-gradient(135deg, #6c757d, #868e96); color: #fff; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
.tips { display: flex; flex-direction: column; gap: 16px; }
.tip-item { display: flex; gap: 12px; align-items: flex-start; }
.tip-icon { font-size: 20px; }
.tip-item strong { color: #2d2b55; font-size: 14px; display: block; margin-bottom: 2px; }
.tip-item p { color: #888; font-size: 12px; line-height: 1.4; }
</style>
