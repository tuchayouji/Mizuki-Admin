from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os

router = APIRouter()

POSTS_DIR = r"D:\boke\Mizuki\src\content\posts"

class Post(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []
    category: Optional[str] = None

@router.get("/")
def list_posts():
    posts = []
    if os.path.exists(POSTS_DIR):
        for f in os.listdir(POSTS_DIR):
            if f.endswith(".md"):
                path = os.path.join(POSTS_DIR, f)
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                title = f.replace(".md", "")
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        for line in parts[1].split("\n"):
                            if line.strip().startswith("title:"):
                                title = line.split(":", 1)[1].strip().strip('"').strip("'")
                posts.append({"filename": f, "title": title, "path": path})
    return posts

@router.post("/")
def create_post(data: Post):
    filename = data.title.replace(" ", "-").replace("/", "-") + ".md"
    path = os.path.join(POSTS_DIR, filename)
    content = f"---\ntitle: \"{data.title}\"\npublished: {datetime.now().strftime('%Y-%m-%d')}\ntags: {data.tags}\ncategory: {data.category or ''}\n---\n\n{data.content}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return {"message": "文章已创建", "filename": filename}

@router.get("/{filename}")
def get_post(filename: str):
    path = os.path.join(POSTS_DIR, filename)
    if not os.path.exists(path):
        return {"error": "文章不存在"}
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return {"filename": filename, "content": content}

@router.put("/{filename}")
def update_post(filename: str, data: Post):
    path = os.path.join(POSTS_DIR, filename)
    if not os.path.exists(path):
        return {"error": "文章不存在"}
    content = f"---\ntitle: \"{data.title}\"\npublished: {datetime.now().strftime('%Y-%m-%d')}\ntags: {data.tags}\ncategory: {data.category or ''}\n---\n\n{data.content}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return {"message": "文章已更新"}

@router.delete("/{filename}")
def delete_post(filename: str):
    path = os.path.join(POSTS_DIR, filename)
    if os.path.exists(path):
        os.remove(path)
        return {"message": "文章已删除"}
    return {"error": "文章不存在"}
