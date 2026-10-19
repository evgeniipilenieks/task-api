from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import pymysql
from fastapi import FastAPI, Depends, HTTPException

# ==========================================
# НАСТРОЙКА БАЗЫ ДАННЫХ
# ==========================================
# Замени 'ТВОЙ_ПАРОЛЬ' на пароль от MySQL
DATABASE_URL = "mysql+pymysql://root:parole@localhost/fastapi_db"

# Создаем подключение
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==========================================
# ОПИСАНИЕ ТАБЛИЦЫ
# ==========================================
class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    status = Column(String(50), default="new")
    priority = Column(String(50), default="medium")

# Создаем таблицу в базе (если ее нет)
Base.metadata.create_all(bind=engine)

# ==========================================
# PYDANTIC-МОДЕЛИ (для API)
# ==========================================
class TaskCreate(BaseModel):
    title: str
    status: str = "new"
    priority: str = "medium"

class TaskResponse(TaskCreate):
    id: int

    class Config:
        from_attributes = True # Позволяет Pydantic читать данные из SQLAlchemy

# ==========================================
# ЗАВИСИМОСТЬ (даем доступ к БД)
# ==========================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# FASTAPI ПРИЛОЖЕНИЕ
# ==========================================
app = FastAPI()

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(status: str = None, db: Session = Depends(get_db)):
    query = db.query(TaskDB)
    if status:
        query = query.filter(TaskDB.status == status)
    return query.all()

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Превращаем Pydantic-модель в объект SQLAlchemy
    db_task = TaskDB(**task.model_dump())
    
    # Сохраняем в БД
    db.add(db_task)
    db.commit()
    db.refresh(db_task) # Получаем id, который сгенерировал MySQL
    
    return db_task
    
# ==========================================
# PUT (Обновление задачи)
# ==========================================
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskCreate, db: Session = Depends(get_db)):
    # 1. Ищем задачу в базе по ID
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    
    # 2. Если не нашли — возвращаем ошибку 404
    if db_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # 3. Обновляем поля
    db_task.title = task_update.title
    db_task.status = task_update.status
    db_task.priority = task_update.priority
    
    # 4. Сохраняем изменения
    db.commit()
    db.refresh(db_task)
    
    return db_task

# ==========================================
# DELETE (Удаление задачи)
# ==========================================
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    # 1. Ищем задачу
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    
    # 2. Если нет — ошибка 404
    if db_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    # 3. Удаляем из базы
    db.delete(db_task)
    db.commit()
    
    return {"message": f"Задача с id={task_id} удалена"}