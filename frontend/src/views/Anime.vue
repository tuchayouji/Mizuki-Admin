<template>
  <div class="page">
    <h1>番剧管理</h1>
    <div class="config-grid">
      <div class="card main-card">
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
              <label class="upload-btn">上传封面<input type="file" @change="uploadCover" accept="image/*" hidden /></label>
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
            <span class="title" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.title }}</span>
            <span class="tag" :class="item.status" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ statusText(item.status) }}</span>
            <span class="rating" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.rating }}</span>
            <span class="progress" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.progress }}/{{ item.totalEpisodes }}</span>
          </div>
          <div class="actions">
            <button class="edit" @click="edit(item)">编辑</button>
            <button class="delete" @click="remove(item.title)">删除</button>
          </div>
        </div>
        <p v-if="!anime.length" class="empty">暂无番剧</p>
      </div>
      <div class="card side-card">
        <h3>使用说明</h3>
        <div class="tips">
          <div class="tip-item">
            <span class="tip-icon">🔗</span>
            <div>
              <strong>自动获取</strong>
              <p>粘贴B站链接自动获取番剧信息和封面</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">📊</span>
            <div>
              <strong>观看状态</strong>
              <p>在看=绿色，看过=蓝色，想看=黄色</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">🖼️</span>
            <div>
              <strong>封面管理</strong>
              <p>可上传本地封面或从B站下载</p>
            </div>
          </div>
        </div>
      </div>
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

const getImageUrl = (cover) => {
  if (!cover) return ''
  if (cover.startsWith('http')) return cover
  const filename = cover.split('/').pop()
  return `/api/anime/images/${filename}`
}

const load = async () => { const { data } = await getAnime(); anime.value = data }
onMounted(load)

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
      if (data.description) form.value.description = data.description
      if (data.genres && data.genres.length) {
        form.value.genreStr = data.genres.join(',')
      }
    }
  } catch (e) {
    alert('获取失败，请检查链接')
  }
  fetching.value = false
}

const uploadCover = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  try {
    const { data } = await uploadAnimeCover(file)
    if (data.url) form.value.cover = data.url
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
.page { max-width: 900px; }
h1 { margin-bottom: 24px; color: #2d2b55; font-weight: 700; font-size: 24px; }
.config-grid { display: grid; grid-template-columns: 1.5fr 1fr; gap: 20px; }
.card { background: #fff; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(45,43,85,0.06); border: 1px solid rgba(45,43,85,0.06); }
.card h3 { color: #2d2b55; font-size: 16px; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 2px solid #ff6b35; display: inline-block; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.form { margin-bottom: 20px; padding: 16px; background: #faf5f0; border-radius: 12px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.form input, .form select { padding: 12px 16px; border: 1.5px solid #e8e4df; border-radius: 10px; font-size: 14px; }
.quick-add { grid-column: 1 / -1; display: flex; gap: 10px; margin-bottom: 10px; }
.url-input { flex: 1; }
.cover-section { grid-column: 1 / -1; display: flex; gap: 16px; align-items: flex-start; margin-bottom: 10px; }
.cover-preview { width: 100px; height: 140px; border-radius: 10px; overflow: hidden; background: #f0f0f0; }
.cover-preview img { width: 100%; height: 100%; object-fit: cover; }
.cover-actions { display: flex; flex-direction: column; gap: 8px; }
.upload-btn { background: linear-gradient(135deg, #28a745, #34d058); color: #fff; padding: 10px 16px; border-radius: 10px; cursor: pointer; font-size: 13px; text-align: center; font-weight: 600; }
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
button:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
button.edit { background: linear-gradient(135deg, #28a745, #34d058); }
button.delete { background: linear-gradient(135deg, #dc3545, #e85d6a); }
button.cancel { background: linear-gradient(135deg, #6c757d, #868e96); }
.anime-item { display: flex; justify-content: space-between; align-items: center; padding: 14px 0; border-bottom: 1px solid rgba(45,43,85,0.06); }
.anime-item .info { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.mini-cover { width: 40px; height: 56px; border-radius: 6px; object-fit: cover; }
.anime-item .title { font-weight: 600; color: #2d2b55; }
.tag { padding: 3px 10px; border-radius: 6px; font-size: 12px; color: #fff; font-weight: 600; }
.tag.watching { background: linear-gradient(135deg, #28a745, #34d058); }
.tag.completed { background: linear-gradient(135deg, #007bff, #4da3ff); }
.tag.planned { background: linear-gradient(135deg, #ffc107, #ffda44); color: #333; }
.rating { color: #ff6b35; font-weight: 700; }
.progress { color: #999; font-size: 13px; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
.tips { display: flex; flex-direction: column; gap: 16px; }
.tip-item { display: flex; gap: 12px; align-items: flex-start; }
.tip-icon { font-size: 20px; }
.tip-item strong { color: #2d2b55; font-size: 14px; display: block; margin-bottom: 2px; }
.tip-item p { color: #888; font-size: 12px; line-height: 1.4; }
</style>
