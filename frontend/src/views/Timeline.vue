<template>
  <div class="page">
    <h1>时间线管理</h1>
    <div class="config-grid">
      <div class="card main-card">
        <div class="header">
          <h3>时间线列表</h3>
          <button @click="showForm = true; editMode = false; resetForm()">添加经历</button>
        </div>
        <div v-if="showForm" class="form">
          <input v-model="form.id" placeholder="ID (英文)" :disabled="editMode" />
          <input v-model="form.title" placeholder="标题" />
          <input v-model="form.description" placeholder="描述" />
          <select v-model="form.type">
            <option value="education">教育经历</option>
            <option value="work">工作经历</option>
            <option value="project">项目经历</option>
            <option value="achievement">成就荣誉</option>
          </select>
          <input v-model="form.startDate" type="date" placeholder="开始日期" />
          <input v-model="form.endDate" type="date" placeholder="结束日期" />
          <input v-model="form.location" placeholder="地点" />
          <input v-model="form.organization" placeholder="机构" />
          <div class="btns">
            <button @click="editMode ? update() : create()">{{ editMode ? '保存' : '添加' }}</button>
            <button class="cancel" @click="showForm = false">取消</button>
          </div>
        </div>
        <div v-for="item in timeline" :key="item.id" class="item">
          <div class="info">
            <span class="name" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.title }}</span>
            <span class="tag" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ typeText(item.type) }}</span>
            <span class="date" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">{{ item.startDate }} {{ item.endDate ? '- ' + item.endDate : '' }}</span>
          </div>
          <div class="actions">
            <button class="edit" @click="edit(item)">编辑</button>
            <button class="delete" @click="remove(item.id)">删除</button>
          </div>
        </div>
        <p v-if="!timeline.length" class="empty">暂无经历</p>
      </div>
      <div class="card side-card">
        <h3>使用说明</h3>
        <div class="tips">
          <div class="tip-item">
            <span class="tip-icon">📅</span>
            <div>
              <strong>记录经历</strong>
              <p>记录教育、工作、项目等人生经历</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">🎓</span>
            <div>
              <strong>类型分类</strong>
              <p>教育、工作、项目、成就四种类别</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">📍</span>
            <div>
              <strong>地点机构</strong>
              <p>填写学校或公司名称和地点</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTimeline, createTimeline, updateTimeline, deleteTimeline } from '../api'

const timeline = ref([])
const showForm = ref(false)
const editMode = ref(false)
const form = ref({ id: '', title: '', description: '', type: 'education', startDate: '', endDate: '', location: '', organization: '' })

const resetForm = () => { form.value = { id: '', title: '', description: '', type: 'education', startDate: '', endDate: '', location: '', organization: '' } }
const typeText = (t) => ({ education: '教育', work: '工作', project: '项目', achievement: '成就' }[t])

const load = async () => { const { data } = await getTimeline(); timeline.value = data }
onMounted(load)
const edit = (item) => { form.value = { ...item }; editMode.value = true; showForm.value = true }
const create = async () => { await createTimeline(form.value); showForm.value = false; resetForm(); load() }
const update = async () => { await updateTimeline(form.value.id, form.value); showForm.value = false; resetForm(); load() }
const remove = async (id) => { if (confirm('确定删除？')) { await deleteTimeline(id); load() } }
</script>

<style scoped>
.page { max-width: 900px; }
h1 { margin-bottom: 24px; color: #2d2b55; font-weight: 700; font-size: 24px; }
.config-grid { display: grid; grid-template-columns: 1.5fr 1fr; gap: 20px; }
.card { background: #fff; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(45,43,85,0.06); border: 1px solid rgba(45,43,85,0.06); }
.card h3 { color: #2d2b55; font-size: 16px; margin-bottom: 20px; padding-bottom: 12px; border-bottom: 2px solid #ff6b35; display: inline-block; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.form { margin-bottom: 20px; padding: 16px; background: #faf5f0; border-radius: 12px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.form input, .form select { padding: 12px 16px; border: 1.5px solid #e8e4df; border-radius: 10px; font-size: 14px; }
.btns { grid-column: 1 / -1; display: flex; gap: 10px; }
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
.item .info { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.item .name { font-weight: 600; color: #2d2b55; }
.tag { padding: 3px 10px; border-radius: 6px; font-size: 12px; background: linear-gradient(135deg, #ff6b35, #ff8c42); color: #fff; font-weight: 600; }
.date { color: #999; font-size: 13px; }
.actions { display: flex; gap: 6px; }
.empty { color: #999; text-align: center; padding: 20px; }
.tips { display: flex; flex-direction: column; gap: 16px; }
.tip-item { display: flex; gap: 12px; align-items: flex-start; }
.tip-icon { font-size: 20px; }
.tip-item strong { color: #2d2b55; font-size: 14px; display: block; margin-bottom: 2px; }
.tip-item p { color: #888; font-size: 12px; line-height: 1.4; }
</style>
