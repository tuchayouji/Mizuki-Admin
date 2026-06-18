from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import re

router = APIRouter()

CONFIG_PATH = r"D:\boke\Mizuki\src\config\siteConfig.ts"

class ThemeConfig(BaseModel):
    hue: Optional[int] = None
    fixed: Optional[bool] = None

def read_theme():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    hue_match = re.search(r'hue:\s*(\d+)', content)
    fixed_match = re.search(r'fixed:\s*(true|false)', content)
    return {
        "hue": int(hue_match.group(1)) if hue_match else 240,
        "fixed": fixed_match.group(1) == "true" if fixed_match else False
    }

def write_theme(data: dict):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    if "hue" in data:
        content = re.sub(r'(hue:\s*)\d+', f'\\g<1>{data["hue"]}', content)
    if "fixed" in data:
        content = re.sub(r'(fixed:\s*)(true|false)', f'\\g<1>{"true" if data["fixed"] else "false"}', content)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(content)

@router.get("/")
def get_theme():
    return read_theme()

@router.put("/")
def update_theme(data: ThemeConfig):
    write_theme(data.model_dump(exclude_none=True))
    return {"message": "主题色已更新"}
