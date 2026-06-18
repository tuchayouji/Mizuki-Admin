from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import config, posts, diary, anime, friends, theme, skills, timeline, projects, albums

app = FastAPI(title="Mizuki Admin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(config.router, prefix="/api/config", tags=["配置"])
app.include_router(posts.router, prefix="/api/posts", tags=["文章"])
app.include_router(diary.router, prefix="/api/diary", tags=["日记"])
app.include_router(anime.router, prefix="/api/anime", tags=["番剧"])
app.include_router(friends.router, prefix="/api/friends", tags=["友链"])
app.include_router(theme.router, prefix="/api/theme", tags=["主题"])
app.include_router(skills.router, prefix="/api/skills", tags=["技能"])
app.include_router(timeline.router, prefix="/api/timeline", tags=["时间线"])
app.include_router(projects.router, prefix="/api/projects", tags=["项目"])
app.include_router(albums.router, prefix="/api/albums", tags=["相册"])

@app.get("/")
def root():
    return {"message": "Mizuki Admin API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
