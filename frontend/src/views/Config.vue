<template>
  <div class="page">
    <h1>站点配置</h1>
    <div class="card">
      <div class="form-item">
        <label>站点标题</label>
        <input v-model="form.title" placeholder="站点标题" />
      </div>
      <div class="form-item">
        <label>副标题</label>
        <input v-model="form.subtitle" placeholder="副标题" />
      </div>
      <div class="form-item">
        <label>站点URL</label>
        <input v-model="form.siteURL" placeholder="https://example.com/" />
      </div>
      <div class="form-item">
        <label>开始日期</label>
        <input v-model="form.siteStartDate" type="date" />
      </div>
      <button @click="save">保存配置</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getConfig, updateConfig } from '../api'

const form = ref({ title: '', subtitle: '', siteURL: '', siteStartDate: '' })

onMounted(async () => {
  const { data } = await getConfig()
  form.value = data
})

const save = async () => {
  await updateConfig(form.value)
  alert('保存成功')
}
</script>

<style scoped>
.page { max-width: 600px; }
h1 { margin-bottom: 20px; color: #333; }
.card { background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.form-item { margin-bottom: 16px; }
.form-item label { display: block; margin-bottom: 6px; color: #666; font-size: 14px; }
.form-item input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}
button {
  background: #ff6b35;
  color: #fff;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}
button:hover { background: #e55a2b; }
</style>
