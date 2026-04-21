from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import json
from datetime import datetime

from models import get_db, User, FishingRecord
from auth import hash_password, verify_password, create_token, get_current_user, get_admin_user

app = FastAPI(title="钓鱼数据看板 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# Pydantic Schemas
# ===========================
class RegisterIn(BaseModel):
    username: str
    password: str

class LoginIn(BaseModel):
    username: str
    password: str

class CatchIn(BaseModel):
    species: str
    count: int = 1
    weight: float = 0
    max_weight: float = 0

class RecordIn(BaseModel):
    id: Optional[int] = None
    date: str
    time: str = ""
    location: str
    weather: str
    temp: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    wind: str = ""
    water_temp: Optional[float] = None
    water_level: str = ""
    method: str = ""
    bait: str = ""
    rating: Optional[int] = None
    notes: str = ""
    catches: List[CatchIn] = []

class AdminUserOut(BaseModel):
    id: int
    username: str
    is_admin: bool
    created_at: str
    record_count: int = 0
    total_weight: float = 0

# ===========================
# Auth Endpoints
# ===========================
@app.post("/api/register")
def register(body: RegisterIn, db: Session = Depends(get_db)):
    if len(body.username) < 3:
        raise HTTPException(status_code=400, detail="用户名至少3个字符")
    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="密码至少6个字符")
    existing = db.query(User).filter(User.username == body.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已被注册")

    is_first = db.query(User).count() == 0
    user = User(
        username=body.username,
        password_hash=hash_password(body.password),
        is_admin=is_first
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_token(user.id, user.username, user.is_admin)
    return {
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "is_admin": user.is_admin
        }
    }

@app.post("/api/login")
def login(body: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_token(user.id, user.username, user.is_admin)
    return {
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "is_admin": user.is_admin
        }
    }

@app.get("/api/me")
def get_me(current = Depends(get_current_user)):
    return current

# ===========================
# Fishing Record Endpoints
# ===========================
@app.get("/api/records")
def list_records(
    db: Session = Depends(get_db),
    current: dict = Depends(get_current_user)
):
    records = db.query(FishingRecord).filter(
        FishingRecord.user_id == current["id"]
    ).order_by(FishingRecord.date.desc()).all()
    return [_record_to_dict(r) for r in records]

@app.post("/api/records")
def create_record(
    body: RecordIn,
    db: Session = Depends(get_db),
    current: dict = Depends(get_current_user)
):
    catches = [{"species": c.species, "count": c.count, "weight": c.weight, "maxWeight": c.max_weight} for c in body.catches]
    total_weight = sum(c.weight for c in body.catches)
    total_count = sum(c.count for c in body.catches)
    record = FishingRecord(
        user_id=current["id"],
        date=body.date,
        time=body.time,
        location=body.location,
        weather=body.weather,
        temp=body.temp,
        humidity=body.humidity,
        pressure=body.pressure,
        wind=body.wind,
        water_temp=body.water_temp,
        water_level=body.water_level,
        method=body.method,
        bait=body.bait,
        rating=body.rating,
        notes=body.notes,
        catches_json=json.dumps(catches, ensure_ascii=False),
        total_weight=total_weight,
        total_count=total_count
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return _record_to_dict(record)

@app.put("/api/records/{record_id}")
def update_record(
    record_id: int,
    body: RecordIn,
    db: Session = Depends(get_db),
    current: dict = Depends(get_current_user)
):
    record = db.query(FishingRecord).filter(
        FishingRecord.id == record_id,
        FishingRecord.user_id == current["id"]
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在或无权修改")
    catches = [{"species": c.species, "count": c.count, "weight": c.weight, "maxWeight": c.max_weight} for c in body.catches]
    record.date = body.date
    record.time = body.time
    record.location = body.location
    record.weather = body.weather
    record.temp = body.temp
    record.humidity = body.humidity
    record.pressure = body.pressure
    record.wind = body.wind
    record.water_temp = body.water_temp
    record.water_level = body.water_level
    record.method = body.method
    record.bait = body.bait
    record.rating = body.rating
    record.notes = body.notes
    record.catches_json = json.dumps(catches, ensure_ascii=False)
    record.total_weight = sum(c.weight for c in body.catches)
    record.total_count = sum(c.count for c in body.catches)
    db.commit()
    db.refresh(record)
    return _record_to_dict(record)

@app.delete("/api/records/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current: dict = Depends(get_current_user)
):
    record = db.query(FishingRecord).filter(
        FishingRecord.id == record_id,
        FishingRecord.user_id == current["id"]
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在或无权删除")
    db.delete(record)
    db.commit()
    return {"ok": True}

# ===========================
# Admin Endpoints
# ===========================
@app.get("/api/admin/users")
def admin_list_users(
    db: Session = Depends(get_db),
    current: dict = Depends(get_admin_user)
):
    users = db.query(User).all()
    result = []
    for u in users:
        records = db.query(FishingRecord).filter(FishingRecord.user_id == u.id).all()
        result.append({
            "id": u.id,
            "username": u.username,
            "is_admin": u.is_admin,
            "created_at": u.created_at.strftime("%Y-%m-%d %H:%M"),
            "record_count": len(records),
            "total_weight": sum(r.total_weight for r in records)
        })
    return result

@app.get("/api/admin/users/{user_id}/records")
def admin_get_user_records(
    user_id: int,
    db: Session = Depends(get_db),
    current: dict = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    records = db.query(FishingRecord).filter(
        FishingRecord.user_id == user_id
    ).order_by(FishingRecord.date.desc()).all()
    return {
        "user": {"id": user.id, "username": user.username},
        "records": [_record_to_dict(r) for r in records]
    }

@app.post("/api/admin/users/{user_id}/set-admin")
def admin_set_admin(
    user_id: int,
    is_admin: bool = True,
    db: Session = Depends(get_db),
    current: dict = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.is_admin = is_admin
    db.commit()
    return {"ok": True, "is_admin": is_admin}

@app.delete("/api/admin/users/{user_id}")
def admin_delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current: dict = Depends(get_admin_user)
):
    if user_id == current["id"]:
        raise HTTPException(status_code=400, detail="不能删除自己")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db.delete(user)
    db.commit()
    return {"ok": True}

# ===========================
# Helper
# ===========================
def _record_to_dict(r: FishingRecord) -> dict:
    return {
        "id": r.id,
        "user_id": r.user_id,
        "date": r.date,
        "time": r.time,
        "location": r.location,
        "weather": r.weather,
        "temp": r.temp,
        "humidity": r.humidity,
        "pressure": r.pressure,
        "wind": r.wind,
        "water_temp": r.water_temp,
        "water_level": r.water_level,
        "method": r.method,
        "bait": r.bait,
        "rating": r.rating,
        "notes": r.notes,
        "catches": json.loads(r.catches_json) if r.catches_json else [],
        "totalWeight": r.total_weight,
        "totalCount": r.total_count,
        "created_at": r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else ""
    }

# ===========================
# Serve Frontend
# ===========================
@app.get("/")
def serve_index():
    return FileResponse("../frontend/index.html")

@app.get("/{path:path}")
def serve_frontend(path: str):
    file_path = f"../frontend/{path}"
    import os
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse("../frontend/index.html")


# 云平台部署：支持 PORT 环境变量
if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
