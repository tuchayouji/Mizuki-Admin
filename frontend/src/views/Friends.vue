<template>
  <div class="page">
    <h1>友链管理</h1>
    <div class="card">
      <div class="header">
        <h3>友链列表</h3>
        <button @click="showForm = true; editMode = false; resetForm()">添加友链</button>
      </div>
      <div v-if="showForm" class="form">
        <input v-model="form.name" placeholder="名称" />
        <input v-model="form.url" placeholder="链接" />
        <input v-model="form.avatar" placeholder="头像链接" />
        <input v-model="form.description" placeholder="简介" />
        <input v-model="form.tagsStr" placeholder="标签 (逗号分隔)" />
        <div class="btns">
          <button @click="editMode ? update() : create()">{{ editMode ? '保存' : '添加' }}</button>
          <button class="cancel" @click="showForm = false">取消</button>
        </div>
      </div>
      <div v-for="item in friends" :key="item.name" class="item">
        <div class="info">
          <span class="name">{{ item.name }}</span>
          <a :href="item.url" target="_blank" class="link">{{ item.url }}</a>
          <span class="desc">{{ item.description }}</span>
        </div>
        <div class="actions">
          <button class="edit" @click="edit(item)">编辑</button>
          <button class="delete" @click="remove(item.name)">删除</button>
        </div>
      </div>
      <p v-if="!friends.length" class="empty">暂无友链</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getFriends, createFriend, updateFriend, deleteFriend } from '../api'

const friends = ref([])
const showForm = ref(false)
const editMode = ref(false)
const editName = ref('')
const form = ref({ name: '', url: '', avatar: '', description: '', tagsStr: '' })

const resetForm = () => { form.value = { name: '', url: '', avatar: '', description: '', tagsStr: '' } }

const load = async () => { const { data } = await getFriends(); friends.value = data }
onMounted(load)

const edit = (item) => {
  editName.value = item.name
  form.value = {
    name: item.name,
    url: item.url,
    avatar: item.avatar || '',
    description: item.description || '',
    tagsStr: (item.tags || []).join(',')
  }
  editMode.value = true
  showForm.value = true
}

const create = async () => {
  const data = { ...form.value, tags: form.value.tagsStr.split(',').map(t => t.trim()).filter(Boolean) }
  await createFriend(data)
  showForm.value = false
  resetForm()
  load()
}

const update = async () => {
  const data = { ...form.value, tags: form.value.tagsStr.split(',').map(t => t.trim()).filter(Boolean) }
  await updateFriend(editName.value, data)
  showForm.value = false
  resetForm()
  editMode.value = false
  load()
}

const remove = async (name) => {
  if (confirm('确定删除这个友链吗？')) {
    await deleteFriend(name)
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
.item .link { color: #007bff; font-size: 13px; text-decoration: none; }
.item .desc { color: #666; font-size: 13px; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
</style>
