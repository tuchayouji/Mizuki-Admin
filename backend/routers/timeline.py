from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import re

router = APIRouter()

TIMELINE_PATH = r"D:\boke\Mizuki\src\data\timeline.ts"

class TimelineItem(BaseModel):
    id: str
    title: str
    description: Optional[str] = ""
    type: str
    startDate: str
    endDate: Optional[str] = ""
    location: Optional[str] = ""
    organization: Optional[str] = ""
    skills: Optional[List[str]] = []
    icon: Optional[str] = ""
    color: Optional[str] = ""

def parse_timeline():
    with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    items = []
    pattern = r'\{[^{}]*?id:\s*"([^"]*)"[^{}]*?title:\s*"([^"]*)"[^{}]*?description:\s*"([^"]*)"[^{}]*?type:\s*"([^"]*)"[^{}]*?startDate:\s*"([^"]*)"[^{}]*?\}'
    for match in re.finditer(pattern, content):
        block = match.group(0)
        end_match = re.search(r'endDate:\s*"([^"]*)"', block)
        loc_match = re.search(r'location:\s*"([^"]*)"', block)
        org_match = re.search(r'organization:\s*"([^"]*)"', block)
        skills_match = re.search(r'skills:\s*\[([^\]]*)\]', block)
        icon_match = re.search(r'icon:\s*"([^"]*)"', block)
        color_match = re.search(r'color:\s*"([^"]*)"', block)
        items.append({
            "id": match.group(1),
            "title": match.group(2),
            "description": match.group(3),
            "type": match.group(4),
            "startDate": match.group(5),
            "endDate": end_match.group(1) if end_match else "",
            "location": loc_match.group(1) if loc_match else "",
            "organization": org_match.group(1) if org_match else "",
            "skills": [s.strip().strip('"') for s in skills_match.group(1).split(",")] if skills_match else [],
            "icon": icon_match.group(1) if icon_match else "",
            "color": color_match.group(1) if color_match else ""
        })
    return items

def write_timeline(items: list):
    content = 'import type { TimelineItem } from "../components/features/timeline/types";\n\nexport const timelineData: TimelineItem[] = [\n'
    for item in items:
        skills_str = ", ".join(f'"{s}"' for s in item.get("skills", []))
        content += f'\t{{\n\t\tid: "{item["id"]}",\n\t\ttitle: "{item["title"]}",\n\t\tdescription: "{item["description"]}",\n\t\ttype: "{item["type"]}",\n\t\tstartDate: "{item["startDate"]}",\n\t\tendDate: "{item.get("endDate", "")}",\n\t\tlocation: "{item.get("location", "")}",\n\t\torganization: "{item.get("organization", "")}",\n\t\tskills: [{skills_str}],\n\t\ticon: "{item.get("icon", "")}",\n\t\tcolor: "{item.get("color", "")}"\n\t}},\n'
    content += '];\n'
    with open(TIMELINE_PATH, "w", encoding="utf-8") as f:
        f.write(content)

@router.get("/")
def list_timeline():
    return parse_timeline()

@router.post("/")
def create_timeline(data: TimelineItem):
    items = parse_timeline()
    items.append(data.model_dump())
    write_timeline(items)
    return {"message": "时间线已添加"}

@router.put("/{item_id}")
def update_timeline(item_id: str, data: TimelineItem):
    items = parse_timeline()
    for i, item in enumerate(items):
        if item["id"] == item_id:
            items[i] = data.model_dump()
            break
    write_timeline(items)
    return {"message": "时间线已更新"}

@router.delete("/{item_id}")
def delete_timeline(item_id: str):
    items = parse_timeline()
    items = [i for i in items if i["id"] != item_id]
    write_timeline(items)
    return {"message": "时间线已删除"}
