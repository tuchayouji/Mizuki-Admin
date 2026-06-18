import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import ConfigView from './views/Config.vue'
import PostsView from './views/Posts.vue'
import DiaryView from './views/Diary.vue'
import AnimeView from './views/Anime.vue'
import FriendsView from './views/Friends.vue'
import ThemeView from './views/Theme.vue'
import SkillsView from './views/Skills.vue'
import TimelineView from './views/Timeline.vue'
import ProjectsView from './views/Projects.vue'
import AlbumsView from './views/Albums.vue'

const routes = [
  { path: '/', redirect: '/config' },
  { path: '/config', component: ConfigView },
  { path: '/posts', component: PostsView },
  { path: '/diary', component: DiaryView },
  { path: '/anime', component: AnimeView },
  { path: '/friends', component: FriendsView },
  { path: '/theme', component: ThemeView },
  { path: '/skills', component: SkillsView },
  { path: '/timeline', component: TimelineView },
  { path: '/projects', component: ProjectsView },
  { path: '/albums', component: AlbumsView },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
