from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import re

router = APIRouter()

SKILLS_PATH = r"D:\boke\Mizuki\src\data\skills.ts"

class Skill(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""
    icon: Optional[str] = ""
    category: str
    level: str
    experience_years: Optional[int] = 0
    experience_months: Optional[int] = 0
    color: Optional[str] = ""

def parse_skills():
    with open(SKILLS_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    items = []
    # 逐个匹配技能对象
    pattern = r'\{\s*id:\s*"([^"]*)",\s*name:\s*"([^"]*)",\s*description:\s*"([^"]*)",\s*icon:\s*"([^"]*)",\s*category:\s*"([^"]*)",\s*level:\s*"([^"]*)",\s*experience:\s*\{\s*years:\s*(\d+),\s*months:\s*(\d+)'
    for match in re.finditer(pattern, content, re.DOTALL):
        items.append({
            "id": match.group(1),
            "name": match.group(2),
            "description": match.group(3),
            "icon": match.group(4),
            "category": match.group(5),
            "level": match.group(6),
            "experience_years": int(match.group(7)),
            "experience_months": int(match.group(8)),
            "color": ""
        })
    # 提取color
    color_matches = re.findall(r'id:\s*"(\w+)"[^}]*?color:\s*"([^"]*)"', content, re.DOTALL)
    color_map = {m[0]: m[1] for m in color_matches}
    for item in items:
        item["color"] = color_map.get(item["id"], "")
    return items

def write_skills(items: list):
    content = 'export interface Skill {\n\tid: string;\n\tname: string;\n\tdescription: string;\n\ticon: string;\n\tcategory: "frontend" | "backend" | "database" | "tools" | "other";\n\tlevel: "beginner" | "intermediate" | "advanced" | "expert";\n\texperience: { years: number; months: number; };\n\tcolor?: string;\n}\n\nexport const skillsData: Skill[] = [\n'
    for item in items:
        content += f'\t{{\n\t\tid: "{item["id"]}",\n\t\tname: "{item["name"]}",\n\t\tdescription: "{item["description"]}",\n\t\ticon: "{item["icon"]}",\n\t\tcategory: "{item["category"]}",\n\t\tlevel: "{item["level"]}",\n\t\texperience: {{ years: {item.get("experience_years", 0)}, months: {item.get("experience_months", 0)} }},\n\t\tcolor: "{item.get("color", "")}"\n\t}},\n'
    content += '];\n'
    with open(SKILLS_PATH, "w", encoding="utf-8") as f:
        f.write(content)

@router.get("/")
def list_skills():
    return parse_skills()

@router.post("/")
def create_skill(data: Skill):
    items = parse_skills()
    items.append(data.model_dump())
    write_skills(items)
    return {"message": "技能已添加"}

@router.put("/{skill_id}")
def update_skill(skill_id: str, data: Skill):
    items = parse_skills()
    for i, item in enumerate(items):
        if item["id"] == skill_id:
            items[i] = data.model_dump()
            break
    write_skills(items)
    return {"message": "技能已更新"}

@router.delete("/{skill_id}")
def delete_skill(skill_id: str):
    items = parse_skills()
    items = [i for i in items if i["id"] != skill_id]
    write_skills(items)
    return {"message": "技能已删除"}
