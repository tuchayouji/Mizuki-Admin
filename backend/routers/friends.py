from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import re

router = APIRouter()

FRIENDS_PATH = r"D:\boke\Mizuki\src\data\friends.ts"

class Friend(BaseModel):
    name: str
    url: str
    avatar: Optional[str] = ""
    description: Optional[str] = ""
    tags: Optional[List[str]] = []

def parse_friends():
    try:
        with open(FRIENDS_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        items = []
        pattern = r'\{[^{}]*?id:\s*(\d+)[^{}]*?title:\s*"([^"]*)"[^{}]*?imgurl:\s*"([^"]*)"[^{}]*?desc:\s*"([^"]*)"[^{}]*?siteurl:\s*"([^"]*)"[^{}]*?\}'
        for match in re.finditer(pattern, content):
            block = match.group(0)
            tags_match = re.search(r'tags:\s*\[([^\]]*)\]', block)
            tags = [t.strip().strip('"') for t in tags_match.group(1).split(",")] if tags_match else []
            items.append({
                "id": int(match.group(1)),
                "name": match.group(2),
                "url": match.group(5),
                "avatar": match.group(3),
                "description": match.group(4),
                "tags": tags
            })
        return items
    except Exception as e:
        print(e)
        return []

def write_friends(items: list):
    content = 'export interface FriendItem {\n\tid: number;\n\ttitle: string;\n\timgurl: string;\n\tdesc: string;\n\tsiteurl: string;\n\ttags: string[];\n}\n\nexport const friendsData: FriendItem[] = [\n'
    for item in items:
        tags_str = ", ".join(f'"{t}"' for t in item.get("tags", []))
        content += f'\t{{\n\t\tid: {item.get("id", 1)},\n\t\ttitle: "{item["name"]}",\n\t\timgurl: "{item.get("avatar", "")}",\n\t\tdesc: "{item.get("description", "")}",\n\t\tsiteurl: "{item["url"]}",\n\t\ttags: [{tags_str}]\n\t}},\n'
    content += '];\n'
    with open(FRIENDS_PATH, "w", encoding="utf-8") as f:
        f.write(content)

@router.get("/")
def list_friends():
    return parse_friends()

@router.post("/")
def create_friend(data: Friend):
    items = parse_friends()
    new_id = max([i.get("id", 0) for i in items], default=0) + 1
    items.append({
        "id": new_id,
        "name": data.name,
        "url": data.url,
        "avatar": data.avatar,
        "description": data.description,
        "tags": data.tags or []
    })
    write_friends(items)
    return {"message": "友链已添加"}

@router.put("/{name}")
def update_friend(name: str, data: Friend):
    items = parse_friends()
    for i, item in enumerate(items):
        if item["name"] == name:
            items[i]["name"] = data.name
            items[i]["url"] = data.url
            items[i]["avatar"] = data.avatar
            items[i]["description"] = data.description
            if data.tags:
                items[i]["tags"] = data.tags
            break
    write_friends(items)
    return {"message": "友链已更新"}

@router.delete("/{name}")
def delete_friend(name: str):
    items = parse_friends()
    items = [i for i in items if i["name"] != name]
    write_friends(items)
    return {"message": "友链已删除"}
