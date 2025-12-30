from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session

app = FastAPI(title="Task Manager API (SQLite)")

# -------------------------
# Database (SQLite)
# -------------------------
DATABASE_URL = "sqlite:///./tasks.db"  # קובץ מקומי בתיקיית הפרויקט

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # חובה ב-SQLite עם FastAPI
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    done = Column(Boolean, default=False, nullable=False)


@app.on_event("startup")
def on_startup():
    # יוצר טבלאות אם לא קיימות
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Schemas (מה נכנס/יוצא ב-JSON)
# -------------------------
class TaskCreate(BaseModel):
    title: str
    done: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


class TaskOut(BaseModel):
    id: int
    title: str
    done: bool

    class Config:
        from_attributes = True  # מאפשר לקרוא ישירות מאובייקט SQLAlchemy


# -------------------------
# Routes
# -------------------------
@app.get("/")
def home():
    return {"message": "Task Manager API (SQLite) is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=List[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(TaskDB).order_by(TaskDB.id.asc()).all()


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = TaskDB(title=payload.title, done=payload.done)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # PATCH אמיתי: מעדכן רק מה שנשלח
    if payload.title is not None:
        task.title = payload.title
    if payload.done is not None:
        task.done = payload.done

    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return
