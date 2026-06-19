from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
import re, os, shutil

router = APIRouter()

MUSIC_TS_PATH = r"D:\boke\Mizuki\src\components\widgets\music-player\constants.ts"
MUSIC_URL_DIR = r"D:\boke\Mizuki\public\assets\music\url"
MUSIC_COVER_DIR = r"D:\boke\Mizuki\public\assets\music\cover"

class Song(BaseModel):
    title: str
    artist: str
    url: Optional[str] = ""
    cover: Optional[str] = ""
    duration: Optional[int] = 0

def parse_songs():
    with open(MUSIC_TS_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    songs = []
    pattern = r'\{\s*id:\s*(\d+),\s*title:\s*"([^"]*)",\s*artist:\s*"([^"]*)",\s*cover:\s*"([^"]*)",\s*url:\s*"([^"]*)",\s*duration:\s*(\d+)'
    for match in re.finditer(pattern, content):
        songs.append({
            "id": int(match.group(1)),
            "title": match.group(2),
            "artist": match.group(3),
            "cover": match.group(4),
            "url": match.group(5),
            "duration": int(match.group(6))
        })
    return songs

def write_songs(songs: list):
    content = '''import type { Song } from "./types";

export const STORAGE_KEY_VOLUME = "music-player-volume";

export const DEFAULT_VOLUME = 0.7;

export const LOCAL_PLAYLIST: Song[] = [
'''
    for song in songs:
        content += f'\t{{\n\t\tid: {song["id"]},\n\t\ttitle: "{song["title"]}",\n\t\tartist: "{song["artist"]}",\n\t\tcover: "{song["cover"]}",\n\t\turl: "{song["url"]}",\n\t\tduration: {song["duration"]},\n\t}},\n'
    content += '''];

export const DEFAULT_SONG: Song = {
	title: "Sample Song",
	artist: "Sample Artist",
	cover: "/favicon/favicon.ico",
	url: "",
	duration: 0,
	id: 0,
};

export const DEFAULT_METING_API =
	"https://www.bilibili.uno/api?server=:server&type=:type&id=:id&auth=:auth&r=:r";
export const DEFAULT_METING_ID = "14164869977";
export const DEFAULT_METING_SERVER = "netease";
export const DEFAULT_METING_TYPE = "playlist";

export const ERROR_DISPLAY_DURATION = 3000;
export const SKIP_ERROR_DELAY = 1000;
'''
    with open(MUSIC_TS_PATH, "w", encoding="utf-8") as f:
        f.write(content)

@router.get("/")
def list_songs():
    return parse_songs()

@router.post("/")
def create_song(data: Song):
    songs = parse_songs()
    new_id = max([s["id"] for s in songs], default=0) + 1
    songs.append({
        "id": new_id,
        "title": data.title,
        "artist": data.artist,
        "cover": data.cover or "assets/music/cover/default.webp",
        "url": data.url or "",
        "duration": data.duration or 0
    })
    write_songs(songs)
    return {"message": "歌曲已添加", "id": new_id}

@router.put("/{song_id}")
def update_song(song_id: int, data: Song):
    songs = parse_songs()
    for i, song in enumerate(songs):
        if song["id"] == song_id:
            songs[i]["title"] = data.title
            songs[i]["artist"] = data.artist
            if data.cover:
                songs[i]["cover"] = data.cover
            if data.url:
                songs[i]["url"] = data.url
            if data.duration:
                songs[i]["duration"] = data.duration
            break
    write_songs(songs)
    return {"message": "歌曲已更新"}

@router.delete("/{song_id}")
def delete_song(song_id: int):
    songs = parse_songs()
    songs = [s for s in songs if s["id"] != song_id]
    write_songs(songs)
    return {"message": "歌曲已删除"}

@router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    filename = f"{int(os.path.getmtime(MUSIC_URL_DIR)) if os.path.exists(MUSIC_URL_DIR) else 0}_{file.filename}"
    filepath = os.path.join(MUSIC_URL_DIR, filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"url": f"assets/music/url/{filename}"}

@router.post("/upload-cover")
async def upload_cover(file: UploadFile = File(...)):
    filename = f"{int(os.path.getmtime(MUSIC_COVER_DIR)) if os.path.exists(MUSIC_COVER_DIR) else 0}_{file.filename}"
    filepath = os.path.join(MUSIC_COVER_DIR, filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"url": f"assets/music/cover/{filename}"}
