<template>
  <div class="page">
    <h1>主题配置</h1>
    <div class="config-grid">
      <div class="card main-card">
        <!-- 主题色 -->
        <div class="section">
          <div class="section-header">
            <h3>主题色</h3>
            <label class="lock-label">
              <input type="checkbox" v-model="themeForm.fixed" />
              锁定主题色（访客不可切换）
            </label>
          </div>
          <div class="form">
            <div class="form-item">
              <label>主题色色相 (0-360)</label>
              <div class="hue-control">
                <input v-model.number="themeForm.hue" type="range" min="0" max="360" />
                <input v-model.number="themeForm.hue" type="number" min="0" max="360" class="hue-input" />
              </div>
              <div class="preview" :style="{ background: `hsl(${themeForm.hue}, 70%, 60%)` }">当前色相: {{ themeForm.hue }}</div>
            </div>
          </div>
        </div>

        <!-- 壁纸区域 -->
        <div class="section">
          <div class="section-header">
            <h3>壁纸</h3>
            <label class="lock-label">
              <input type="checkbox" v-model="displayForm.fixedWallpaper" />
              锁定壁纸（访客不可切换）
            </label>
          </div>
          <div class="option-group">
            <div v-for="mode in wallpaperModes" :key="mode.value"
              class="option-item" :class="{ active: displayForm.wallpaperMode === mode.value }"
              @click="displayForm.wallpaperMode = mode.value">
              <span class="option-icon">{{ mode.icon }}</span>
              <span class="option-label">{{ mode.label }}</span>
              <span class="check" v-if="displayForm.wallpaperMode === mode.value">✓</span>
            </div>
          </div>
        </div>

        <!-- 横幅选项 -->
        <div class="section">
          <div class="section-header">
            <h3>横幅选项</h3>
            <label class="lock-label">
              <input type="checkbox" v-model="displayForm.fixedBanner" />
              锁定横幅（访客不可切换）
            </label>
          </div>
          <div class="toggle-group">
            <div class="toggle-item">
              <span>横幅标题</span>
              <label class="switch">
                <input type="checkbox" v-model="displayForm.bannerTitle" />
                <span class="slider"></span>
              </label>
            </div>
            <div class="toggle-item">
              <span>水波纹动画</span>
              <label class="switch">
                <input type="checkbox" v-model="displayForm.bannerWaves" />
                <span class="slider"></span>
              </label>
            </div>
          </div>
        </div>

        <!-- 布局区域 -->
        <div class="section">
          <div class="section-header">
            <h3>布局</h3>
            <label class="lock-label">
              <input type="checkbox" v-model="displayForm.fixedLayout" />
              锁定布局（访客不可切换）
            </label>
          </div>
          <div class="option-group">
            <div v-for="mode in layoutModes" :key="mode.value"
              class="option-item" :class="{ active: displayForm.postListMode === mode.value }"
              @click="displayForm.postListMode = mode.value">
              <span class="option-icon">{{ mode.icon }}</span>
              <span class="option-label">{{ mode.label }}</span>
              <span class="check" v-if="displayForm.postListMode === mode.value">✓</span>
            </div>
          </div>
        </div>

        <button @click="save" class="save-btn">保存设置</button>
      </div>
      <div class="card side-card">
        <h3>设置说明</h3>
        <div class="tips">
          <div class="tip-item">
            <span class="tip-icon">🎨</span>
            <div>
              <strong>主题色色相</strong>
              <p>调整网站的主色调，0=红色，120=绿色，240=蓝色</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">🔒</span>
            <div>
              <strong>锁定功能</strong>
              <p>锁定后访客在博客界面将无法看到对应的切换按钮</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">🖼️</span>
            <div>
              <strong>壁纸模式</strong>
              <p>横幅=顶部图片，全屏=整页背景，隐藏=纯色背景</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">✨</span>
            <div>
              <strong>横幅选项</strong>
              <p>控制首页标题文字和底部水波纹动画效果</p>
            </div>
          </div>
          <div class="tip-item">
            <span class="tip-icon">📐</span>
            <div>
              <strong>文章布局</strong>
              <p>列表=单列展示，网格=双列卡片展示</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTheme, updateTheme } from '../api'
import { getDisplaySettings, updateDisplaySettings } from '../api'

const themeForm = ref({ hue: 240, fixed: false })
const displayForm = ref({
  wallpaperMode: 'banner',
  bannerTitle: true,
  bannerWaves: true,
  postListMode: 'list',
  fixedWallpaper: false,
  fixedBanner: false,
  fixedLayout: false
})

const wallpaperModes = [
  { value: 'banner', icon: '🖼️', label: '横幅模式' },
  { value: 'fullscreen', icon: '🖥️', label: '全屏模式' },
  { value: 'none', icon: '🚫', label: '隐藏壁纸' }
]

const layoutModes = [
  { value: 'list', icon: '📋', label: '列表' },
  { value: 'grid', icon: '📐', label: '网格' }
]

onMounted(async () => {
  const [themeRes, displayRes] = await Promise.all([getTheme(), getDisplaySettings()])
  themeForm.value = themeRes.data
  displayForm.value = { ...displayForm.value, ...displayRes.data }
})

const save = async () => {
  await Promise.all([updateTheme(themeForm.value), updateDisplaySettings(displayForm.value)])
  alert('保存成功')
}
</script>

<style scoped>
.page { max-width: 900px; }
h1 { margin-bottom: 24px; color: #2d2b55; font-weight: 700; font-size: 24px; }
.config-grid { display: grid; grid-template-columns: 1.5fr 1fr; gap: 20px; }
.card { background: #fff; padding: 24px; border-radius: 16px; box-shadow: 0 2px 12px rgba(45,43,85,0.06); border: 1px solid rgba(45,43,85,0.06); }
.card h3 { color: #2d2b55; font-size: 16px; }
.section { margin-bottom: 28px; }
.section-header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 10px; border-bottom: 2px solid #ff6b35; margin-bottom: 16px; }
.section-header h3 { margin: 0; }

.lock-label {
  display: flex; align-items: center; gap: 8px;
  font-size: 13px; color: #666; cursor: pointer; font-weight: 500;
}
.lock-label input[type="checkbox"] { accent-color: #2563eb; width: 16px; height: 16px; }

.form { display: flex; flex-direction: column; gap: 16px; }
.form-item { display: flex; flex-direction: column; gap: 6px; }
.form-item label { color: #666; font-size: 13px; font-weight: 600; }
.checkbox-label { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.hue-control { display: flex; gap: 12px; align-items: center; }
.hue-control input[type="range"] { flex: 1; accent-color: #ff6b35; }
.hue-input { width: 70px; padding: 8px 12px; border: 1.5px solid #e8e4df; border-radius: 10px; font-size: 14px; text-align: center; }
.hue-input:focus { border-color: #ff6b35; box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1); outline: none; }
.preview { margin-top: 8px; padding: 8px 16px; border-radius: 10px; color: #fff; font-weight: 600; font-size: 14px; display: inline-block; }

.option-group { display: flex; flex-direction: column; gap: 8px; }
.option-item {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 16px; border-radius: 12px; background: #faf5f0;
  cursor: pointer; transition: all 0.2s; border: 2px solid transparent;
}
.option-item:hover { background: #f0ebe5; }
.option-item.active { border-color: #ff6b35; background: rgba(255, 107, 53, 0.08); }
.option-icon { font-size: 18px; }
.option-label { flex: 1; font-size: 14px; color: #2d2b55; font-weight: 500; }
.check {
  width: 24px; height: 24px; border-radius: 50%;
  background: #ff6b35; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 700;
}

.toggle-group { display: flex; flex-direction: column; gap: 12px; }
.toggle-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 16px; border-radius: 12px; background: #faf5f0;
}
.toggle-item span { font-size: 14px; color: #2d2b55; font-weight: 500; }

.switch { position: relative; display: inline-block; width: 48px; height: 26px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider {
  position: absolute; cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #ccc; transition: 0.3s; border-radius: 26px;
}
.slider:before {
  position: absolute; content: "";
  height: 20px; width: 20px; left: 3px; bottom: 3px;
  background-color: white; transition: 0.3s; border-radius: 50%;
}
input:checked + .slider { background-color: #ff6b35; }
input:checked + .slider:before { transform: translateX(22px); }
input:disabled + .slider { opacity: 0.5; cursor: not-allowed; }

.save-btn {
  background: linear-gradient(135deg, #ff6b35, #ff8c42);
  color: #fff; border: none; padding: 12px 24px;
  border-radius: 10px; cursor: pointer; font-size: 14px;
  font-weight: 600; transition: all 0.2s; width: 100%;
}
.save-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3); }

.tips { display: flex; flex-direction: column; gap: 16px; }
.tip-item { display: flex; gap: 12px; align-items: flex-start; }
.tip-icon { font-size: 20px; }
.tip-item strong { color: #2d2b55; font-size: 14px; display: block; margin-bottom: 2px; }
.tip-item p { color: #888; font-size: 12px; line-height: 1.4; }
</style>
