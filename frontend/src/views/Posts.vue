<template>
  <div class="page">
    <h1>文章管理</h1>
    <div class="card">
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
          <span class="name">{{ post.title }}</span>
          <span class="file">{{ post.filename }}</span>
        </div>
        <div class="actions">
          <button class="edit" @click="edit(post)">编辑</button>
          <button class="delete" @click="remove(post.filename)">删除</button>
        </div>
      </div>
      <p v-if="!posts.length" class="empty">暂无文章</p>
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
.page { max-width: 800px; }
h1 { margin-bottom: 20px; color: #333; }
.card { background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
button { background: #ff6b35; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; }
button.edit { background: #28a745; }
button.delete { background: #dc3545; }
button.cancel { background: #6c757d; }
.form { margin-bottom: 20px; padding: 16px; background: #f8f9fa; border-radius: 8px; display: flex; flex-direction: column; gap: 10px; }
.form input, .form textarea { padding: 10px; border: 1px solid #ddd; border-radius: 6px; }
.form textarea { min-height: 200px; resize: vertical; }
.btns { display: flex; gap: 10px; }
.item { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
.item .info { display: flex; flex-direction: column; gap: 4px; }
.item .name { font-weight: bold; color: #333; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.item .file { color: #999; font-size: 12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
</style>
