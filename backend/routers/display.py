from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import re

router = APIRouter()

CONFIG_PATH = r"D:\boke\Mizuki\src\config\siteConfig.ts"

class DisplaySettings(BaseModel):
    wallpaperMode: Optional[str] = None
    bannerTitle: Optional[bool] = None
    bannerWaves: Optional[bool] = None
    postListMode: Optional[str] = None
    fixedWallpaper: Optional[bool] = None
    fixedBanner: Optional[bool] = None
    fixedLayout: Optional[bool] = None

def read_settings():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    result = {}
    # 壁纸模式
    wm = re.search(r'wallpaperMode.*?defaultMode:\s*"(banner|fullscreen|none)"', content, re.DOTALL)
    if wm: result["wallpaperMode"] = wm.group(1)
    # 横幅标题
    bt = re.search(r'homeText.*?enable:\s*(true|false)', content, re.DOTALL)
    if bt: result["bannerTitle"] = bt.group(1) == "true"
    # 水波纹
    bw = re.search(r'waves.*?enable:\s*(true|false)', content, re.DOTALL)
    if bw: result["bannerWaves"] = bw.group(1) == "true"
    # 布局
    pl = re.search(r'postListLayout.*?defaultMode:\s*"(list|grid)"', content, re.DOTALL)
    if pl: result["postListMode"] = pl.group(1)
    # 锁定配置
    fw = re.search(r'fixedWallpaper:\s*(true|false)', content)
    result["fixedWallpaper"] = fw.group(1) == "true" if fw else False
    fb = re.search(r'fixedBanner:\s*(true|false)', content)
    result["fixedBanner"] = fb.group(1) == "true" if fb else False
    fl = re.search(r'fixedLayout:\s*(true|false)', content)
    result["fixedLayout"] = fl.group(1) == "true" if fl else False
    return result

@router.get("/")
def get_settings():
    return read_settings()

@router.put("/")
def update_settings(data: DisplaySettings):
    # 读取当前配置文件内容
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 只更新传入的字段，其他字段保持不变
    # 更新壁纸模式
    if data.wallpaperMode:
        content = re.sub(
            r'(wallpaperMode.*?defaultMode:\s*)"(banner|fullscreen|none)"',
            f'\\1"{data.wallpaperMode}"',
            content, count=1, flags=re.DOTALL
        )
    
    # 更新横幅标题
    if data.bannerTitle is not None:
        content = re.sub(
            r'(homeText.*?enable:\s*)(true|false)',
            f'\\g<1>{"true" if data.bannerTitle else "false"}',
            content, count=1, flags=re.DOTALL
        )
    
    # 更新水波纹
    if data.bannerWaves is not None:
        content = re.sub(
            r'(waves.*?enable:\s*)(true|false)',
            f'\\g<1>{"true" if data.bannerWaves else "false"}',
            content, count=1, flags=re.DOTALL
        )
    
    # 更新布局
    if data.postListMode:
        content = re.sub(
            r'(postListLayout.*?defaultMode:\s*)"(list|grid)"',
            f'\\1"{data.postListMode}"',
            content, count=1, flags=re.DOTALL
        )
    
    # 更新锁定字段 - 只替换已存在的字段值
    if data.fixedWallpaper is not None:
        val = "true" if data.fixedWallpaper else "false"
        if 'fixedWallpaper:' in content:
            content = re.sub(r'(fixedWallpaper:\s*)(true|false)', f'\\1{val}', content)
    
    if data.fixedBanner is not None:
        val = "true" if data.fixedBanner else "false"
        if 'fixedBanner:' in content:
            content = re.sub(r'(fixedBanner:\s*)(true|false)', f'\\1{val}', content)
    
    if data.fixedLayout is not None:
        val = "true" if data.fixedLayout else "false"
        if 'fixedLayout:' in content:
            content = re.sub(r'(fixedLayout:\s*)(true|false)', f'\\1{val}', content)
    
    # 写入更新后的配置
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    
    return {"message": "设置已更新", "settings": read_settings()}
