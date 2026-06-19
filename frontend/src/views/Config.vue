<template>
  <div class="page">
    <h1>站点配置</h1>
    <div class="config-grid">
      <div class="card main-card">
        <h3>基本信息</h3>
        <div class="form">
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
      <div class="card side-card">
        <h3>配置说明</h3>
        <div class="tips">
          <div class="tip-item">
            <span class="tip-icon">💡</span>
            <div>
              <strong>站点标题</strong>
              <p>显示在浏览器标签页和导航栏上</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">📝</span>
            <div>
              <strong>副标题</strong>
              <p>显示在首页横幅下方的一句话介绍</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">🔗</span>
            <div>
              <strong>站点URL</strong>
              <p>你的博客访问地址，用于生成链接</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">📅</span>
            <div>
              <strong>开始日期</strong>
              <p>用于计算博客运行天数</p>
            </div>
          </div>
        </div>
      </div>
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
.page { max-width: 900px; }
h1 { margin-bottom: 24px; color: #2d2b55; font-weight: 700; font-size: 24px; }
.config-grid { display: grid; grid-template-columns: 1.5fr 1fr; gap: 20px; }
.card { background: #fff; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(45,43,85,0.06); border: 1px solid rgba(45,43,85,0.06); }
.card h3 { color: #2d2b55; font-size: 16px; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 2px solid #ff6b35; display: inline-block; }
.form { display: flex; flex-direction: column; gap: 16px; }
.form-item { display: flex; flex-direction: column; gap: 6px; }
.form-item label { color: #666; font-size: 13px; font-weight: 600; }
.form-item input {
  padding: 12px 16px;
  border: 1.5px solid #e8e4df;
  border-radius: 10px;
  font-size: 14px;
  font-family: 'Nunito', sans-serif;
  transition: all 0.2s;
}
.form-item input:focus {
  border-color: #ff6b35;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
  outline: none;
}
button {
  background: linear-gradient(135deg, #ff6b35, #ff8c42);
  color: #fff;
  border: none;
  padding: 12px 24px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
  margin-top: 8px;
}
button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
}
.tips { display: flex; flex-direction: column; gap: 16px; }
.tip-item { display: flex; gap: 12px; align-items: flex-start; }
.tip-icon { font-size: 20px; }
.tip-item strong { color: #2d2b55; font-size: 14px; display: block; margin-bottom: 2px; }
.tip-item p { color: #888; font-size: 12px; line-height: 1.4; }
</style>
