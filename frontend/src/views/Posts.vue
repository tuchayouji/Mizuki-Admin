<template>
  <div class="page">
    <h1>文章管理</h1>
    <div class="config-grid">
      <div class="card main-card">
        <div class="header">
          <h3>文章列表</h3>
          <button @click="showForm = true; editMode = false; resetForm()">新建文章</button>
        </div>
        <div v-if="showForm" class="form">
          <input v-model="form.title" placeholder="文章标题" />
          <textarea v-model="form.content" placeholder="文章内容 (Markdown格式)"></textarea>
          <div class="btns">
            <button @click="editMode ? update() : create()">{{ editMode ? '保存' : '创建' }}</button>
            <button class="cancel" @click="showForm = false">取消</button>
          </div>
        </div>
        <div v-for="post in posts" :key="post.filename" class="item">
          <div class="info">
            <span class="name" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ post.title }}</span>
            <span class="file" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ post.filename }}</span>
          </div>
          <div class="actions">
            <button class="edit" @click="edit(post)">编辑</button>
            <button class="delete" @click="remove(post.filename)">删除</button>
          </div>
        </div>
        <p v-if="!posts.length" class="empty">暂无文章</p>
      </div>
      <div class="card side-card">
        <h3>使用说明</h3>
        <div class="tips">
          <div class="tip-item">
            <span class="tip-icon">📝</span>
            <div>
              <strong>创建文章</strong>
              <p>点击右上角按钮创建新文章，支持Markdown格式</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">✏️</span>
            <div>
              <strong>编辑文章</strong>
              <p>点击编辑按钮修改已有文章内容</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">🗑️</span>
            <div>
              <strong>删除文章</strong>
              <p>删除后无法恢复，请谨慎操作</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPosts, createPost, getPost, deletePost } from '../api'
import axios from 'axios'

const posts = ref([])
const showForm = ref(false)
const editMode = ref(false)
const editFilename = ref('')
const form = ref({ title: '', content: '' })

const resetForm = () => { form.value = { title: '', content: '' } }

const load = async () => { const { data } = await getPosts(); posts.value = data }
onMounted(load)

const edit = async (post) => {
  const { data } = await axios.get(`/api/posts/${post.filename}`)
  editFilename.value = post.filename
  form.value = { title: post.title, content: data.content || '' }
  editMode.value = true
  showForm.value = true
}

const create = async () => {
  await createPost(form.value)
  showForm.value = false
  resetForm()
  load()
}

const update = async () => {
  await axios.put(`/api/posts/${editFilename.value}`, form.value)
  showForm.value = false
  resetForm()
  editMode.value = false
  load()
}

const remove = async (filename) => {
  if (confirm('确定删除这篇文章吗？')) {
    await deletePost(filename)
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
.form input, .form textarea { padding: 12px 16px; border: 1.5px solid #e8e4df; border-radius: 10px; font-size: 14px; }
.form textarea { min-height: 200px; resize: vertical; }
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
.item .info { display: flex; flex-direction: column; gap: 4px; }
.item .name { font-weight: 600; color: #2d2b55; }
.item .file { color: #999; font-size: 12px; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
.tips { display: flex; flex-direction: column; gap: 16px; }
.tip-item { display: flex; gap: 12px; align-items: flex-start; }
.tip-icon { font-size: 20px; }
.tip-item strong { color: #2d2b55; font-size: 14px; display: block; margin-bottom: 2px; }
.tip-item p { color: #888; font-size: 12px; line-height: 1.4; }
</style>
