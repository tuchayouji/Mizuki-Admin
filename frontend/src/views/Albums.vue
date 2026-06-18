<template>
  <div class="page">
    <h1>相册管理</h1>
    <div class="card">
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
          <span class="name">{{ item.title }}</span>
          <span class="desc">{{ item.description }}</span>
          <div class="tags">
            <span v-for="tag in item.tags" :key="tag" class="tag">{{ tag }}</span>
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
  form.value = {
    title: item.title || '',
    description: item.description || '',
    tagsStr: (item.tags || []).join(','),
    password: '',
    passwordHint: item.passwordHint || ''
  }
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
.page { max-width: 800px; }
h1 { margin-bottom: 20px; color: #333; }
.card { background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
button { background: #ff6b35; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; }
button.edit { background: #28a745; }
button.delete { background: #dc3545; }
button.cancel { background: #6c757d; }
.form { margin-bottom: 20px; padding: 16px; background: #f8f9fa; border-radius: 8px; display: flex; flex-direction: column; gap: 10px; }
.form input { padding: 10px; border: 1px solid #ddd; border-radius: 6px; }
.btns { display: flex; gap: 10px; }
.item { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
.item .info { display: flex; flex-direction: column; gap: 4px; flex: 1; }
.item .name { font-weight: bold; color: #333; }
.item .desc { color: #666; font-size: 13px; }
.tags { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 4px; }
.tag { padding: 2px 8px; border-radius: 4px; font-size: 12px; background: #ff6b35; color: #fff; }
.tag.locked { background: #dc3545; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
</style>
