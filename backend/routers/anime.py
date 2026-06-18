from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import re

router = APIRouter()

ANIME_PATH = r"D:\boke\Mizuki\src\data\anime.ts"

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
        lines.append(f'\t{{\n\t\ttitle: "{item["title"]}",\n\t\tstatus: "{item["status"]}",\n\t\trating: {item["rating"]},\n\t\tcover: "{item["cover"]}",\n\t\tdescription: "{item["description"]}",\n\t\tepisodes: "{item["episodes"]}",\n\t\tyear: "{item["year"]}",\n\t\tgenre: [{genre_str}],\n\t\tstudio: "{item["studio"]}",\n\t\tlink: "{item["link"]}",\n\t\tprogress: {item["progress"]},\n\t\ttotalEpisodes: {item["totalEpisodes"]},\n\t\tstartDate: "{item["startDate"]}",\n\t\tendDate: "{item["endDate"]}"\n\t}},')
    lines.append('];\n\nexport default localAnimeList;\n')
    with open(ANIME_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

@router.get("/")
def list_anime():
    return parse_anime()

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
