from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import re
import requests
import os
import shutil
from datetime import datetime

router = APIRouter()

ANIME_PATH = r"D:\boke\Mizuki\src\data\anime.ts"
ANIME_IMG_DIR = r"D:\boke\Mizuki\public\assets\anime"

os.makedirs(ANIME_IMG_DIR, exist_ok=True)

@router.get("/images/{filename}")
def get_anime_image(filename: str):
    """直接从博客目录返回图片"""
    filepath = os.path.join(ANIME_IMG_DIR, filename)
    if os.path.exists(filepath):
        return FileResponse(filepath)
    return {"error": "not found"}

class AnimeItem(BaseModel):
    title: str
    status: str
    rating: float
    cover: Optional[str] = ""
    description: Optional[str] = ""
    episodes: Optional[str] = "12 episodes"
    year: Optional[str] = ""
    genre: Optional[List[str]] = []
    studio: Optional[str] = ""
    link: Optional[str] = ""
    progress: Optional[int] = 0
    totalEpisodes: Optional[int] = 12
    startDate: Optional[str] = ""
    endDate: Optional[str] = ""

class BilibiliLink(BaseModel):
    url: str

def parse_anime():
    with open(ANIME_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    items = []
    pattern = r'\{\s*title:\s*"([^"]*)",\s*status:\s*"([^"]*)",\s*rating:\s*([\d.]+),\s*cover:\s*"([^"]*)",\s*description:\s*"([^"]*)",\s*episodes:\s*"([^"]*)",\s*year:\s*"([^"]*)",\s*genre:\s*\[([^\]]*)\],\s*studio:\s*"([^"]*)",\s*link:\s*"([^"]*)",\s*progress:\s*(\d+),\s*totalEpisodes:\s*(\d+),\s*startDate:\s*"([^"]*)",\s*endDate:\s*"([^"]*)"'
    for match in re.finditer(pattern, content):
        genre_list = [g.strip().strip('"') for g in match.group(8).split(",")]
        items.append({
            "title": match.group(1),
            "status": match.group(2),
            "rating": float(match.group(3)),
            "cover": match.group(4),
            "description": match.group(5),
            "episodes": match.group(6),
            "year": match.group(7),
            "genre": genre_list,
            "studio": match.group(9),
            "link": match.group(10),
            "progress": int(match.group(11)),
            "totalEpisodes": int(match.group(12)),
            "startDate": match.group(13),
            "endDate": match.group(14)
        })
    return items

def write_anime(items: list):
    lines = ['import type { AnimeItem } from "../types/config";\n', '', 'const localAnimeList: AnimeItem[] = [']
    for item in items:
        genre_str = ", ".join(f'"{g}"' for g in item["genre"])
        desc = item["description"].replace("\n", "\\n").replace('"', '\\"')
        lines.append(f'\t{{\n\t\ttitle: "{item["title"]}",\n\t\tstatus: "{item["status"]}",\n\t\trating: {item["rating"]},\n\t\tcover: "{item["cover"]}",\n\t\tdescription: "{item["description"]}",\n\t\tepisodes: "{item["episodes"]}",\n\t\tyear: "{item["year"]}",\n\t\tgenre: [{genre_str}],\n\t\tstudio: "{item["studio"]}",\n\t\tlink: "{item["link"]}",\n\t\tprogress: {item["progress"]},\n\t\ttotalEpisodes: {item["totalEpisodes"]},\n\t\tstartDate: "{item["startDate"]}",\n\t\tendDate: "{item["endDate"]}"\n\t}},')
    lines.append('];\n\nexport default localAnimeList;\n')
    with open(ANIME_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

@router.get("/")
def list_anime():
    return parse_anime()

@router.post("/fetch")
def fetch_anime_info(data: BilibiliLink):
    """从B站链接获取番剧信息并自动简化"""
    try:
        media_match = re.search(r'media/md(\d+)', data.url)
        if not media_match:
            return {"error": "无效的B站番剧链接"}
        
        media_id = media_match.group(1)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com"
        }
        
        # 使用数据更全的API
        info = None
        resp = requests.get(f"https://api.bilibili.com/pgc/view/web/media?media_id={media_id}", headers=headers, timeout=10)
        result = resp.json()
        if result.get("code") == 0:
            info = result.get("result", {})
        
        if not info:
            return {"error": "获取番剧信息失败，请检查链接"}
        
        # 标题
        title = info.get("title", "")
        
        # 封面
        cover = info.get("cover", "")
        if cover and not cover.startswith("http"):
            cover = f"https:{cover}"
        
        # 简化简介
        desc = info.get("evaluate", "")
        if desc and len(desc) > 80:
            for i, c in enumerate(desc):
                if c in "。！？" and i > 30:
                    desc = desc[:i+1]
                    break
            else:
                desc = desc[:80] + "..."
        
        # 评分
        rating_obj = info.get("rating", {})
        score = rating_obj.get("score", 0) if rating_obj else 0
        
        # 集数（从episode_index获取）
        episodes = 0
        ep_index = info.get("episode_index", {})
        if ep_index:
            try:
                episodes = int(ep_index.get("index", 0))
            except:
                pass
        if not episodes:
            new_ep = info.get("new_ep", {})
            if new_ep:
                try:
                    episodes = int(new_ep.get("index", 0))
                except:
                    pass
        
        # 年份（从pub_date获取）
        year = ""
        publish = info.get("publish", {})
        if publish:
            pub_date = publish.get("pub_date", "")
            if pub_date:
                year = pub_date[:4]
        
        # 类型（注意是styles不是style）
        genres = []
        styles = info.get("styles", [])
        if styles:
            genres = [s.get("name", "") for s in styles[:4]]
        
        # 制作公司（staff是字符串，需解析"动画制作：XXX"）
        studio = ""
        staff_str = info.get("staff", "")
        if staff_str and isinstance(staff_str, str):
            for line in staff_str.split("\n"):
                if "动画制作" in line:
                    parts = line.split("：")
                    if len(parts) > 1:
                        studio = parts[-1].strip()
                    break
        
        return {
            "title": title,
            "cover": cover,
            "description": desc or "",
            "rating": score,
            "episodes": episodes,
            "year": year,
            "genres": genres,
            "studio": studio,
            "link": data.url
        }
    except Exception as e:
        return {"error": f"获取失败: {str(e)}"}

@router.post("/")
def create_anime(data: AnimeItem):
    items = parse_anime()
    items.append(data.model_dump())
    write_anime(items)
    return {"message": "番剧已添加"}

@router.put("/{title}")
def update_anime(title: str, data: AnimeItem):
    items = parse_anime()
    for i, item in enumerate(items):
        if item["title"] == title:
            items[i] = data.model_dump()
            break
    write_anime(items)
    return {"message": "番剧已更新"}

@router.delete("/{title}")
def delete_anime(title: str):
    items = parse_anime()
    items = [i for i in items if i["title"] != title]
    write_anime(items)
    return {"message": "番剧已删除"}

@router.post("/upload-cover")
async def upload_cover(file: UploadFile = File(...)):
    """上传封面图片"""
    filename = f"{int(datetime.now().timestamp())}_{file.filename}"
    filepath = os.path.join(ANIME_IMG_DIR, filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"url": f"/assets/anime/{filename}"}

@router.post("/download-cover")
def download_cover(data: dict):
    """从URL下载封面图片"""
    url = data.get("url", "")
    if not url:
        return {"error": "请提供图片URL"}
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.bilibili.com"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            ext = url.split(".")[-1].split("?")[0]
            if ext not in ["jpg", "jpeg", "png", "webp", "gif"]:
                ext = "jpg"
            filename = f"{int(datetime.now().timestamp())}.{ext}"
            filepath = os.path.join(ANIME_IMG_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(resp.content)
            return {"url": f"/assets/anime/{filename}"}
        return {"error": "下载失败"}
    except Exception as e:
        return {"error": f"下载失败: {str(e)}"}
