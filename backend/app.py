import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# إنشاء تطبيق FastAPI
app = FastAPI(title="EXCORA PRO API")

# 1. إعدادات CORS - تسمح للواجهة الأمامية بالاتصال بالسيرفر من أي مكان
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. إعداد مسارات الملفات الثابتة (للتوافق مع Render و Acode)
# نخرج من مجلد backend لنصل للمجلد الرئيسي EXCORA
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# نحدد مكان مجلد الصور: EXCORA/frontend/static
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")

# التأكد من وجود المجلد وتفعيله
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    print(f"✅ Static files mounted successfully from: {STATIC_DIR}")
else:
    # هذا التنبيه سيظهر في Logs موقع Render إذا كان هناك خطأ في التسمية
    print(f"❌ Warning: Static directory NOT found at {STATIC_DIR}")

# 3. المسار الرئيسي لفحص الحالة
@app.get("/")
def home():
    return {
        "status": "EXCORA Engine Online",
        "platform": "Render Cloud",
        "developer": "Samer Salman",
        "logo_path": "/static/logo.png"
    }

# 4. تشغيل السيرفر بما يتوافق مع بيئة Render السحابية
if __name__ == "__main__":
    # Render يخصص المنفذ تلقائياً عبر متغير البيئة PORT
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
