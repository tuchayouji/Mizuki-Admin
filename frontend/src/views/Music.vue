<template>
  <div class="page">
    <h1>音乐管理</h1>
    <div class="config-grid">
      <div class="card main-card">
        <div class="header">
          <h3>歌曲列表</h3>
          <button @click="showForm = true; editMode = false; resetForm()">添加歌曲</button>
        </div>
        <div v-if="showForm" class="form">
          <input v-model="form.title" placeholder="歌曲名称" />
          <input v-model="form.artist" placeholder="歌手" />
          <div class="upload-row">
            <label class="upload-btn">
              上传音频
              <input type="file" @change="uploadAudio" accept="audio/*" hidden />
            </label>
            <span class="file-info" v-if="form.url">{{ form.url.split('/').pop() }}</span>
          </div>
          <div class="upload-row">
            <label class="upload-btn">
              上传封面
              <input type="file" @change="uploadCover" accept="image/*" hidden />
            </label>
            <img v-if="form.cover" :src="getCoverUrl(form.cover)" class="cover-preview" />
          </div>
          <input v-model.number="form.duration" type="number" placeholder="时长(秒)" />
          <div class="btns">
            <button @click="editMode ? update() : create()">{{ editMode ? '保存' : '添加' }}</button>
            <button class="cancel" @click="showForm = false">取消</button>
          </div>
        </div>
        <div v-for="item in songs" :key="item.id" class="item">
          <div class="info">
            <img :src="getCoverUrl(item.cover)" class="mini-cover" />
            <div class="text">
              <span class="name" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.title }}</span>
              <span class="artist" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.artist }}</span>
            </div>
          </div>
          <div class="actions">
            <button class="edit" @click="edit(item)">编辑</button>
            <button class="delete" @click="remove(item.id)">删除</button>
          </div>
        </div>
        <p v-if="!songs.length" class="empty">暂无歌曲</p>
      </div>
      <div class="card side-card">
        <h3>使用说明</h3>
        <div class="tips">
          <div class="tip-item">
            <span class="tip-icon">🎵</span>
            <div>
              <strong>添加歌曲</strong>
              <p>上传mp3音频和封面图片，填写歌曲信息</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">📁</span>
            <div>
              <strong>文件位置</strong>
              <p>音频存放在 public/assets/music/url/，封面存放在 public/assets/music/cover/</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">⏱️</span>
            <div>
              <strong>时长设置</strong>
              <p>填入秒数，如4分钟填240，播放器会自动计算进度条</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMusic, createMusic, updateMusic, deleteMusic, uploadMusicAudio, uploadMusicCover } from '../api'

const songs = ref([])
const showForm = ref(false)
const editMode = ref(false)
const editId = ref(null)
const form = ref({ title: '', artist: '', url: '', cover: '', duration: 0 })

const resetForm = () => {
  form.value = { title: '', artist: '', url: '', cover: '', duration: 0 }
  editId.value = null
}

const getCoverUrl = (cover) => {
  if (!cover) return ''
  if (cover.startsWith('http')) return cover
  return '/' + cover
}

const load = async () => { const { data } = await getMusic(); songs.value = data }
onMounted(load)

const uploadAudio = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  try {
    const { data } = await uploadMusicAudio(file)
    if (data.url) form.value.url = data.url
  } catch (e) { alert('上传失败') }
}

const uploadCover = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  try {
    const { data } = await uploadMusicCover(file)
    if (data.url) form.value.cover = data.url
  } catch (e) { alert('上传失败') }
}

const edit = (item) => {
  form.value = { ...item }
  editId.value = item.id
  editMode.value = true
  showForm.value = true
}

const create = async () => {
  await createMusic(form.value)
  showForm.value = false
  resetForm()
  load()
}

const update = async () => {
  await updateMusic(editId.value, form.value)
  showForm.value = false
  resetForm()
  editMode.value = false
  load()
}

const remove = async (id) => {
  if (confirm('确定删除这首歌曲吗？')) {
    await deleteMusic(id)
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
.form { margin-bottom: 20px; padding: 16px; background: #faf5f0; border-radius: 12px; display: flex; flex-direction: column; gap: 10px; }
.form input { padding: 12px 16px; border: 1.5px solid #e8e4df; border-radius: 10px; font-size: 14px; }
.upload-row { display: flex; align-items: center; gap: 12px; }
.upload-btn { background: linear-gradient(135deg, #28a745, #34d058); color: #fff; padding: 10px 16px; border-radius: 10px; cursor: pointer; font-size: 13px; font-weight: 600; }
.file-info { color: #666; font-size: 13px; }
.cover-preview { width: 60px; height: 60px; border-radius: 8px; object-fit: cover; }
.btns { display: flex; gap: 10px; }
button { background: linear-gradient(135deg, #ff6b35, #ff8c42); color: #fff; border: none; padding: 10px 20px; border-radius: 10px; cursor: pointer; font-size: 13px; font-weight: 600; transition: all 0.2s; }
button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3); }
button.edit { background: linear-gradient(135deg, #28a745, #34d058); }
button.delete { background: linear-gradient(135deg, #dc3545, #e85d6a); }
button.cancel { background: linear-gradient(135deg, #6c757d, #868e96); }
.item { display: flex; justify-content: space-between; align-items: center; padding: 14px 0; border-bottom: 1px solid rgba(45,43,85,0.06); }
.item .info { display: flex; gap: 12px; align-items: center; }
.mini-cover { width: 48px; height: 48px; border-radius: 8px; object-fit: cover; }
.item .text { display: flex; flex-direction: column; }
.item .name { font-weight: 600; color: #2d2b55; font-size: 14px; }
.item .artist { color: #888; font-size: 13px; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
.tips { display: flex; flex-direction: column; gap: 16px; }
.tip-item { display: flex; gap: 12px; align-items: flex-start; }
.tip-icon { font-size: 20px; }
.tip-item strong { color: #2d2b55; font-size: 14px; display: block; margin-bottom: 2px; }
.tip-item p { color: #888; font-size: 12px; line-height: 1.4; }
</style>
