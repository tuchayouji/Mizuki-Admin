<template>
  <div class="page">
    <h1>相册管理</h1>
    <div class="config-grid">
      <div class="card main-card">
        <div class="header">
          <h3>相册列表</h3>
          <button @click="showForm = true; editMode = false; resetForm()">创建相册</button>
        </div>
        <div v-if="showForm" class="form">
          <input v-model="form.title" placeholder="相册标题" />
          <input v-model="form.description" placeholder="描述" />
          <input v-model="form.tagsStr" placeholder="标签 (逗号分隔)" />
          <input v-model="form.password" placeholder="密码 (加密相册)" />
          <input v-model="form.passwordHint" placeholder="密码提示" />
          <div class="btns">
            <button @click="editMode ? update() : create()">{{ editMode ? '保存' : '创建' }}</button>
            <button class="cancel" @click="showForm = false">取消</button>
          </div>
        </div>
        <div v-for="item in albums" :key="item.id" class="item">
          <div class="info">
            <span class="name" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.title }}</span>
            <span class="desc" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.description }}</span>
            <div class="tags">
              <span v-for="tag in item.tags" :key="tag" class="tag" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ tag }}</span>
              <span v-if="item.password" class="tag locked">🔒 加密</span>
            </div>
          </div>
          <div class="actions">
            <button class="edit" @click="edit(item)">编辑</button>
            <button class="delete" @click="remove(item.id)">删除</button>
          </div>
        </div>
        <p v-if="!albums.length" class="empty">暂无相册</p>
      </div>
      <div class="card side-card">
        <h3>使用说明</h3>
        <div class="tips">
          <div class="tip-item">
            <span class="tip-icon">🖼️</span>
            <div>
              <strong>创建相册</strong>
              <p>创建图片相册，展示你的摄影作品</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">🔒</span>
            <div>
              <strong>加密相册</strong>
              <p>设置密码保护私密相册</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">🏷️</span>
            <div>
              <strong>标签分类</strong>
              <p>用标签对相册进行分类管理</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAlbums, createAlbum, updateAlbum, deleteAlbum } from '../api'

const albums = ref([])
const showForm = ref(false)
const editMode = ref(false)
const editId = ref('')
const form = ref({ title: '', description: '', tagsStr: '', password: '', passwordHint: '' })

const resetForm = () => { form.value = { title: '', description: '', tagsStr: '', password: '', passwordHint: '' } }

const load = async () => { const { data } = await getAlbums(); albums.value = data }
onMounted(load)

const edit = (item) => {
  editId.value = item.id
  form.value = { title: item.title || '', description: item.description || '', tagsStr: (item.tags || []).join(','), password: '', passwordHint: item.passwordHint || '' }
  editMode.value = true
  showForm.value = true
}

const create = async () => {
  const data = { ...form.value, tags: form.value.tagsStr.split(',').map(t => t.trim()).filter(Boolean) }
  await createAlbum(data)
  showForm.value = false
  resetForm()
  load()
}

const update = async () => {
  const data = { ...form.value, tags: form.value.tagsStr.split(',').map(t => t.trim()).filter(Boolean) }
  await updateAlbum(editId.value, data)
  showForm.value = false
  resetForm()
  editMode.value = false
  load()
}

const remove = async (id) => {
  if (confirm('确定删除这个相册吗？')) {
    await deleteAlbum(id)
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
.btns { display: flex; gap: 10px; }
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
.item .info { display: flex; flex-direction: column; gap: 4px; flex: 1; }
.item .name { font-weight: 600; color: #2d2b55; }
.item .desc { color: #666; font-size: 13px; }
.tags { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 4px; }
.tag { padding: 3px 10px; border-radius: 6px; font-size: 12px; background: linear-gradient(135deg, #ff6b35, #ff8c42); color: #fff; font-weight: 600; }
.tag.locked { background: linear-gradient(135deg, #dc3545, #e85d6a); }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
.tips { display: flex; flex-direction: column; gap: 16px; }
.tip-item { display: flex; gap: 12px; align-items: flex-start; }
.tip-icon { font-size: 20px; }
.tip-item strong { color: #2d2b55; font-size: 14px; display: block; margin-bottom: 2px; }
.tip-item p { color: #888; font-size: 12px; line-height: 1.4; }
</style>
