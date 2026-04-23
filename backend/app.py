from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

app = FastAPI(title="EXCORA PRO Terminal")

# ربط الصور والفيديوهات (logo.png, 1000017310.jpg, 1000017311.mp4)
app.mount("/static", StaticFiles(directory="."), name="static")

# بيانات الدخول (Username: admin | Password: excora2026)
USER_DB = {"admin": "excora2026"}

@app.get("/")
async def home():
    return FileResponse('index.html')

@app.get("/login-page")
async def login_page():
    return FileResponse('login.html')

@app.get("/dashboard")
async def dashboard():
    return FileResponse('dashboard.html')

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username in USER_DB and USER_DB[username] == password:
        return RedirectResponse(url="/dashboard", status_code=303)
    return {"status": "error", "message": "بيانات الدخول غير صحيحة"}
