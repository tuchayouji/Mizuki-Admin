<template>
  <div class="page">
    <h1>番剧管理</h1>
    <div class="card">
      <div class="header">
        <h3>追番列表</h3>
        <button @click="showForm = true; editMode = false; resetForm()">添加番剧</button>
      </div>
      
      <div v-if="showForm" class="form">
        <div class="quick-add" v-if="!editMode">
          <input v-model="bilibiliUrl" placeholder="粘贴B站番剧链接，自动获取信息" class="url-input" />
          <button @click="fetchInfo" :disabled="fetching">{{ fetching ? '获取中...' : '自动获取' }}</button>
        </div>
        
        <div class="cover-section">
          <div class="cover-preview" v-if="form.cover">
            <img :src="getImageUrl(form.cover)" alt="封面" />
          </div>
          <div class="cover-actions">
            <label class="upload-btn">
              上传封面
              <input type="file" @change="uploadCover" accept="image/*" hidden />
            </label>
          </div>
        </div>

        <input v-model="form.title" placeholder="番名" :disabled="editMode" />
        <select v-model="form.status">
          <option value="watching">在看</option>
          <option value="completed">看过</option>
          <option value="planned">想看</option>
        </select>
        <input v-model.number="form.rating" type="number" placeholder="评分" step="0.1" />
        <input v-model="form.description" placeholder="简介" />
        <input v-model="form.genreStr" placeholder="类型 (逗号分隔)" />
        <input v-model="form.year" placeholder="年份" />
        <input v-model="form.link" placeholder="B站链接" />
        <input v-model="form.studio" placeholder="制作公司" />
        <input v-model.number="form.progress" type="number" placeholder="已看集数" />
        <input v-model.number="form.totalEpisodes" type="number" placeholder="总集数" />
        <div class="btns">
          <button @click="editMode ? update() : create()">{{ editMode ? '保存' : '添加' }}</button>
          <button class="cancel" @click="showForm = false">取消</button>
        </div>
      </div>

      <div v-for="item in anime" :key="item.title" class="anime-item">
        <div class="info">
          <img v-if="item.cover" :src="getImageUrl(item.cover)" class="mini-cover" />
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
import { getAnime, createAnime, updateAnime, deleteAnime, uploadAnimeCover } from '../api'
import axios from 'axios'

const anime = ref([])
const showForm = ref(false)
const editMode = ref(false)
const bilibiliUrl = ref('')
const fetching = ref(false)
const form = ref({ title: '', status: 'watching', rating: 0, description: '', genreStr: '', year: '', link: '', studio: '', progress: 0, totalEpisodes: 12, cover: '' })

const resetForm = () => {
  form.value = { title: '', status: 'watching', rating: 0, description: '', genreStr: '', year: '', link: '', studio: '', progress: 0, totalEpisodes: 12, cover: '' }
  bilibiliUrl.value = ''
}

const statusText = (s) => ({ watching: '在看', completed: '看过', planned: '想看' }[s])

// 将图片路径转换为后端API地址
const getImageUrl = (cover) => {
  if (!cover) return ''
  if (cover.startsWith('http')) return cover
  // 提取文件名
  const filename = cover.split('/').pop()
  return `/api/anime/images/${filename}`
}

const load = async () => { const { data } = await getAnime(); anime.value = data }
onMounted(load)

// 从B站链接获取信息
const fetchInfo = async () => {
  if (!bilibiliUrl.value) return alert('请输入B站链接')
  fetching.value = true
  try {
    const { data } = await axios.post('/api/anime/fetch', { url: bilibiliUrl.value })
    if (data.error) {
      alert(data.error)
    } else {
      form.value.title = data.title || form.value.title
      form.value.rating = data.rating || form.value.rating
      form.value.year = data.year || form.value.year
      form.value.link = data.link || form.value.link
      form.value.studio = data.studio || form.value.studio
      if (data.episodes) form.value.totalEpisodes = data.episodes
      if (data.cover) {
        form.value.cover = data.cover.startsWith('http') ? data.cover : 'https:' + data.cover
      }
      // 简化简介
      if (data.description) {
        form.value.description = data.description
      }
      // 填充类型
      if (data.genres && data.genres.length) {
        form.value.genreStr = data.genres.join(',')
      }
    }
  } catch (e) {
    alert('获取失败，请检查链接')
  }
  fetching.value = false
}

// 上传封面
const uploadCover = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  try {
    const { data } = await uploadAnimeCover(file)
    if (data.url) {
      form.value.cover = data.url
    }
  } catch (e) {
    alert('上传失败')
  }
}

const edit = (item) => {
  form.value = { ...item, genreStr: (item.genre || []).join(',') }
  editMode.value = true
  showForm.value = true
}

const create = async () => {
  const submitData = { ...form.value, genre: form.value.genreStr ? form.value.genreStr.split(',').map(g => g.trim()) : [] }
  await createAnime(submitData)
  showForm.value = false
  resetForm()
  load()
}

const update = async () => {
  const submitData = { ...form.value, genre: form.value.genreStr ? form.value.genreStr.split(',').map(g => g.trim()) : [] }
  await updateAnime(form.value.title, submitData)
  showForm.value = false
  resetForm()
  editMode.value = false
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
button:disabled { opacity: 0.6; cursor: not-allowed; }
button.edit { background: #28a745; }
button.delete { background: #dc3545; }
button.cancel { background: #6c757d; }
.form { margin-bottom: 20px; padding: 16px; background: #f8f9fa; border-radius: 8px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.form input, .form select { padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
.quick-add { grid-column: 1 / -1; display: flex; gap: 10px; margin-bottom: 10px; }
.url-input { flex: 1; }
.cover-section { grid-column: 1 / -1; display: flex; gap: 16px; align-items: flex-start; margin-bottom: 10px; }
.cover-preview { width: 120px; height: 160px; border-radius: 8px; overflow: hidden; background: #f0f0f0; }
.cover-preview img { width: 100%; height: 100%; object-fit: cover; }
.cover-actions { display: flex; flex-direction: column; gap: 8px; }
.upload-btn { background: #28a745; color: #fff; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; text-align: center; }
.upload-btn:hover { background: #218838; }
.btns { grid-column: 1 / -1; display: flex; gap: 10px; }
.anime-item { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
.anime-item .info { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.mini-cover { width: 40px; height: 56px; border-radius: 4px; object-fit: cover; }
.anime-item .title { font-weight: bold; color: #333; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.tag { padding: 2px 8px; border-radius: 4px; font-size: 12px; color: #fff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.tag.watching { background: #28a745; }
.tag.completed { background: #007bff; }
.tag.planned { background: #ffc107; color: #333; }
.rating { color: #ff6b35; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.progress { color: #999; font-size: 13px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
</style>
