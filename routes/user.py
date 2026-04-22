from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["User Management"])

@app.post("/login")
def login(username: str, password: str):
    # هنا تضع منطق التحقق من المشتركين
    return {"message": "Welcome Samer Salman", "access": "Granted"}
