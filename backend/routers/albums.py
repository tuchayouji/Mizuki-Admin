from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import os, json

router = APIRouter()

ALBUMS_DIR = r"D:\boke\Mizuki\public\images\albums"

class Album(BaseModel):
    title: str
    description: Optional[str] = ""
    tags: Optional[List[str]] = []
    password: Optional[str] = ""
    passwordHint: Optional[str] = ""

def parse_albums():
    albums = []
    if not os.path.exists(ALBUMS_DIR):
        return albums
    for folder in os.listdir(ALBUMS_DIR):
        info_path = os.path.join(ALBUMS_DIR, folder, "info.json")
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                info = json.load(f)
            info["id"] = folder
            albums.append(info)
    return albums

@router.get("/")
def list_albums():
    return parse_albums()

@router.get("/{album_id}")
def get_album(album_id: str):
    info_path = os.path.join(ALBUMS_DIR, album_id, "info.json")
    if os.path.exists(info_path):
        with open(info_path, "r", encoding="utf-8") as f:
            info = json.load(f)
        info["id"] = album_id
        return info
    return {"error": "相册不存在"}

@router.post("/")
def create_album(data: Album):
    album_id = data.title.replace(" ", "_").lower()
    album_dir = os.path.join(ALBUMS_DIR, album_id)
    os.makedirs(album_dir, exist_ok=True)
    info = {
        "title": data.title,
        "description": data.description,
        "tags": data.tags,
        "hidden": False,
        "date": "2026-06-18"
    }
    if data.password:
        info["password"] = data.password
        info["passwordHint"] = data.passwordHint or ""
    with open(os.path.join(album_dir, "info.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, indent=4, ensure_ascii=False)
    return {"message": "相册已创建", "id": album_id}

@router.put("/{album_id}")
def update_album(album_id: str, data: Album):
    info_path = os.path.join(ALBUMS_DIR, album_id, "info.json")
    if os.path.exists(info_path):
        with open(info_path, "r", encoding="utf-8") as f:
            info = json.load(f)
        info["title"] = data.title
        info["description"] = data.description
        if data.tags:
            info["tags"] = data.tags
        if data.password:
            info["password"] = data.password
            info["passwordHint"] = data.passwordHint or ""
        with open(info_path, "w", encoding="utf-8") as f:
            json.dump(info, f, indent=4, ensure_ascii=False)
        return {"message": "相册已更新"}
    return {"error": "相册不存在"}

@router.delete("/{album_id}")
def delete_album(album_id: str):
    album_dir = os.path.join(ALBUMS_DIR, album_id)
    if os.path.exists(album_dir):
        import shutil
        shutil.rmtree(album_dir)
        return {"message": "相册已删除"}
    return {"error": "相册不存在"}
