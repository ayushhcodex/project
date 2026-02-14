from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

# Import the parser you just created
from .md_parser import parse_markdown_file, get_pygments_css

app = FastAPI()

# Tell FastAPI where your static files (CSS/Images) and Templates are
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

BLOG_DIR = "content/blogs"
from fastapi.staticfiles import StaticFiles

# This tells FastAPI to serve any file inside 'content' as a static file
app.mount("/content", StaticFiles(directory="content"), name="content")
@app.get("/")
async def home(request: Request):
    # This renders your index.html (the one with your NITRA & IIT Madras info)
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/blog")
async def blog_index(request: Request):
    # Logic to list all your markdown files
    posts = []
    for filename in os.listdir(BLOG_DIR):
        if filename.endswith(".md"):
            path = os.path.join(BLOG_DIR, filename)
            meta, _ = parse_markdown_file(path)
            meta['slug'] = filename.replace('.md', '')
            posts.append(meta)
    
    # Sort by date (newest first)
    posts.sort(key=lambda x: x.get('date', ''), reverse=True)
    return templates.TemplateResponse("blog_index.html", {"request": request, "posts": posts})

@app.get("/blog/{slug}")
async def blog_post(request: Request, slug: str):
    path = os.path.join(BLOG_DIR, f"{slug}.md")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Use your md_parser to get the content
    meta, content = parse_markdown_file(path)
    pygments_css = get_pygments_css()
    
    return templates.TemplateResponse("blog_post.html", {
        "request": request, 
        "content": content, 
        "meta": meta,
        "pygments_css": pygments_css
    })