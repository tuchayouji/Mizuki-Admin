from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import re

router = APIRouter()

PROJECTS_PATH = r"D:\boke\Mizuki\src\data\projects.ts"

class Project(BaseModel):
    id: str
    title: str
    description: Optional[str] = ""
    category: str
    status: str
    techStack: Optional[List[str]] = []
    sourceCode: Optional[str] = ""
    liveDemo: Optional[str] = ""

def parse_projects():
    try:
        with open(PROJECTS_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        items = []
        pattern = r'\{[^{}]*?id:\s*"([^"]*)"[^{}]*?title:\s*"([^"]*)"[^{}]*?description:\s*"([^"]*)"[^{}]*?category:\s*"([^"]*)"[^{}]*?status:\s*"([^"]*)"[^{}]*?\}'
        for match in re.finditer(pattern, content):
            block = match.group(0)
            tech_match = re.search(r'techStack:\s*\[([^\]]*)\]', block)
            src_match = re.search(r'sourceCode:\s*"([^"]*)"', block)
            demo_match = re.search(r'liveDemo:\s*"([^"]*)"', block)
            items.append({
                "id": match.group(1),
                "title": match.group(2),
                "description": match.group(3),
                "category": match.group(4),
                "status": match.group(5),
                "techStack": [t.strip().strip('"') for t in tech_match.group(1).split(",")] if tech_match else [],
                "sourceCode": src_match.group(1) if src_match else "",
                "liveDemo": demo_match.group(1) if demo_match else ""
            })
        return items
    except:
        return []

def write_projects(items: list):
    content = 'export interface Project {\n\tid: string;\n\ttitle: string;\n\tdescription: string;\n\timage: string;\n\tcategory: "web" | "mobile" | "desktop" | "other";\n\ttechStack: string[];\n\tstatus: "completed" | "in-progress" | "planned";\n\tliveDemo?: string;\n\tsourceCode?: string;\n}\n\nexport const projectsData: Project[] = [\n'
    for item in items:
        tech_str = ", ".join(f'"{t}"' for t in item.get("techStack", []))
        content += f'\t{{\n\t\tid: "{item["id"]}",\n\t\ttitle: "{item["title"]}",\n\t\tdescription: "{item["description"]}",\n\t\timage: "",\n\t\tcategory: "{item["category"]}",\n\t\ttechStack: [{tech_str}],\n\t\tstatus: "{item["status"]}",\n\t\tsourceCode: "{item.get("sourceCode", "")}",\n\t\tliveDemo: "{item.get("liveDemo", "")}"\n\t}},\n'
    content += '];\n'
    with open(PROJECTS_PATH, "w", encoding="utf-8") as f:
        f.write(content)

@router.get("/")
def list_projects():
    return parse_projects()

@router.post("/")
def create_project(data: Project):
    items = parse_projects()
    items.append(data.model_dump())
    write_projects(items)
    return {"message": "项目已添加"}

@router.put("/{project_id}")
def update_project(project_id: str, data: Project):
    items = parse_projects()
    for i, item in enumerate(items):
        if item["id"] == project_id:
            items[i] = data.model_dump()
            break
    write_projects(items)
    return {"message": "项目已更新"}

@router.delete("/{project_id}")
def delete_project(project_id: str):
    items = parse_projects()
    items = [i for i in items if i["id"] != project_id]
    write_projects(items)
    return {"message": "项目已删除"}
