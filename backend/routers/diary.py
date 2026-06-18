from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import re, os, shutil

router = APIRouter()

DIARY_PATH = r"D:\boke\Mizuki\src\data\diary.ts"
DIARY_IMG_DIR = r"D:\boke\Mizuki\public\images\diary"

os.makedirs(DIARY_IMG_DIR, exist_ok=True)

class DiaryItem(BaseModel):
    id: Optional[int] = None
    content: str
    date: Optional[str] = None
    images: Optional[List[str]] = []

def parse_diary():
    with open(DIARY_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    items = []
    pattern = r'\{[^{}]*?id:\s*(\d+)[^{}]*?content:\s*"([^"]*)"[^{}]*?date:\s*"([^"]*)"[^{}]*?\}'
    for match in re.finditer(pattern, content):
        item = {
            "id": int(match.group(1)),
            "content": match.group(2),
            "date": match.group(3),
        }
        block = match.group(0)
        images_match = re.search(r'images:\s*\[([^\]]*)\]', block)
        if images_match:
            images = re.findall(r'"([^"]*)"', images_match.group(1))
            item["images"] = images
        items.append(item)
    return items

def write_diary(items: list):
    content = """// 日记数据配置
export interface DiaryItem {
\tid: number;
\tcontent: string;
\tdate: string;
\timages?: string[];
\ttags?: string[];
}

const diaryData: DiaryItem[] = [
"""
    for item in items:
        images_str = ""
        if item.get("images"):
            images_str = f',\n\t\timages: [{", ".join(f"\"{i}\"" for i in item["images"])}]'
        content += f'\t{{\n\t\tid: {item["id"]},\n\t\tcontent: "{item["content"]}",\n\t\tdate: "{item["date"]}"{images_str}\n\t}},\n'
    content += """];

export const getDiaryList = (limit?: number) => {
\tconst sortedData = [...diaryData].sort(
\t\t(a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
\t);
\tif (limit && limit > 0) return sortedData.slice(0, limit);
\treturn sortedData;
};

export const getAllTags = () => {
\tconst tags = new Set<string>();
\tfor (const item of diaryData) {
\t\tif (item.tags) {
\t\t\tfor (const tag of item.tags) {
\t\t\t\ttags.add(tag);
\t\t\t}
\t\t}
\t}
\treturn Array.from(tags).sort();
};

export default diaryData;
"""
    with open(DIARY_PATH, "w", encoding="utf-8") as f:
        f.write(content)

@router.get("/images/{filename}")
def get_image(filename: str):
    filepath = os.path.join(DIARY_IMG_DIR, filename)
    if os.path.exists(filepath):
        return FileResponse(filepath)
    return {"error": "not found"}

@router.get("/")
def list_diary():
    return parse_diary()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    filename = f"{int(datetime.now().timestamp())}_{file.filename}"
    filepath = os.path.join(DIARY_IMG_DIR, filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"url": f"/images/diary/{filename}"}

@router.post("/")
def create_diary(data: DiaryItem):
    items = parse_diary()
    new_id = max([i["id"] for i in items], default=0) + 1
    new_item = {
        "id": new_id,
        "content": data.content,
        "date": data.date or datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "images": data.images or []
    }
    items.insert(0, new_item)
    write_diary(items)
    return {"message": "日记已创建", "id": new_id}

@router.put("/{diary_id}")
def update_diary(diary_id: int, data: DiaryItem):
    items = parse_diary()
    for i, item in enumerate(items):
        if item["id"] == diary_id:
            items[i]["content"] = data.content
            if data.date:
                items[i]["date"] = data.date
            if data.images is not None:
                items[i]["images"] = data.images
            break
    write_diary(items)
    return {"message": "日记已更新"}

@router.delete("/{diary_id}")
def delete_diary(diary_id: int):
    items = parse_diary()
    items = [i for i in items if i["id"] != diary_id]
    write_diary(items)
    return {"message": "日记已删除"}
