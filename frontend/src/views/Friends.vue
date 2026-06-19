<template>
  <div class="page">
    <h1>友链管理</h1>
    <div class="config-grid">
      <div class="card main-card">
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
            <span class="name" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.name }}</span>
            <a :href="item.url" target="_blank" class="link" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.url }}</a>
            <span class="desc" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.description }}</span>
          </div>
          <div class="actions">
            <button class="edit" @click="edit(item)">编辑</button>
            <button class="delete" @click="remove(item.name)">删除</button>
          </div>
        </div>
        <p v-if="!friends.length" class="empty">暂无友链</p>
      </div>
      <div class="card side-card">
        <h3>使用说明</h3>
        <div class="tips">
          <div class="tip-item">
            <span class="tip-icon">👥</span>
            <div>
              <strong>添加友链</strong>
              <p>添加其他博主的链接，互相引流</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">🖼️</span>
            <div>
              <strong>头像设置</strong>
              <p>填入对方的头像图片链接</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">🏷️</span>
            <div>
              <strong>标签分类</strong>
              <p>用标签对友链进行分类管理</p>
            </div>
          </div>
        </div>
      </div>
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
  form.value = { name: item.name, url: item.url, avatar: item.avatar || '', description: item.description || '', tagsStr: (item.tags || []).join(',') }
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
.item .link { color: #007bff; font-size: 13px; text-decoration: none; }
.item .desc { color: #666; font-size: 13px; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
.tips { display: flex; flex-direction: column; gap: 16px; }
.tip-item { display: flex; gap: 12px; align-items: flex-start; }
.tip-icon { font-size: 20px; }
.tip-item strong { color: #2d2b55; font-size: 14px; display: block; margin-bottom: 2px; }
.tip-item p { color: #888; font-size: 12px; line-height: 1.4; }
</style>
