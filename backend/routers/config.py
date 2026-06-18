from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import re

router = APIRouter()

CONFIG_PATH = r"D:\boke\Mizuki\src\config\siteConfig.ts"

class SiteConfig(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    siteURL: Optional[str] = None
    siteStartDate: Optional[str] = None

def read_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    result = {}
    for key in ["title", "subtitle", "siteURL", "siteStartDate"]:
        match = re.search(rf'{key}:\s*"([^"]*)"', content)
        if match:
            result[key] = match.group(1)
    return result

def write_config(data: dict):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    for key, value in data.items():
        if value:
            content = re.sub(rf'({key}:\s*)"[^"]*"', rf'\1"{value}"', content)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(content)

@router.get("/")
def get_config():
    return read_config()

@router.put("/")
def update_config(data: SiteConfig):
    write_config(data.model_dump(exclude_none=True))
    return {"message": "配置已更新"}
