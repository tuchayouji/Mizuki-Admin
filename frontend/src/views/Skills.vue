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
        <input v-model="form.name" placeholder="技能名称" />
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
        <input v-model="form.icon" placeholder="图标 (如 logos:javascript)" />
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
.btns { grid-column: 1 / -1; display: flex; gap: 10px; }
.item { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
.item .info { display: flex; gap: 10px; align-items: center; }
.item .name { font-weight: bold; color: #333; }
.tag { padding: 2px 8px; border-radius: 4px; font-size: 12px; background: #e9ecef; color: #495057; }
.tag.level { background: #ff6b35; color: #fff; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
</style>
