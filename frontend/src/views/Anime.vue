<template>
  <div class="page">
    <h1>番剧管理</h1>
    <div class="card">
      <div class="header">
        <h3>追番列表</h3>
        <button @click="showForm = true; editMode = false; resetForm()">添加番剧</button>
      </div>
      <div v-if="showForm" class="form">
        <input v-model="form.title" placeholder="番名" :disabled="editMode" />
        <select v-model="form.status">
          <option value="watching">在看</option>
          <option value="completed">看过</option>
          <option value="planned">想看</option>
        </select>
        <input v-model.number="form.rating" type="number" placeholder="评分" />
        <input v-model="form.description" placeholder="简介" />
        <input v-model="form.year" placeholder="年份" />
        <input v-model="form.link" placeholder="B站链接" />
        <input v-model="form.studio" placeholder="制作公司" />
        <input v-model.number="form.progress" type="number" placeholder="进度" />
        <input v-model.number="form.totalEpisodes" type="number" placeholder="总集数" />
        <div class="btns">
          <button @click="editMode ? update() : create()">{{ editMode ? '保存' : '添加' }}</button>
          <button class="cancel" @click="showForm = false">取消</button>
        </div>
      </div>
      <div v-for="item in anime" :key="item.title" class="anime-item">
        <div class="info">
          <span class="title">{{ item.title }}</span>
          <span class="tag" :class="item.status">{{ statusText(item.status) }}</span>
          <span class="rating">{{ item.rating }}</span>
          <span class="progress">{{ item.progress }}/{{ item.totalEpisodes }}</span>
        </div>
        <div class="actions">
          <button class="edit" @click="edit(item)">编辑</button>
          <button class="delete" @click="remove(item.title)">删除</button>
        </div>
      </div>
      <p v-if="!anime.length" class="empty">暂无番剧</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAnime, createAnime, updateAnime, deleteAnime } from '../api'

const anime = ref([])
const showForm = ref(false)
const editMode = ref(false)
const form = ref({ title: '', status: 'watching', rating: 0, description: '', year: '', link: '', studio: '', progress: 0, totalEpisodes: 12 })

const resetForm = () => {
  form.value = { title: '', status: 'watching', rating: 0, description: '', year: '', link: '', studio: '', progress: 0, totalEpisodes: 12 }
}

const statusText = (s) => ({ watching: '在看', completed: '看过', planned: '想看' }[s])

const load = async () => {
  const { data } = await getAnime()
  anime.value = data
}

onMounted(load)

const edit = (item) => {
  form.value = { ...item }
  editMode.value = true
  showForm.value = true
}

const create = async () => {
  await createAnime(form.value)
  showForm.value = false
  resetForm()
  load()
}

const update = async () => {
  await updateAnime(form.value.title, form.value)
  showForm.value = false
  resetForm()
  load()
}

const remove = async (title) => {
  if (confirm('确定删除？')) {
    await deleteAnime(title)
    load()
  }
}
</script>

<style scoped>
.page { max-width: 800px; }
h1 { margin-bottom: 20px; color: #333; }
.card { background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
button { background: #ff6b35; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; }
button:hover { background: #e55a2b; }
button.edit { background: #28a745; }
button.delete { background: #dc3545; }
button.cancel { background: #6c757d; }
.form { margin-bottom: 20px; padding: 16px; background: #f8f9fa; border-radius: 8px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.form input, .form select { padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
.btns { grid-column: 1 / -1; display: flex; gap: 10px; }
.anime-item { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
.anime-item .info { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.anime-item .title { font-weight: bold; color: #333; }
.tag { padding: 2px 8px; border-radius: 4px; font-size: 12px; color: #fff; }
.tag.watching { background: #28a745; }
.tag.completed { background: #007bff; }
.tag.planned { background: #ffc107; color: #333; }
.rating { color: #ff6b35; }
.progress { color: #999; font-size: 13px; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
</style>
