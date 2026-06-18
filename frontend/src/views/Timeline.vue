<template>
  <div class="page">
    <h1>时间线管理</h1>
    <div class="card">
      <div class="header">
        <h3>时间线列表</h3>
        <button @click="showForm = true; editMode = false; resetForm()">添加经历</button>
      </div>
      <div v-if="showForm" class="form">
        <input v-model="form.id" placeholder="ID (英文)" :disabled="editMode" />
        <input v-model="form.title" placeholder="标题" />
        <input v-model="form.description" placeholder="描述" />
        <select v-model="form.type">
          <option value="education">教育经历</option>
          <option value="work">工作经历</option>
          <option value="project">项目经历</option>
          <option value="achievement">成就荣誉</option>
        </select>
        <input v-model="form.startDate" type="date" placeholder="开始日期" />
        <input v-model="form.endDate" type="date" placeholder="结束日期" />
        <input v-model="form.location" placeholder="地点" />
        <input v-model="form.organization" placeholder="机构" />
        <div class="btns">
          <button @click="editMode ? update() : create()">{{ editMode ? '保存' : '添加' }}</button>
          <button class="cancel" @click="showForm = false">取消</button>
        </div>
      </div>
      <div v-for="item in timeline" :key="item.id" class="item">
        <div class="info">
          <span class="name">{{ item.title }}</span>
          <span class="tag">{{ typeText(item.type) }}</span>
          <span class="date">{{ item.startDate }} {{ item.endDate ? '- ' + item.endDate : '' }}</span>
        </div>
        <div class="actions">
          <button class="edit" @click="edit(item)">编辑</button>
          <button class="delete" @click="remove(item.id)">删除</button>
        </div>
      </div>
      <p v-if="!timeline.length" class="empty">暂无经历</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTimeline, createTimeline, updateTimeline, deleteTimeline } from '../api'

const timeline = ref([])
const showForm = ref(false)
const editMode = ref(false)
const form = ref({ id: '', title: '', description: '', type: 'education', startDate: '', endDate: '', location: '', organization: '' })

const resetForm = () => { form.value = { id: '', title: '', description: '', type: 'education', startDate: '', endDate: '', location: '', organization: '' } }
const typeText = (t) => ({ education: '教育', work: '工作', project: '项目', achievement: '成就' }[t])

const load = async () => { const { data } = await getTimeline(); timeline.value = data }
onMounted(load)
const edit = (item) => { form.value = { ...item }; editMode.value = true; showForm.value = true }
const create = async () => { await createTimeline(form.value); showForm.value = false; resetForm(); load() }
const update = async () => { await updateTimeline(form.value.id, form.value); showForm.value = false; resetForm(); load() }
const remove = async (id) => { if (confirm('确定删除？')) { await deleteTimeline(id); load() } }
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
.item .info { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.item .name { font-weight: bold; color: #333; }
.tag { padding: 2px 8px; border-radius: 4px; font-size: 12px; background: #ff6b35; color: #fff; }
.date { color: #999; font-size: 13px; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
</style>
