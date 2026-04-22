from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import uvicorn
import requests
import os

# 1. تنظيف واجهة السجلات (Logs)
# هذا السطر يمنع ظهور مئات طلبات الـ GET المتكررة ويجعل الشاشة مريحة للعين
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

app = FastAPI(title="EXCORA PRO REAL-TIME API")

# 2. إعدادات الـ CORS للاتصال من الويب أو الأندرويد
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- إضافة دعم الملفات الثابتة (الصور) ---
# تأكد من إنشاء مجلد باسم static وبداخله مجلد images في نفس مسار هذا الملف
if not os.path.exists("static"):
    os.makedirs("static/images")

app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. دالة جلب السعر الحقيقي من Binance
@app.get("/price/{symbol}")
def get_binance_price(symbol: str):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
        response = requests.get(url)
        data = response.json()
        return {"symbol": data["symbol"], "price": data["price"]}
    except Exception as e:
        return {"error": "تحقق من رمز العملة أو اتصال الإنترنت", "details": str(e)}

# نقطة اختبار بسيطة للتأكد من عمل السيرفر
@app.get("/")
def read_root():
    return {"message": "Welcome to EXCORA PRO API", "status": "Online"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
