<template>
  <div class="page">
    <h1>主题配置</h1>
    <div class="card">
      <div class="form-item">
        <label>主题色色相 (0-360)</label>
        <input v-model.number="form.hue" type="range" min="0" max="360" />
        <span class="preview" :style="{ background: `hsl(${form.hue}, 70%, 60%)` }">{{ form.hue }}</span>
      </div>
      <div class="form-item">
        <label>
          <input type="checkbox" v-model="form.fixed" />
          锁定主题色（访客不可切换）
        </label>
      </div>
      <button @click="save">保存</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTheme, updateTheme } from '../api'

const form = ref({ hue: 240, fixed: false })

onMounted(async () => {
  const { data } = await getTheme()
  form.value = data
})

const save = async () => {
  await updateTheme(form.value)
  alert('保存成功')
}
</script>

<style scoped>
.page { max-width: 600px; }
h1 { margin-bottom: 20px; color: #333; }
.card { background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.form-item { margin-bottom: 20px; }
.form-item label { display: block; margin-bottom: 8px; color: #666; font-size: 14px; }
.form-item input[type="range"] { width: 80%; }
.preview {
  display: inline-block;
  margin-left: 10px;
  padding: 2px 10px;
  border-radius: 4px;
  color: #fff;
  font-weight: bold;
}
button {
  background: #ff6b35;
  color: #fff;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  cursor: pointer;
}
button:hover { background: #e55a2b; }
</style>
