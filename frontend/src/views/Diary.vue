<template>
  <div class="page">
    <h1>日记管理</h1>
    <div class="config-grid">
      <div class="card main-card">
        <div class="header">
          <h3>日记列表</h3>
          <button @click="showForm = true; editMode = false; resetForm()">写日记</button>
        </div>
        <div v-if="showForm" class="form">
          <textarea v-model="form.content" placeholder="今天发生了什么..."></textarea>
          <div class="upload-area">
            <input type="file" ref="fileInput" @change="upload" accept="image/*" multiple />
            <div class="preview" v-if="form.images.length">
              <div v-for="(img, i) in form.images" :key="i" class="img-item">
                <img :src="getDiaryImageUrl(img)" />
                <button class="remove" @click="form.images.splice(i, 1)">×</button>
              </div>
            </div>
          </div>
          <div class="btns">
            <button @click="editMode ? update() : create()">{{ editMode ? '保存' : '发布' }}</button>
            <button class="cancel" @click="showForm = false">取消</button>
          </div>
        </div>
        <div v-for="item in diary" :key="item.id" class="diary-item">
          <div class="content" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.content }}</div>
          <div class="images" v-if="item.images && item.images.length">
            <img v-for="img in item.images" :key="img" :src="getDiaryImageUrl(img)" />
          </div>
          <div class="meta">
            <span style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ formatDate(item.date) }}</span>
            <div class="actions">
              <button class="edit" @click="edit(item)">编辑</button>
              <button class="delete" @click="remove(item.id)">删除</button>
            </div>
          </div>
        </div>
        <p v-if="!diary.length" class="empty">暂无日记</p>
      </div>
      <div class="card side-card">
        <h3>使用说明</h3>
        <div class="tips">
          <div class="tip-item">
            <span class="tip-icon">📖</span>
            <div>
              <strong>写日记</strong>
              <p>记录生活中的点滴，支持上传图片</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">🖼️</span>
            <div>
              <strong>图片上传</strong>
              <p>可以上传多张图片作为日记配图</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">📅</span>
            <div>
              <strong>时间排序</strong>
              <p>日记按时间倒序展示，最新的在最前面</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDiary, createDiary, updateDiary, deleteDiary, uploadDiaryImage, getDiaryImageUrl } from '../api'

const diary = ref([])
const showForm = ref(false)
const editMode = ref(false)
const editId = ref(null)
const fileInput = ref(null)
const form = ref({ content: '', images: [] })

const resetForm = () => {
  form.value = { content: '', images: [] }
  editId.value = null
}

const formatDate = (dateStr) => {
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
}

const load = async () => {
  const { data } = await getDiary()
  diary.value = data
}

onMounted(load)

const upload = async (e) => {
  const files = e.target.files
  for (const file of files) {
    const { data } = await uploadDiaryImage(file)
    form.value.images.push(data.url)
  }
  fileInput.value.value = ''
}

const edit = (item) => {
  form.value = { content: item.content, images: item.images || [] }
  editId.value = item.id
  editMode.value = true
  showForm.value = true
}

const create = async () => {
  await createDiary(form.value)
  showForm.value = false
  resetForm()
  load()
}

const update = async () => {
  await updateDiary(editId.value, form.value)
  showForm.value = false
  resetForm()
  load()
}

const remove = async (id) => {
  if (confirm('确定删除？')) {
    await deleteDiary(id)
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
.form textarea { width: 100%; height: 100px; padding: 12px 16px; border: 1.5px solid #e8e4df; border-radius: 10px; resize: vertical; }
.upload-area { margin-top: 10px; }
.upload-area input[type="file"] { font-size: 13px; }
.preview { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
.img-item { position: relative; width: 80px; height: 80px; }
.img-item img { width: 100%; height: 100%; object-fit: cover; border-radius: 8px; }
.img-item .remove { position: absolute; top: -6px; right: -6px; width: 20px; height: 20px; border-radius: 50%; background: #dc3545; color: #fff; font-size: 12px; display: flex; align-items: center; justify-content: center; padding: 0; }
.btns { display: flex; gap: 10px; margin-top: 10px; }
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
.diary-item { padding: 16px 0; border-bottom: 1px solid rgba(45,43,85,0.06); }
.diary-item .content { color: #2d2b55; line-height: 1.6; }
.diary-item .images { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
.diary-item .images img { width: 80px; height: 80px; object-fit: cover; border-radius: 8px; }
.diary-item .meta { display: flex; justify-content: space-between; align-items: center; margin-top: 8px; color: #999; font-size: 13px; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
.tips { display: flex; flex-direction: column; gap: 16px; }
.tip-item { display: flex; gap: 12px; align-items: flex-start; }
.tip-icon { font-size: 20px; }
.tip-item strong { color: #2d2b55; font-size: 14px; display: block; margin-bottom: 2px; }
.tip-item p { color: #888; font-size: 12px; line-height: 1.4; }
</style>
