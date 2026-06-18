import axios from 'axios'

const api = axios.create({
  baseURL: '/api'
})

export const getConfig = () => api.get('/config/')
export const updateConfig = (data) => api.put('/config/', data)
export const getPosts = () => api.get('/posts/')
export const getPost = (filename) => api.get(`/posts/${filename}`)
export const createPost = (data) => api.post('/posts/', data)
export const updatePost = (filename, data) => api.put(`/posts/${filename}`, data)
export const deletePost = (filename) => api.delete(`/posts/${filename}`)
export const getDiary = () => api.get('/diary/')
export const createDiary = (data) => api.post('/diary/', data)
export const updateDiary = (id, data) => api.put(`/diary/${id}`, data)
export const deleteDiary = (id) => api.delete(`/diary/${id}`)
export const uploadDiaryImage = (file) => {
  const fd = new FormData()
  fd.append('file', file)
  return api.post('/diary/upload', fd)
}
export const getDiaryImageUrl = (path) => {
  const filename = path.split('/').pop()
  return `/api/diary/images/${filename}`
}
export const getAnime = () => api.get('/anime/')
export const createAnime = (data) => api.post('/anime/', data)
export const updateAnime = (title, data) => api.put(`/anime/${title}`, data)
export const deleteAnime = (title) => api.delete(`/anime/${title}`)
export const getFriends = () => api.get('/friends/')
export const createFriend = (data) => api.post('/friends/', data)
export const updateFriend = (name, data) => api.put(`/friends/${name}`, data)
export const deleteFriend = (name) => api.delete(`/friends/${name}`)
export const getTheme = () => api.get('/theme/')
export const updateTheme = (data) => api.put('/theme/', data)
export const getSkills = () => api.get('/skills/')
export const createSkill = (data) => api.post('/skills/', data)
export const updateSkill = (id, data) => api.put(`/skills/${id}`, data)
export const deleteSkill = (id) => api.delete(`/skills/${id}`)
export const getTimeline = () => api.get('/timeline/')
export const createTimeline = (data) => api.post('/timeline/', data)
export const updateTimeline = (id, data) => api.put(`/timeline/${id}`, data)
export const deleteTimeline = (id) => api.delete(`/timeline/${id}`)
export const getProjects = () => api.get('/projects/')
export const createProject = (data) => api.post('/projects/', data)
export const updateProject = (id, data) => api.put(`/projects/${id}`, data)
export const deleteProject = (id) => api.delete(`/projects/${id}`)
export const getAlbums = () => api.get('/albums/')
export const createAlbum = (data) => api.post('/albums/', data)
export const updateAlbum = (id, data) => api.put(`/albums/${id}`, data)
export const deleteAlbum = (id) => api.delete(`/albums/${id}`)
